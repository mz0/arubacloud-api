#!/usr/bin/python3

from ArubaCloud.PyArubaAPI import CloudInterface
from ArubaCloud.objects import SmartVmCreator
from pprint import pprint
import time
import logging

try:
    from ConfigParser import ConfigParser as iniParser
except ModuleNotFoundError:
    from configparser import ConfigParser as iniParser

inifile = iniParser()
inifile.read("/home/mz0/.ssh/aruba/ansible.ini")
myId = inifile.get("acct0", "user")
myPw = inifile.get("acct0", "passwd")

tmp_root_passwd = 'hjgkhg_bkhjgbkhgb'
# template = 'debian8_x64_1_0'
vmname = 'La'
dc = 1

i = CloudInterface(dc=dc, debug_level=logging.DEBUG)
i.login(username=myId, password=myPw, load=False)

vm = i.get_vm(pattern=vmname)[0]
print('Reinitialize: %s' % vm.vm_name)
if vm.status == 3:
        vm.poweroff()
while len(i.get_jobs()['Value']) > 0:
        time.sleep(1)
vm.reinitialize(admin_password=tmp_root_passwd)

# 2018-12-10 15:19 MainThread DEBUG
