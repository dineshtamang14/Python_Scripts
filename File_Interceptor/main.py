import netfilterqueue
import scapy.all as scapy


def process_packet(packet) -> None:
    '''Accepts a packets and print it'''
    # converting packets to scapy packets
    scapy_packet = scapy.IP(packet.get_payload())
    if scapy_packet.haslayer(scapy.Raw):
        if scapy_packet[scapy.TCP].dport == 80:
            print("HTTP Request")
            print(scapy_packet.show())
        elif scapy_packet[scapy.TCP].sport == 80:
            print("HTTP Response")
            print(scapy_packet.show())

    packet.accept() # To accept packet and forward it to destination
    # packet.drop() # To accept packet and drop it


queue = netfilterqueue.NetfilterQueue() # initiating a object
queue.bind(0, process_packet) # binding a queue of iptable here 0 is the queue number
queue.run() # running a queue of iptable