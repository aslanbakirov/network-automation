from netmiko import ConnectHandler
from getpass import getpass
from netmiko.ssh_exception import AuthenticationException
from paramiko.ssh_exception import SSHException
from netmiko.ssh_exception import NetMikoTimeoutException


username=input('Enter your ssh username: ')
password=getpass()

with open('device_list') as f:
    device_list=f.read().splitlines()

with open('commands_file') as f:
    commands_to_send=f.read().splitlines()

for ip in device_list:
    print('Connecting to ' + ip)
    device = {
        'device_type': 'cisco_ios',
        'ip': ip,
        'username': str(username),
        'password': str(password)
    }
    try:
        net_connect = ConnectHandler(**device)
    except (AuthenticationException):
        print('Authentication failure: ' + ip)
        continue
    except (NetMikoTimeoutException):
        print('Timeout to device: ' + ip)
        continue
    except (EOFError):
        print('End of file while attempting device ' + ip)
        continue
    except (SSHException):
        print('SSH Issue. Are you sure SSH is enabled? ' + ip)
        continue
    except Exception as unknown_error:
        print('Some other error: ' + str(unknown_error))
        continue

    output=net_connect.send_config_set(commands_to_send)
    print(output)