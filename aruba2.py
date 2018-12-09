#!/usr/bin/python3

from ArubaCloud.PyArubaAPI import CloudInterface
from pprint import pprint

myId='AWI-71331'
myPw=''

ci = CloudInterface(dc=1)
ci.login(username=myId, password=myPw, load=False)
# hypervisors:
#   1 -> Microsoft Hyper-V - Cloud Pro
#   2 -> VMWare - Cloud Pro
#   3 -> Microsoft Hyper-V Low Cost - Cloud Pro
#   4 -> VMWare - Cloud Smart

pprint(ci.find_template(hv=4))
