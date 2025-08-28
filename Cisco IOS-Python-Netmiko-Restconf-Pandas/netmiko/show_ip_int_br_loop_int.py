"""Get 'show ip interface brief' from devices 10.254.0.1-3 using integer loop."""
from netmiko import ConnectHandler

IP_PREFIX = "10.254.0."
USERNAME = "cisco"
PASSWORD = "cisco"
DEVICE_TYPE = "cisco_ios"
PORT = 22

def get_ip_int_br(ip: str) -> str:
    conn = ConnectHandler(ip=ip, device_type=DEVICE_TYPE,
                          username=USERNAME, password=PASSWORD, port=PORT)
    return conn.send_command("show ip interface brief | exclude unassigned")

def main():
    last_octet = 1
    while last_octet <= 3:
        ip = f"{IP_PREFIX}{last_octet}"
        output = get_ip_int_br(ip)
        print(output)
        print("_"*80)
        last_octet += 1

if __name__ == "__main__":
    main()
