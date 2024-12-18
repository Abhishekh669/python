# import socket 
# import os 

# HOST = '0.0.0.0'

# def main():
#     if os.name == 'nt':
#         socket_protocol = socket.IPPROTO_IP
#     else:
#         socket_protocol = socket.IPPROTO_ICMP
#     sniffer = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket_protocol)
#     sniffer.bind((HOST,0))
#     sniffer.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)

#     if os.name == 'nt':
#         sniffer.ioctl(socket.SIO_RCVALL, socket.SIO.RCVALL_ON)
    
#     print("Listening to the packets....")
#     print(sniffer.recvfrom(65535))
#     if os.name == 'nt':
#         sniffer.ioctl(socket.SIO_RCVALL, socket.RCVALL_OFF)

# if __name__ == "__main__":
#     main()


import socket 
import ipaddress

MESSAGE = 'python rules'

SUBNET = '192.168.1.0/24'

def udp_sender():
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sender:
        for ip in ipaddress.ip_network(SUBNET).hosts():
            sender.sendto(MESSAGE.encode('utf8'), (str(ip), 65212))


udp_sender()