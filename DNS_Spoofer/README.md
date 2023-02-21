# To Create a packets queue
`iptables -I FORWARD -j NFQUEUE --queue-num 0` # -I flag is for edit table --queue-num for to identify the queue

# To delete a ip tables
`iptables --flush`

# to create packets queue for localhost machine
for out going packets: `iptables -I OUTPUT -j NFQUEUE --queue-num 0`
for incoming packets: `iptables -I INPUT -j NFQUEUE --queue-num 0`

# full forms
`DNSQR = DNS Question Record`
`DNSRR = DNS Resource Record`