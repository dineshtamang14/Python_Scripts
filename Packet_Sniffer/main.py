import scapy.all as scapy 
from scapy.layers import http


def sniff(interface: str) -> None:
    '''Takes interface to sniff data'''
    scapy.sniff(iface=interface, store=False, prn=process_sniffed_packet)
    
    
def process_sniffed_packet(packet) -> None:
    '''Takes Packets and Prints it'''
    print(type(packet))
    # filtering a data from packets
    if packet.haslayer(http.HTTPRequest):
        if packet.haslayer(scapy.Raw):
            # printing a data from all layers.
            # print(packet.show()) 
            # printing a specific field from packet
            print(packet[scapy.Raw].load)
    
    
sniff("eth0")