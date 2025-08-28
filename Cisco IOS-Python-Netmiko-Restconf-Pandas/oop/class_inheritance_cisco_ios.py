from netmiko import ConnectHandler

class Cisco:
    def __init__(self, ip, device_type=None, username=None, password=None):
        self.conn_data = {"ip": ip, "device_type": device_type, "username": username, "password": password}
    def login(self):
        return ConnectHandler(**self.conn_data)

class CiscoIOS(Cisco):
    def __init__(self, ip, username=None, password=None):
        super().__init__(ip, device_type="cisco_ios", username=username or "cisco", password=password or "cisco")
    def populate_interface_list(self):
        conn = self.login()
        sh_ip_int_br = conn.send_command("show ip int br", use_textfsm=True)
        self.interface_list = [row["intf"] for row in sh_ip_int_br]

if __name__ == "__main__":
    csr1kv1 = CiscoIOS("10.254.0.1")
    csr1kv1.populate_interface_list()
    print(csr1kv1.interface_list)
