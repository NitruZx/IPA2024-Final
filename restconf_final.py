import json
import requests
requests.packages.urllib3.disable_warnings()

# Router IP Address is 10.0.15.181-184
std_id = "65070041"
host = "10.0.15.181"
api_url = f"https://{host}/restconf/data/ietf-interfaces:interfaces/interface=Loopback{std_id}"

# the RESTCONF HTTP headers, including the Accept and Content-Type
# Two YANG data formats (JSON and XML) work with RESTCONF 
headers = {
    "Accept": "application/yang-data+json",
    "Content-Type": "application/yang-data+json"
}
basicauth = ("admin", "cisco")


def create():
    yangConfig = {
    "ietf-interfaces:interface": {
        "name": f"Loopback{std_id}",
        "type": "iana-if-type:softwareLoopback",
        "enabled": True,
        "ietf-ip:ipv4": {
            "address": [
                {
                    "ip": f"172.30.{std_id[-2:]}.1",
                    "netmask": "255.255.255.0"
                }
            ]
        },
        "ietf-ip:ipv6": {}
    }
} 

    resp = requests.put(
        api_url, 
        data=json.dumps(yangConfig), 
        auth=basicauth, 
        headers=headers, 
        verify=False
        )

    if(resp.status_code >= 200 and resp.status_code <= 299):
        print("STATUS OK: {}".format(resp.status_code))
        if(resp.status_code == 204):
            return f"Cannot create: Interface loopback {std_id}"
        return f"Interface loopback {std_id} is created successfully"
    else:
        print('Error. Status Code: {}'.format(resp.status_code))
        return f"Failed to create: Interface loopback {std_id}"


def delete():
    resp = requests.delete(
        api_url, 
        auth=basicauth, 
        headers=headers, 
        verify=False
        )

    if(resp.status_code >= 200 and resp.status_code <= 299):
        print("STATUS OK: {}".format(resp.status_code))
        return f"Interface loopback {std_id} is deleted successfully"
    else:
        print('Error. Status Code: {}'.format(resp.status_code))
        return f"Cannot delete: Interface loopback {std_id}"


def enable():
    yangConfig = {
    "ietf-interfaces:interface": {
        "name": f"Loopback{std_id}",
        "type": "iana-if-type:softwareLoopback",
        "enabled": True,
    }
}

    resp = requests.patch(
        api_url, 
        data=json.dumps(yangConfig), 
        auth=basicauth, 
        headers=headers, 
        verify=False
        )

    if(resp.status_code >= 200 and resp.status_code <= 299):
        print("STATUS OK: {}".format(resp.status_code))
        return f"Interface loopback {std_id} is enabled successfully"
    else:
        print('Error. Status Code: {}'.format(resp.status_code))
        return f"Cannot enable: Interface loopback {std_id}"


def disable():
    yangConfig = {
    "ietf-interfaces:interface": {
        "name": f"Loopback{std_id}",
        "type": "iana-if-type:softwareLoopback",
        "enabled": False,
    }}

    resp = requests.patch(
        api_url, 
        data=json.dumps(yangConfig), 
        auth=basicauth, 
        headers=headers, 
        verify=False
        )

    if(resp.status_code >= 200 and resp.status_code <= 299):
        print("STATUS OK: {}".format(resp.status_code))
        return f"Interface loopback {std_id} is shutdowned successfully"
    else:
        print('Error. Status Code: {}'.format(resp.status_code))
        return f"Cannot shutdown: Interface loopback {std_id}"


def status():
    api_url_status = f"https://{host}/restconf/data/ietf-interfaces:interfaces-state/interface=Loopback{std_id}"

    resp = requests.get(
        api_url_status, 
        auth=basicauth, 
        headers=headers, 
        verify=False
        )

    if(resp.status_code >= 200 and resp.status_code <= 299):
        print("STATUS OK: {}".format(resp.status_code))
        response_json = resp.json()
        admin_status = response_json["ietf-interfaces:interface"]["admin-status"]
        oper_status = response_json["ietf-interfaces:interface"]["oper-status"]
        if admin_status == 'up' and oper_status == 'up':
            return f"Interface loopback {std_id} is enabled"
        elif admin_status == 'down' and oper_status == 'down':
            return f"Interface loopback {std_id} is disabled"
    elif(resp.status_code == 404):
        print("STATUS NOT FOUND: {}".format(resp.status_code))
        return f"No Interface loopback {std_id}"
    else:
        print('Error. Status Code: {}'.format(resp.status_code))
        return f"Failed to get status from loopback {std_id}"
