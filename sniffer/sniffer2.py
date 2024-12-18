import ipaddress
import os
import socket
import sys
import threading
import time
import struct

SUBNET = '192.168.1.0/24'
MESSAGE = 'PYTHON RULES '

class IP:
    def __init__(self, buff=None):
        if buff:
            header = struct.unpack('<BBHHHBBH4s4s', buff)
            self.ver = header[0] >> 4
            self.ihl = header[0] & 0xF
            self.tos = header[1]
            self.len = header[2]
            self.id = header[3]
            self.offset = header[4]
            self.ttl = header[5]
            self.protocol_num = header[6]
            self.sum = header[7]
            self.src = header[8]
            self.dst = header[9]

            print('-'*30)
            print("IPv4 header:")
            print('-'*30)
            print(f"Version: {self.ver}")
            print(f"IP header length: {self.ihl}")
            print(f"Type of service: {self.tos}")
            print(f"Payload length: {self.len}")
            print(f"Offset: {self.offset}")
            print(f"Time to live: {self.ttl}")
            print(f"Protocol number: {self.protocol_num}")
            print(f"Checksum: {self.sum}")
            print('-'*30)

            # Converts the raw data into IP addresses
            self.src_address = ipaddress.ip_address(self.src)
            self.dst_address = ipaddress.ip_address(self.dst)

class ICMP:
    def __init__(self, buff):
        header = struct.unpack('<BBHHH', buff)
        self.type = header[0]
        self.code = header[1]
        self.sum = header[2]
        self.id = header[3]
        self.seq = header[4]

        print('-'*30)
        print("ICMP header:")
        print('-'*30)
        print(f"Type: {self.type}")
        print(f"Code: {self.code}")
        print(f"Checksum: {self.sum}")
        print(f"ID: {self.id}")
        print(f"Sequence: {self.seq}")
        print('-'*30)

def udp_sender():
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sender:
        for ip in ipaddress.ip_network(SUBNET).hosts():
            sender.sendto(MESSAGE.encode('utf8'), (str(ip), 65212))

class Scanner:
    def __init__(self, host):
        self.host = host
        socket_protocol = socket.IPPROTO_ICMP
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket_protocol)
        self.socket.bind((host, 0))
        self.socket.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)

        if os.name == 'nt':
            self.socket.ioctl(socket.SIO_RCVALL, socket.RCVALL_ON)
    
    def sniff(self):
        hosts_up = set()

        try:
            while True:
                raw_buffer = self.socket.recvfrom(65535)[0]
                ip_header = IP(raw_buffer)

                if ip_header.protocol_num == 1:  # ICMP protocol number
                    offset = ip_header.ihl * 4
                    buff = raw_buffer[offset:offset + 8]
                    icmp_header = ICMP(buff)

                    if icmp_header.code == 3 and icmp_header.type == 3:
                        if ipaddress.ip_address(ip_header.src_address) in ipaddress.ip_network(SUBNET):
                            if raw_buffer[-len(MESSAGE):] == MESSAGE.encode('utf8'):
                                tgt = str(ip_header.src_address)
                                if tgt != self.host and tgt not in hosts_up:
                                    hosts_up.add(tgt)
                                    print(f"Host up: {tgt}")
        except KeyboardInterrupt:
            if os.name == 'nt':
                self.socket.ioctl(socket.SIO_RCVALL, socket.RCVALL_OFF)

            if hosts_up:
                print(f"\nSummary: Hosts up on {SUBNET}")
                for host in sorted(hosts_up):
                    print(f"{host}")
            print("")
            sys.exit()

if __name__ == '__main__':
    if len(sys.argv) == 2:
        host = sys.argv[1]
    else:
        host = '192.168.1.19'

    s = Scanner(host)

    t = threading.Thread(target=udp_sender)
    print("Starting UDP sender thread...")
    t.start()

    time.sleep(5)  # Sleep to allow UDP sender to send packets

    s.sniff()
