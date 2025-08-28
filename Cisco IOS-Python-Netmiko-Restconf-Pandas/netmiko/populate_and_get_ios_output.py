from netmiko import ConnectHandler

def populate_ip_list(ip_base: str, ip_range) -> list:
    return [f"{ip_base}{n}" for n in ip_range]

def get_ios_output(ip_list, command):
    for ip in ip_list:
        conn = ConnectHandler(ip=ip, device_type="cisco_ios", username="cisco", password="cisco", port=22)
        print(conn.send_command(command))

if __name__ == "__main__":
    ips = populate_ip_list("10.254.0.", range(1, 4))
    get_ios_output(ips, "show ip int br")
