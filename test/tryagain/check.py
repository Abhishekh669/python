import ipaddress 
import os 
import socket 
import struct 
import sys 
import threading
import time 

SUBNET = '10.10.30.0/23'
MESSAGE = 'PYTHONRULES!'

def udp_sender():
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sender:
        for ip in ipaddress.ip_network(SUBNET).hosts():
            sender.sendto(MESSAGE.encode('utf8'), (str(ip), 65212))

class IP: 
    def __init__(self, buff=None):
        header = struct.unpack("<BBHHHBBH4s4s", buff)
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

        self.src_address = ipaddress.ip_address(self.src)
        self.dst_address = ipaddress.ip_address(self.dst)

        self.protocol_map = {1: "ICMP", 6: "TCP", 17: "UDP"}

        try:
            self.protocol = self.protocol_map[self.protocol_num]
        except Exception as e:
            print("%s No protocol for %s" % (e, self.protocol_num))

class ICMP:
    def __init__(self, buff):
        header = struct.unpack('<BBHHH', buff)
        self.type = header[0]
        self.code = header[1]
        self.sum = header[2]
        self.id = header[3]
        self.seq = header[4]

class Scanner:
    def __init__(self, host):
        self.host = host
        if os.name == "nt":
            socket_protocol = socket.IPPROTO_IP
        else:
            socket_protocol = socket.IPPROTO_ICMP
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket_protocol)  
        self.socket.bind((host, 0))
        self.socket.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)
        if os.name == 'nt':
            self.socket.ioctl(socket.SIO_RCVALL, socket.RCVALL_ON)

    def sniff(self):
        hosts_up = set()
        unreachable_hosts = set()  # Set to store unreachable hosts
        try:
            while True:
                print('-' * 30)
                print("Listening for ICMP messages...")
                raw_buffer = self.socket.recvfrom(65535)[0]
                ip_header = IP(raw_buffer[0:20])
                
                if ip_header.protocol == "ICMP":
                    offset = ip_header.ihl * 4 #for conversion to bytes 
                    buf = raw_buffer[offset:offset + 8] # since the header of hte icmp is 8 
                    icmp_header = ICMP(buf)
                    print(f"Host: {ip_header.src_address}  \nICMP Header - Code: {icmp_header.code}, Type: {icmp_header.type}")

                    # Check for unreachable hosts
                    if icmp_header.type == 3:  # Destination Unreachable
                        unreachable_hosts.add(ip_header.src_address)
                        print(f"Unreachable Host: {str(ip_header.src_address)}")
                    
                    # Check for specific unreachable port
                    if icmp_header.code == 3:  # Port Unreachable
                        if raw_buffer[len(raw_buffer) - len(MESSAGE):] == bytes(MESSAGE, 'utf8'):
                            hosts_up.add(ip_header.src_address)
                            print(f"Hosts up: {str(ip_header.src_address)}")

                print("-" * 30)
        except KeyboardInterrupt:
            if os.name == 'nt':
                self.socket.ioctl(socket.SIO_RCVALL, socket.RCVALL_OFF)
            print("\nUser interrupted.")
            if hosts_up:
                print(f"\nSummary: Hosts up on {SUBNET}")
                for host in sorted(hosts_up):
                    print(f'{host}')
            if unreachable_hosts:
                print(f"\nSummary: Unreachable Hosts on {SUBNET}")
                for host in sorted(unreachable_hosts):
                    print(f'{host}')
            print("")
            sys.exit()

if __name__ == "__main__":
    if len(sys.argv) == 2:
        host = sys.argv[1]
    else:
        host = "10.10.30.142"
    s = Scanner(host)
    time.sleep(10)
    t = threading.Thread(target=udp_sender)
    t.start()
    s.sniff()