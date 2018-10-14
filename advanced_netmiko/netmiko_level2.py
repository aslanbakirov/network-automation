from netmiko import ConnectHandler

with open('commands_file') as f:
    commands_to_send=f.read().splitlines()

iosv_l2_s1 = {
    'device_type':'cisco_ios',
    'ip':'192.168.122.32',
    'username':'aslan',
    'password':'cisco'
}

alldevices=[iosv_l2_s1]

for devices in alldevices:
    net_connect = ConnectHandler(**iosv_l2_s1)
    output=net_connect.send_config_set(commands_to_send)
    print(output)