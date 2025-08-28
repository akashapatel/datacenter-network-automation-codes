"""Demo using float math to iterate IPs (for teaching purposes only)."""
from netmiko import ConnectHandler

IP_BASE = "10.254."
USERNAME = "cisco"
PASSWORD = "cisco"
DEVICE_TYPE = "cisco_ios"
PORT = 22

def get_ip_int_br(ip: str) -> str:
    conn = ConnectHandler(ip=ip, device_type=DEVICE_TYPE,
                          username=USERNAME, password=PASSWORD, port=PORT)
    return conn.send_command("show ip interface brief")

def main():
    ip_end = 0.1
    while ip_end <= 0.3:
        ip = IP_BASE + str(ip_end)
        output = get_ip_int_br(ip)
        print(output)
        print("IP int from", ip)
        print("_"*80)
        ip_end = round(ip_end + 0.1, 2)

if __name__ == "__main__":
    main()
