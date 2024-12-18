import socket
import os

HOST = "0.0.0.0"  # Listen on all network interfaces

def main():
    try:
        if os.name == "nt":
            # Windows-specific setup
            socket_protocol = socket.IPPROTO_IP
            sniffer = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_IP)
        else:
            # Unix/Linux-specific setup
            socket_protocol = socket.IPPROTO_ICMP
            sniffer = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)

        # Bind to the specified host and any port
        sniffer.bind((HOST, 0))

        # Include IP headers in the captured packets
        sniffer.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)

        if os.name == 'nt':
            # Enable promiscuous mode on Windows
            sniffer.ioctl(socket.SIO_RCVALL, socket.RCVALL_ON)

        print("Listen@g for packets...")
        
        # Capture a packet
        packet, addr = sniffer.recvfrom(65565)
        print(f"Packet received from {addr[0]}:{addr[1]}")

        # Optional: Print the raw packet data
        print("Raw packet data:")
        print(packet)

    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        if os.name == 'nt':
            # Disable promiscuous mode on Windows
            sniffer.ioctl(socket.SIO_RCVALL, socket.RCVALL_OFF)
        sniffer.close()

if __name__ == '__main__':
    main()
