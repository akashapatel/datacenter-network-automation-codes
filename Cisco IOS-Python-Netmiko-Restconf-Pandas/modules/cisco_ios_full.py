import sys
import pandas as pd
from getpass import getpass
from netmiko import ConnectHandler
from netmiko.ssh_exception import NetmikoAuthenticationException, NetmikoTimeoutException

class CiscoIOS:
    def __init__(self, ip, port=22, username=None, password=None, device_type="cisco_ios"):
        self.ip, self.port, self.username, self.password, self.device_type = ip, port, username, password, device_type
        try:
            self.conn = self.connect()
        except NetmikoAuthenticationException:
            print("Authentication Failed.")
            self.username = input("Enter username: ")
            self.password = getpass("Enter password: ")
            self.conn = self.connect()
        except NetmikoTimeoutException:
            print("\n*** SSH Timeout ***\nEnsure you are using the correct connection information.\n")
            sys.exit(1)
        self.hostname = self.conn.send_command("show run | include hostname").split()[-1]

    def connect(self):
        return ConnectHandler(ip=self.ip, port=self.port, username=self.username,
                              password=self.password, device_type=self.device_type)

    def get_interface_names(self):
        ip_int_br = self.conn.send_command("show ip int br", use_textfsm=True)
        df = pd.DataFrame(ip_int_br)
        return df["intf"].to_list()

    def get_ip_int_br(self):
        return self.conn.send_command("show ip int br")

    def get_ip_arp(self, as_dataframe=False):
        if as_dataframe:
            ip_arp = self.conn.send_command("show ip arp", use_textfsm=True)
            return pd.DataFrame(ip_arp)
        return self.conn.send_command("show ip arp")

    def get_interface_IPs(self):
        df = self.get_ip_arp(as_dataframe=True)
        return {iface: df['address'].loc[df['interface'] == iface].to_list() for iface in df['interface'].unique()}

    def get_interface_MACs(self):
        df = self.get_ip_arp(as_dataframe=True)
        return {iface: df['mac'].loc[df['interface'] == iface].to_list() for iface in df['interface'].unique()}

    def get_ip_route(self, connected=False):
        return self.conn.send_command("show ip route connected" if connected else "show ip route")

    def get_run_cfg(self, include=""):
        return self.conn.send_command("show run | " + include if include else "show run")

    def commit_changes(self):
        return self.conn.send_command("copy running-config startup-config")

def main():
    csr = CiscoIOS("10.254.0.1", username="cisco", password="cisco")
    print(csr.get_ip_arp())

if __name__ == "__main__":
    main()
