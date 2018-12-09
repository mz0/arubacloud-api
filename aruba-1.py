#!/usr/bin/python3

import requests
from pprint import pprint
import json
from datetime import datetime

try:
    from ConfigParser import ConfigParser as iniParser
except ModuleNotFoundError:
    from configparser import ConfigParser as iniParser

inifile = iniParser()
inifile.read("/home/mz0/.ssh/aruba/ansible.ini")
myId = inifile.get("acct0", "user")
myPw = inifile.get("acct0", "passwd")


def u(dc, cmd):
    return "https://api.dc{}.computing.cloud.it/WsEndUser/v2.9/WsEndUser.svc/json/{}".format(dc, cmd)


def c0(cmd):
    return '{{"ApplicationId":"{}","RequestId":"{}","SessionId":"{}","Password":"{}","Username":"{}"' \
           '}}'.format(cmd, cmd, cmd, myPw, myId)


def c1(cmd, server):
    """ GetServerDetails, SetEnqueueServerStart (powerOn), SetEnqueueServerPowerOff, SetEnqueueServerDeletion """
    return '{{"ApplicationId":"{}","RequestId":"{}","SessionId":"{}","Password":"{}","Username":"{}"' \
           ',"ServerId":{}}}'.format(cmd, cmd, cmd, myPw, myId, server)


def dns(ip, fqdn):
    cmd = "SetEnqueueSetReverseDns"
    return '{{"ApplicationId":"{}","RequestId":"{}","SessionId":"{}","Password":"{}","Username":"{}"' \
           ',"Hosts":["{}"],"IP":"{}"}}'.format(cmd, cmd, cmd, myPw, myId, fqdn, ip)


t_json = 'application/json'
h_ct = 'Content-Type'
h_cl = 'Content-Length'


def list_server(dc):
    server = 0
    cmd = "GetServers"
    data1 = c0(cmd=cmd)
    headers = {h_ct: t_json, h_cl: str(len(data1))}
    response = requests.post(u(dc, cmd), data=data1, headers=headers)
    if response.status_code == 200 and \
       h_ct in response.headers and \
       response.headers[h_ct] == t_json:
         re = response.content
    try:
        for jr in json.loads(re)['Value']:

            isSmart = jr['HypervisorType']==4
            name    = jr['Name']
            tpl     = jr['OSTemplateId']
            isBusy  = jr['Busy']
            powerOn = jr['ServerStatus']==3
            server  = jr['ServerId']
            cpu = jr['CPUQuantity']
            hdd = jr['HDTotalSize']
            ram = jr['RAMQuantity']
            print("{}cpu-{}GB-ssd{}GB  id {} name '{}' from template {}".format(cpu, ram, hdd, server, name, tpl))
            if isSmart and powerOn and not isBusy:
                print("is running")
    except Exception as e:
        print(e)

    cmd = "GetServerDetails"
    data2 = c1(cmd=cmd, server=server)
    headers = {h_ct: t_json, h_cl: str(len(data2))}
    response = requests.post(u(dc, cmd), data=data2, headers=headers)
    if response.status_code == 200:
        re = response.content
    try:
        jr = json.loads(re)
        print(jr['Value']['EasyCloudIPAddress']['Value'])
        n6s = jr['Value']['NetworkAdapters'][0]['IPAddresses'][0]['StartRangeIPv6']
        n6p = jr['Value']['NetworkAdapters'][0]['IPAddresses'][0]['PrefixIPv6']
        print(n6s)
        if n6p == 64:
            print(n6s[0:20]+":/"+str(n6p))  # ignore SubnetPrefixIPv6 -- Aruba truncates 2 hex digits
        else:
            print("Prefix:" + str(n6p))
        cdt = jr['Value']['CreationDate'][6:16]
        print("Created     @ {}".format(datetime.utcfromtimestamp(int(cdt))))
        rdt = jr['Value']['RenewDateSmart'][6:16]
        print("Next charge @ {}".format(datetime.utcfromtimestamp(int(rdt))))
    except Exception as e:
        print(e)


for dc in [1, 5, 6]: list_server(dc)


def templates(dc):
    cmd = 'GetHypervisors'
    data1 = c0(cmd=cmd)
    headers = {h_ct: t_json, h_cl: str(len(data1))}
    response = requests.post(u(dc, cmd), data=data1, headers=headers)
    if response.status_code == 200 and \
            h_ct in response.headers and \
            response.headers[h_ct] == t_json:
        re = response.content
    for templ in json.loads(re)['Value']:
        if templ['HypervisorType'] == 4:  # is Smart
            print("show|ipv6 |size|sshk|	Id | Name                  |Description")
            #      True|True|-MLX|False|	954|WS08-001_W2K8R2_X64_1_2|Windows 2008 R2 64bit
            for t in templ['Templates']:
                compatl = t['CompatiblePreConfiguredPackages']
                if compatl == [9, 10, 11]:
                    compat = "-MLX"
                elif compatl == [1, 6, 7, 8]:
                    compat = "SMLX"
                else:
                    compat = str(compatl)
                descr  = t['Description']
                showme = t['Enabled']
                id = t['Id']
                id_cod = t['IdentificationCode']
                name   = t['Name']
                ssh_in = t['SshKeyInitializationSupported']
                ipv6_ok= t['Ipv6Compatible']
                print(str(showme)+"|"+str(ipv6_ok)+"|"+compat+"|"+str(ssh_in)+"|\t"+str(id)+"|"+name+"\t|"+descr)


# templates(6)
