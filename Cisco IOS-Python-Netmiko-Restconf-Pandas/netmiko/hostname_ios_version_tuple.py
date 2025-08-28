"""Collect hostname and IOS XE version as tuples."""
from netmiko import ConnectHandler
import pprint

USERNAME = "cisco"
PASSWORD = "cisco"
DEVICE_TYPE = "cisco_ios"
PORT = 22
IPS = ("10.254.0.1", "10.254.0.2", "10.254.0.3")

def main():
    result_list = []
    for ip in IPS:
        conn = ConnectHandler(ip=ip, device_type=DEVICE_TYPE,
                              username=USERNAME, password=PASSWORD, port=PORT)
        hostname = conn.send_command("show run | include hostname").strip()
        ios_xe_version = conn.send_command("show version | section Cisco IOS XE Software, Version").strip()
        result_list.append((hostname, ios_xe_version))
    pprint.pprint(result_list)

if __name__ == "__main__":
    main()
