"""Filter output by a boolean check and membership in a list."""
from netmiko import ConnectHandler

CHECK_LIST = ["10.254.0.2"]
USERNAME = "cisco"
PASSWORD = "cisco"
DEVICE_TYPE = "cisco_ios"
PORT = 22

def get_ip_int_br(ip: str) -> str:
    conn = ConnectHandler(ip=ip, device_type=DEVICE_TYPE,
                          username=USERNAME, password=PASSWORD, port=PORT)
    return conn.send_command("show ip interface brief")

def main():
    prefix = "10.254.0."
    last = 1
    while last <= 3:
        ip = prefix + str(last)
        output = get_ip_int_br(ip)
        contains_text = len(output) > 0
        if ip in CHECK_LIST and contains_text:
            print("IP interface from", ip)
            print(output)
            print("-"*80)
        last += 1

if __name__ == "__main__":
    main()
