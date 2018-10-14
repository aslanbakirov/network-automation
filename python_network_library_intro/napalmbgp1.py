import json
from napalm import get_network_driver

driver =get_network_driver('ios')
iosvl2=driver('192.168.122.32','aslan','cisco')
iosvl2.open()

ios_output=iosvl2.get_bgp_neighbors()
print(json.dumps(ios_output, indent=4))

iosvl2.close()
