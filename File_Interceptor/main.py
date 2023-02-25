import netfilterqueue
import scapy.all as scapy


ack_list = []

def process_packet(packet) -> None:
    '''Accepts a packets and print it'''
    # converting packets to scapy packets
    scapy_packet = scapy.IP(packet.get_payload())
    if scapy_packet.haslayer(scapy.Raw):
        # HTTP Request
        if scapy_packet[scapy.TCP].dport == 80: 
            if ".exe" in scapy_packet[scapy.Raw].load:
                print("[+] exe Request")
                ack_list.append(scapy_packet[scapy.TCP].ack)    
                print(scapy_packet.show())
        # HTTP Response
        elif scapy_packet[scapy.TCP].sport == 80:
            if scapy_packet[scapy.TCP].seq in ack_list:
                ack_list.remove(scapy_packet[scapy.TCP].seq)
                print("[+] Replacing file")
                print(scapy_packet.show())

    packet.accept() # To accept packet and forward it to destination
    # packet.drop() # To accept packet and drop it


queue = netfilterqueue.NetfilterQueue() # initiating a object
queue.bind(0, process_packet) # binding a queue of iptable here 0 is the queue number
queue.run() # running a queue of iptable