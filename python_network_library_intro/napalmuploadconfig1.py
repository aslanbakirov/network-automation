import json
from napalm import get_network_driver

driver =get_network_driver('ios')
iosvl2=driver('192.168.122.32','aslan','cisco')
iosvl2.open()

ios_output=iosvl2.load_merge_candidate(filename='acl1.cfg')

diffs=iosvl2.compare_config()

if len(diffs)>0:
    print(diffs)
    iosvl2.commit_config()
else:
    print('no differece')
    iosvl2.discard_config()

iosvl2.close()
