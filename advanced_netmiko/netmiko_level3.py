from netmiko import ConnectHandler

with open('device_list') as f:
    device_list=f.read().splitlines()

with open('commands_file') as f:
    commands_to_send=f.read().splitlines()

for ip in device_list:
    print('Connecting to ' + ip)
    device = {
        'device_type': 'cisco_ios',
        'ip': ip,
        'username': 'aslan',
        'password': 'cisco'
    }
    net_connect = ConnectHandler(**device)
    output=net_connect.send_config_set(commands_to_send)
    print(output)