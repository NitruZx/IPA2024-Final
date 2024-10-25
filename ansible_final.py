import subprocess

def showrun():
    # read https://www.datacamp.com/tutorial/python-subprocess to learn more about subprocess
    command = ['ansible-playbook', 'backup_cisco_router_playbook.yaml']
    result = subprocess.run(command, capture_output=True, text=True)
    result = result.stdout
    if 'ok=2' in result:
        return result
    else:
        return result
