import scapy.all as scapy
import argparse


def get_arguments() -> argparse.Namespace:
    '''captures and returns the arguments passed by the user'''
    # initizing object for taking input through argument
    parser = argparse.ArgumentParser()
    # options for user input through arguments
    parser.add_argument("-t", "--target", dest="target", help="Target IP / IP Range.")
    options = parser.parse_args()
    if not options.target: # validating user input contains target IP or not
        parser.error("[-] Please specify an Target IP / IP Range, use --help for more info.")

    return options


def scan(ip: str) -> list:
    '''accepts a IP address or IP range and creates a arp packet'''
    arp_request = scapy.ARP(pdst=ip) # creating a arp packet with dest ip
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff") # adding a dest MAC addr to arp packet
    arp_request_broadcast = broadcast/arp_request # combining both dest ip and dest Mac addr
    answered_list = scapy.srp(arp_request_broadcast, timeout=1, verbose=False)[0] # broadcasting arp packet and capturing a results
    
    clients_list = []
    for element in answered_list:
        # storing responded vm ip addr and mac addr in dictionary
        client_dict = { "ip": element[1].psrc, "mac": element[1].hwsrc }
        clients_list.append(client_dict)
    
    return clients_list
    
    # arp_request_broadcast.show() # to show to details
    # print(arp_request.summary()) # printing a summary of message
    # scapy.ls(scapy.ARP()) # To list all the Function of scapy.ARP() class
    

def print_result(results_list: list) -> None:
    '''prints a all the scan results'''
    print("IP\t\t\tMAC Address\n-------------------")
    
    for client in results_list:
        print(client["ip"] + "\t\t" + client["mac"])
    
    
options = get_arguments()
scan_result = scan(options.target)
print_result(scan_result)
