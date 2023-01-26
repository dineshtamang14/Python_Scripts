import scapy.all as scapy


def scan(ip: str) -> None:
    arp_request = scapy.ARP(pdst=ip, psrc="192.168.12.104")
    print(arp_request.summary())
    
    # To list all the Function of scapy.ARP() class
    # scapy.ls(scapy.ARP())
    
    
scan('192.168.12.1')