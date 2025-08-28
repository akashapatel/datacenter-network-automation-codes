import re
from netmiko import ConnectHandler
from parsing.change_mac_notation import change_notation

def main():
    conn = ConnectHandler(ip="10.254.0.1", device_type="cisco_ios", username="cisco", password="cisco", port=22)
    show_arp = conn.send_command("show arp")
    macs = re.findall(r"((?:[0-9a-f]{4}\.){2}[0-9a-f]{4})", show_arp, flags=re.I)
    if macs:
        print(change_notation(macs[0], ":"))

if __name__ == "__main__":
    main()
