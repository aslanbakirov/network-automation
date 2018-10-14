from netmiko import ConnectHandler

iosv_l2_s1 = {
    'device_type': 'cisco_ios',
    'ip':'192.168.122.72',
    'username':'aslan',
    'password':'cisco',
}

iosv_l2_s2 = {
    'device_type': 'cisco_ios',
    'ip':'192.168.122.82',
    'username':'aslan',
    'password':'cisco',
}

iosv_l2_s3 = {
    'device_type': 'cisco_ios',
    'ip':'192.168.122.83',
    'username':'aslan',
    'password':'cisco',
}

all_devices=[iosv_l2_s1,iosv_l2_s2,iosv_l2_s3]

net_connect=ConnectHandler(**iosv_l2)
output= net_connect.send_command('show ip int br')
print (output)

config_commands = ['int loop 0','ip address 1.1.1.1 255.255.255.0']
output = net_connect.send_config_set(config_commands)
print(output)

for devices in all_devices:
    net_connect = ConnectHandler(**devices)
    output = net_connect.send_command('show ip int br')
    print(output)

    config_commands = ['int loop 0', 'ip address 1.1.1.1 255.255.255.0']
    output = net_connect.send_config_set(config_commands)
    print(output)
    for n in range (2,21):
        print("Creating Vlan " + str(n))
        config_commands = ['vlan '+ str(n),'name Python_VLAN_'+str(n)]
        output = net_connect.send_config_set(config_commands)
        print(output)