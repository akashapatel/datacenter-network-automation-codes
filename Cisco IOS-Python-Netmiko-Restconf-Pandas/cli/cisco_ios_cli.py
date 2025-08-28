import argparse
from getpass import getpass
from netmiko import ConnectHandler
import pandas as pd

class CiscoIOS:
    def __init__(self, ip, port=22, prompt=False, username=None, password=None, device_type="cisco_ios"):
        if prompt:
            username = input("Username: ")
            password = getpass()
        self.conn = ConnectHandler(ip=ip, port=port, username=username, password=password, device_type=device_type)
        self.hostname = self.conn.send_command("show run | include hostname").split()[-1]

    def get_interface_list(self):
        ip_int_br = self.conn.send_command("show ip int br", use_textfsm=True)
        df = pd.DataFrame(ip_int_br)
        return df["intf"].to_list()

    def get_run_int(self):
        section = input("Interface: ")
        if section in self.get_interface_list():
            return self.conn.send_command("show run | section " + section)
        return "Error - Invalid interface name."

class CiscoIOS_CLI(CiscoIOS):
    def __init__(self):
        parser = argparse.ArgumentParser()
        parser.add_argument("ip", type=str, help="IP address, SSH endpoint")
        parser.add_argument("--port", type=int, default=22, help="Port for connection")
        parser.add_argument("-u", "--username", type=str, help="Username for SSH connection")
        parser.add_argument("-p", "--password", type=str, help="Password for SSH connection")
        parser.add_argument("--device_type", type=str, default="cisco_ios", help="Device type of appliance")
        args = parser.parse_args()
        super().__init__(args.ip, port=args.port, username=args.username, password=args.password,
                         device_type=args.device_type)
        print(self.conn.send_command("show run | include hostname"))

def main():
    cli = CiscoIOS_CLI()
    print(cli.get_interface_list())

if __name__ == "__main__":
    main()
