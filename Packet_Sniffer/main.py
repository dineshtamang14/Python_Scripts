import scapy.all as scapy 
from scapy.layers import http


def sniff(interface: str) -> None:
    scapy.sniff(iface=interface, store=False, prn=process_sniffed_packet)
    
    
def process_sniffed_packet(packet) -> None:
    print(type(packet))
    if packet.haslayer(http.HTTPRequest):
        print(packet)
    
    
sniff("eth0")