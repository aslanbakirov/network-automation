from simplecrypt import decrypt
from pprint import pprint
from netmiko import ConnectHandler
import json
from time import time

from multiprocessing.dummy import Pool as ThreadPool


# ------------------------------------------------------------------------------
def read_devices(devices_filename):
    devices = {}  # create our dictionary for storing devices and their info

    with open(devices_filename) as devices_file:
        for device_line in devices_file:
            device_info = device_line.strip().split(',')  # extract device info from line

            device = {'ipaddr': device_info[0],
                      'type': device_info[1],
                      'name': device_info[2]}  # create dictionary of device objects ...

            devices[device['ipaddr']] = device  # store our device in the devices dictionary
            # note the key for devices dictionary entries is ipaddr

    print('\n----- devices --------------------------')
    pprint(devices)

    return devices


# ------------------------------------------------------------------------------
def read_device_creds(device_creds_filename, key):
    print('\n... getting credentials ...\n')
    with open(device_creds_filename, 'rb') as device_creds_file:
        device_creds_json = decrypt(key, device_creds_file.read())

    device_creds_list = json.loads(device_creds_json.decode('utf-8'))

    print('\n----- device_creds ----------------------')

    # convert to dictionary of lists using dictionary comprehension
    device_creds = {dev[0]: dev for dev in device_creds_list}
    pprint(device_creds)

    return device_creds


# ------------------------------------------------------------------------------
def config_worker(device_and_creds):
    # For threadpool library we had to pass only one argument, so extract the two
    # pieces (device and creds) out of the one tuple passed.
    device = device_and_creds[0]
    creds = device_and_creds[1]

    # ---- Connect to the device ----
    if device['type'] == 'junos-srx':
        device_type = 'juniper'
    elif device['type'] == 'cisco-ios':
        device_type = 'cisco_ios'
    elif device['type'] == 'cisco-xr':
        device_type = 'cisco_xr'
    else:
        device_type = 'cisco_ios'  # attempt Cisco IOS as default

    print('---- Connecting to device {0}, username={1}, password={2}'.format(device['ipaddr'],
                                                                             creds[1], creds[2]))

    # ---- Connect to the device
    session = ConnectHandler(device_type=device_type, ip=device['ipaddr'],
                             username=creds[1], password=creds[2])
    # session = ConnectHandler( device_type=device_type, ip='172.16.0.1',  # Faking out IP address for now
    #                                                   username=creds[1], password=creds[2] )

    if device_type == 'juniper':
        # ---- Use CLI command to get configuration data from device
        print('---- Getting configuration from device')
        session.send_command('configure terminal')
        config_data = session.send_command('show configuration')

    if device_type == 'cisco_ios':
        # ---- Use CLI command to get configuration data from device
        print('---- Getting configuration from device')
        config_data = session.send_command('show run')

    if device_type == 'cisco_xr':
        # ---- Use CLI command to get configuration data from device
        print('---- Getting configuration from device')
        config_data = session.send_command('show configuration running-config')

    # ---- Write out configuration information to file
    config_filename = 'config-' + device['ipaddr']  # Important - create unique configuration file name

    print('---- Writing configuration: ', config_filename)
    with open(config_filename, 'w') as config_out:
        config_out.write(config_data)

    session.disconnect()

    return


# ==============================================================================
# ---- Main: Get Configuration
# ==============================================================================

devices = read_devices('device-file')
creds = read_device_creds('encrypted-device-creds', 'cisco')

num_threads_str = input('\nNumber of threads (5): ') or '5'
num_threads = int(num_threads_str)

# ---- Create list for passing to config worker
config_params_list = []
for ipaddr, device in devices.items():
    config_params_list.append((device, creds[ipaddr]))

starting_time = time()

print('\n--- Creating threadpool, launching get config threads\n')
threads = ThreadPool(num_threads)
results = threads.map(config_worker, config_params_list)

threads.close()
threads.join()

print('\n---- End get config threadpool, elapsed time=', time() - starting_time)