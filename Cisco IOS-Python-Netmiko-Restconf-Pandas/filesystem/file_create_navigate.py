import os
from netmiko import ConnectHandler

class CiscoIOS:
    def __init__(self, ip, port=22, username=None, password=None, device_type="cisco_ios"):
        self.conn = ConnectHandler(ip=ip, port=port, username=username, password=password, device_type=device_type)
        self.hostname = self.conn.send_command("show run | include hostname").split()[-1]

    def get_run_cfg(self):
        return self.conn.send_command("show run")

    def get_ip_int(self):
        return self.conn.send_command("show ip int")

    def get_log(self):
        return self.conn.send_command("show log")

def main():
    ip_list = ["10.254.0.1", "10.254.0.2", "10.254.0.3"]
    routers = [CiscoIOS(ip, username="cisco", password="cisco") for ip in ip_list]

    base_dir = os.path.join(os.getcwd(), "routers")
    os.makedirs(base_dir, exist_ok=True)

    for r in routers:
        router_dir = os.path.join(base_dir, r.hostname)
        os.makedirs(router_dir, exist_ok=True)
        data = {
            "running-config": r.get_run_cfg(),
            "ip-interface": r.get_ip_int(),
            "log": r.get_log(),
        }
        for name, content in data.items():
            with open(os.path.join(router_dir, f"{name}.txt"), "w") as f:
                f.write(content)

    for root, dirs, files in os.walk("routers"):
        print(root, dirs, files)

if __name__ == "__main__":
    main()
