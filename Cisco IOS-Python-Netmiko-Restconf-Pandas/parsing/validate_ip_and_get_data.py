import re
from netmiko import ConnectHandler

ip_pattern = re.compile(r"""(?:(?:25[0-5]|2[0-4][0-9]|1?[0-9]?[0-9])\.){3}(?:25[0-5]|2[0-4][0-9]|1?[0-9]?[0-9])""")

def validate_ip(s: str) -> bool:
    return bool(ip_pattern.fullmatch(s))

def connect(ip, username, password):
    assert validate_ip(ip), "Invalid IP address"
    return ConnectHandler(ip=ip, username=username, password=password, device_type="cisco_ios")

def get_data(conn, command):
    out = conn.send_command(command)
    assert "Invalid input" not in out, "Invalid command: " + command
    assert len(out) > 0, "No Output, check command: " + command
    return out

def main():
    conn = connect("10.254.0.1", "cisco", "cisco")
    print(get_data(conn, "show run | include hostname"))

if __name__ == "__main__":
    main()
