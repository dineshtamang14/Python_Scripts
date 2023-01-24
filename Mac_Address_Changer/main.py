import subprocess
import optparse


def change_mac(interface: str, new_mac_addr: str)-> None:
    print(f"[+] Changing MAC address for {interface} to {new_mac_addr}")
    subprocess.call(["ifconfig", interface, "down"])
    subprocess.call(["ifconfig", interface, "hw", "ether", new_mac_addr])
    subprocess.call(["ifconfig", interface, "up"])


# initizing object for taking input through argument
parser = optparse.OptionParser()
# options for user input through arguments
parser.add_option("-i", "--interface", dest="interface", help="interface to change its MAC address")
parser.add_option("-m", "--mac", dest="new_mac", help="New MAC address")

# understand user input arguments
(options, arguments) = parser.parse_args()

change_mac(options.interface, options.new_mac)