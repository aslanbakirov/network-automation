from netmiko import ConnectHandler
from getpass import getpass
from netmiko.ssh_exception import AuthenticationException
from paramiko.ssh_exception import SSHException
from netmiko.ssh_exception import NetMikoTimeoutException


username=input('Enter your ssh username: ')
password=getpass()

with open('device_list') as f:
    device_list=f.read().splitlines()

with open('command_file_switch') as f:
    commands_to_switch=f.read().splitlines()

with open('command_file_router') as f:
    commands_to_router=f.read().splitlines()


list_versions=[
    'vios_l2-ADVENTERPRISEK9-M',
    'C3745-ADVIPSERVICESK9-M'
]

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

    for v in list_versions:
        print('Checking for version:'+v)
        output_version=net_connect.send_command('show version')
        int_version=0
        int_version=output_version.find(v)
        if int_version>0:
            print('Software Version found:'+ v)
            break
        else:
            print('Did not find version')

    if v=='vios_l2-ADVENTERPRISEK9-M':
        print('Sending command to the switch')
        output=net_connect.send_config_set(commands_to_switch)
    elif v == 'C3745-ADVIPSERVICESK9-M':
        print('Sending command to the router')
        output = net_connect.send_config_set(commands_to_router)

    print(output)