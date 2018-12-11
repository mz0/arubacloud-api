#!/usr/bin/python3

from ArubaCloud.PyArubaAPI import CloudInterface
from ArubaCloud.objects.VmTypes import Smart, Pro
from ArubaCloud.ReverseDns import ReverseDns
from pprint import pprint

myId=''
myPw=''

# hypervisors:
#   1 -> Microsoft Hyper-V          - Cloud Pro
#   2 -> VMWare                     - Cloud Pro
#   3 -> Microsoft Hyper-V Low Cost - Cloud Pro
#   4 -> VMWare                   - Cloud Smart

# DCs:
# 1 -> DC1 -> Italy 1
# 2 -> DC2 -> Italy 2
# 3 -> DC3 -> Czech Republic
# 4 -> DC4 -> France
# 5 -> DC5 -> Germany
# 6 -> DC6 -> UK
# 7 -> DC7 -> Italy 3
# 8 -> DC8 -> Poland

#pprint(ci.find_template(name='Debian', hv=4, debug=False))


def ptr(jptr):
  if isinstance(jptr, list) and len(jptr)==1 and isinstance(jptr[0], dict) and ('Hosts' in jptr[0]) and \
   len(jptr[0]['Hosts']) > 0 and isinstance(jptr[0]['Hosts'], list) and len(jptr[0]['Hosts']) > 0:
    return jptr[0]['Hosts'][0]
  else:
    return '--'

    
for dc in [1,5,6]:
#for dc in [3]:
    ci = CloudInterface(dc=dc)
    ci.login(username=myId, password=myPw, load=False)
    ci.get_servers(debug=False)
    for vm in ci.vmlist:
        ip = ''
        if isinstance(vm, Smart):
            ip = vm.ip_addr
            rdns = ReverseDns.ReverseDns(username=myId, password=myPw, ws_uri=ci.wcf_baseurl)
            jptr = rdns.get(addresses=[ip])
            print("DC{} vm-name: {} \tIP {}\tPTR {}\t ServerID {} Status:{}".format(dc, vm.vm_name, ip, ptr(jptr),vm.sid,vm.status))
            if vm.ip_addr=='80.211.223.223' and vm.status==2:
                print("Ready to kill")
                ci.delete_vm(server_id=vm.sid)
            if vm.ip_addr == '212.237.9.140':
                #print(rdns.set(address=ip, host_name=['La.x302.net']))
                pass
        elif isinstance(vm, Pro):
            print("unexpected!")
            # for ip in vm.ip_addr: print(" IP: {}".format(ip.ip_addr))

#DC1 vm-name: La 	IP 11.237.9.140  PTR La.x302.net ServerID 29265
#DC3 vm-name: cz2 	IP 10.211.23.223 PTR --
#DC5 vm-name: de1 	IP 16.105.53.6   PTR fe.x302.net ServerID 29252
#DC6 vm-name: uk1 	IP 14.177.25.25  PTR li.x302.net ServerID 24842
