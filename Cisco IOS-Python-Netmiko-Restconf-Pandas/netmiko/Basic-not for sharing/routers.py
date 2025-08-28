"""Minimal helper used by show_ip_int_br_for_loop.py"""
from netmiko import ConnectHandler

creds = [
    {"ip": "10.254.0.1", "username": "cisco", "password": "cisco", "device_type": "cisco_ios"},
    {"ip": "10.254.0.2", "username": "cisco", "password": "cisco", "device_type": "cisco_ios"},
    {"ip": "10.254.0.3", "username": "cisco", "password": "cisco", "device_type": "cisco_ios"},
]

def get_ip_int_br(ip, username, password, device_type):
    conn = ConnectHandler(ip=ip, username=username, password=password, device_type=device_type)
    return conn.send_command("show ip int brief")
