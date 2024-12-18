from scapy.all import sniff 

def packet_callback(packet):
    print(packet.show())


def main():
    sniff(prn=packet_callback, count = 3 ) #every time the packet is captured then the callback funciton is called 

if __name__ =="__main__":
    main()
