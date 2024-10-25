from netmiko import ConnectHandler
from pprint import pprint

device_ip = "10.0.15.181"
username = "admin"
password = "cisco"

device_params = {
    "device_type": "cisco_xe",
    "ip": device_ip,
    "username": username,
    "password": password,
}


def gigabit_status():
    ans = ""
    with ConnectHandler(**device_params) as ssh:
        up = 0
        down = 0
        admin_down = 0
        result = ssh.send_command("sh ip int br", use_textfsm=True)
        print(result)
        for status in result:
            ans += f"{status['interface']} {status['status']}, "
            if status:
                if status["status"] == "up":
                    up += 1
                elif status["status"] == "down":
                    down += 1
                elif status["status"] == "administratively down":
                    admin_down += 1
        ans = ans[:-2] + f"-> {up} up, {down} down, {admin_down} administratively down"
        pprint(ans)
        return ans
