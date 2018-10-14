from netmiko import ConnectHandler

iosv_l2_s4 = {
    'device_type': 'cisco_ios',
    'ip':'192.168.122.84',
    'username':'aslan',
    'password':'cisco',
}

iosv_l2_s5 = {
    'device_type': 'cisco_ios',
    'ip':'192.168.122.85',
    'username':'aslan',
    'password':'cisco',
}

iosv_l2_s6 = {
    'device_type': 'cisco_ios',
    'ip':'192.168.122.86',
    'username':'aslan',
    'password':'cisco',
}

with open('configuration.txt') as f:
    lines=f.read().splitlines()
print(lines)

all_devices=[iosv_l2_s4,iosv_l2_s5,iosv_l2_s6]

for devices in all_devices:
    net_connect = ConnectHandler(**devices)
    output = net_connect.send_config_set(lines)
    print(output)