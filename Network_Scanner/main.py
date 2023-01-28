import scapy.all as scapy


def scan(ip: str) -> None:
    '''accepts a ip addr and creates a arp packet'''
    arp_request = scapy.ARP(pdst=ip) # creating a arp packet with dest ip
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff") # adding a dest MAC addr to arp packet
    arp_request_broadcast = broadcast/arp_request # combining both dest ip and dest Mac addr
    answered_list, unanswered_list = scapy.srp(arp_request_broadcast, timeout=1, verbose=False)[0] # broadcasting arp packet and capturing a results
    
    print("IP\t\t\tMAC Address\n-------------------")
    for element in answered_list:
        # printing responded vm ip addr and printing responded vm mac addr
        print(element[1].psrc + "\t\t" + element[1].hwsrc) 
    
    # arp_request_broadcast.show() # to show to details
    # print(arp_request.summary()) # printing a summary of message
    # scapy.ls(scapy.ARP()) # To list all the Function of scapy.ARP() class
    
    
scan('192.168.12.1')