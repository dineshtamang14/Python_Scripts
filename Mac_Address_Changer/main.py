import subprocess
import optparse
import re


def get_arguments() -> optparse.Values:
    # initizing object for taking input through argument
    parser = optparse.OptionParser()
    # options for user input through arguments
    parser.add_option("-i", "--interface", dest="interface", help="interface to change its MAC address") # adding a option of interface
    parser.add_option("-m", "--mac", dest="new_mac", help="New MAC address") # adding a option of new_mac

    # understand user input arguments
    (options, arguments) = parser.parse_args()
    if not options.interface: # validating user input contains interface or not
        parser.error("[-] Please specify an interface, use --help for more info.")
    elif not options.new_mac: # validating user input contains new_mac or not
        parser.error("[-] Please specify a new mac, use --help for more info.")
    return options


def change_mac(interface: str, new_mac_addr: str)-> None:
    print(f"[+] Changing MAC address for {interface} to {new_mac_addr}")
    subprocess.call(["ifconfig", interface, "down"]) # executing a linux command to bring interface down
    subprocess.call(["ifconfig", interface, "hw", "ether", new_mac_addr]) # executing linux command to change mac addr
    subprocess.call(["ifconfig", interface, "up"]) # executing linux command to bring interface up

def get_current_mac(interface: str)-> str:
    # executing linux command to get interface info
    ifconfig_result = subprocess.check_output(["ifconfig", interface]) 
    # filtering linux command output using regex to return only mac address
    mac_address_search_result = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", str(ifconfig_result)) 

    if mac_address_search_result: # validating up code result
        return mac_address_search_result.group(0)
    else:
        print("[-] Could not read MAC address.")


options = get_arguments()

current_mac = get_current_mac(options.interface)
print(f"Current MAC = {str(current_mac)}")
change_mac(options.interface, options.new_mac)


current_mac = get_current_mac(options.interface)
if current_mac == options.new_mac:
    print(f"[+] MAC address was successfully changed to {current_mac}")
else:
    print(f"[-] MAC address did not get changed.")