"""Get 'show log' from three devices defined as strings."""
from netmiko import ConnectHandler

DEVICES = ["10.254.0.1", "10.254.0.2", "10.254.0.3"]
USERNAME = "cisco"
PASSWORD = "cisco"
DEVICE_TYPE = "cisco_ios"
PORT = 22

def get_log(ip: str) -> str:
    conn = ConnectHandler(ip=ip, device_type=DEVICE_TYPE,
                          username=USERNAME, password=PASSWORD, port=PORT)
    return conn.send_command("show log")

def main():
    for ip in DEVICES:
        print(get_log(ip))

if __name__ == "__main__":
    main()
