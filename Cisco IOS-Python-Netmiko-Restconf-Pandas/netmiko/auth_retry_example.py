from getpass import getpass
from netmiko import ConnectHandler
from netmiko.ssh_exception import NetmikoAuthenticationException

def main():
    ip = "10.254.0.1"
    username = "wrong_username"
    password = "wrong_password"
    device_type = "cisco_ios"

    try:
        conn = ConnectHandler(ip=ip, username=username, password=password, device_type=device_type)
    except NetmikoAuthenticationException:
        print("Authentication Failed")
        username = input("Enter Username: ")
        password = getpass("Enter Password: ")
        conn = ConnectHandler(ip=ip, username=username, password=password, device_type=device_type)

    print(conn.send_command("show ip int br"))

if __name__ == "__main__":
    main()
