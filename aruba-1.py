#!/usr/bin/python3

import requests
from pprint import pprint
import json
from datetime import datetime
from sys import stderr

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


def c0x(cmd, x=''):
    """ x=ServerId
    GetServerDetails, SetEnqueueServerStart (powerOn), SetEnqueueServerPowerOff, SetEnqueueServerDeletion """
    return '{{"ApplicationId":"{}","RequestId":"{}","SessionId":"{}","Password":"{}","Username":"{}"{}' \
           '}}'.format(cmd, cmd, cmd, myPw, myId, x)


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
    data1 = c0x(cmd=cmd)
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
    x = ',"ServerId":{}'.format(server)
    data2 = c0x(cmd=cmd, x=x)
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


def templates(dc):
    cmd = 'GetHypervisors'
    data1 = c0x(cmd=cmd)
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


# for dc in [1, 5, 6]: list_server(dc)
# templates(1)


def get_servers(dc):
    servers = []
    cmd = "GetServers"
    data1 = c0x(cmd=cmd)
    headers = {h_ct: t_json, h_cl: str(len(data1))}
    response = requests.post(u(dc, cmd), data=data1, headers=headers)
    if response.status_code == 200 and \
       h_ct in response.headers and \
       response.headers[h_ct] == t_json:
         re = response.content
    try:
        for j in json.loads(re)['Value']:
            # pprint(j)
            name    = j['Name']
            tpl     = j['OSTemplateId']
            powerOn = j['ServerStatus']==3
            server  = j['ServerId']
            busy    = j['Busy']
            servers.append({"DC": dc, "ServerID": server, "ServerName": name,
                 "Busy":busy, "TemplateID": tpl, "isOn": powerOn})
    except Exception as e:
        stderr.write(e)
    return servers


def cmdX(dc, cmd, x=''):
    data = c0x(cmd=cmd, x=x)
    headers = {h_ct: t_json, h_cl: str(len(data))}
    return requests.post(u(dc, cmd), data=data, headers=headers)

def isBusy(s):
    dc  = s["DC"]
    sId = s["ServerID"]
    all = get_servers(dc)
    for x in all:
        if x["ServerID"] == sId:
            return x['Busy']


def poweroff(s):
    if not s["isOn"]:
        stderr.write("Already Off!\n")
        return
    if isBusy(s):
        stderr.write("Busy!\n")
        return
    server = s["ServerID"]
    dc     = s["DC"]
    cmd  = "SetEnqueueServerPowerOff"
    xtra = ',"ServerId":{}'.format(server)
    cmdX(dc, cmd, xtra)

    cmd = "GetJobs"
    response = cmdX(dc, cmd, xtra)
    pprint(response.headers)
    pprint(response.content)
# '{"ExceptionInfo":null,"ResultCode":0,"ResultMessage":null,"Success":true,"Value":[
#    {"CreationDate":"\\/Date(1544463013390+0100)\\/","JobId":7958363,"LastUpdateDate":"\\/Date(1544463013390+0100)\\/","LicenseId":null,"OperationName":"StopVirtualMachineSmartVMWare","Progress":0,"ResourceId":null,"ResourceValue":null,"ServerId":292659,"ServerName":"La","Status":1,"UserId":70331,"Username":"AWI-71331"}]}'


def poweron(s):
    if s["isOn"]:
        stderr.write("Already On!\n")
        return
    if isBusy(s):
        stderr.write("Busy!\n")
        return
    server = s["ServerID"]
    dc     = s["DC"]
    cmd = "SetEnqueueServerStart"
    x = ',"ServerId":{}'.format(server)
    data = c0x(cmd=cmd, x=x)
    headers = {h_ct: t_json, h_cl: str(len(data))}
    response = requests.post(u(dc, cmd), data=data, headers=headers)
#   pprint(response.headers)
#   pprint(response.content)
# {'Content-Length': '73',
#  'X-AspNet-Version': '4.0.30319', 'Set-Cookie': 'ASP.NET_SessionId=jwe0r42fww1ulyyoam1uwxjx; path=/; HttpOnly',
#  'X-Powered-By': 'ASP.NET',  'Server': 'Microsoft-IIS/7.5', 'Cache-Control': 'private',
#  'Date': 'Mon, 10 Dec 2018 16:14:55 GMT', 'Content-Type': 'application/json'}
#'{"ExceptionInfo":null,"ResultCode":0,"ResultMessage":null,"Success":true}'


def reinit(s):
    server = s["ServerID"]
    dc     = s["DC"]
    cmd = "SetEnqueueReinitializeServer"
    rtpw = 'fsk;dlfk'
    ipv6 = 'false'
    x = ',"AdministratorPassword":"{}","ServerId":{},"ConfigureIPv6":{}'.format(rtpw, server, ipv6)
    data = c0x(cmd=cmd, x=x)
    headers = {h_ct: t_json, h_cl: str(len(data))}
    response = requests.post(u(dc, cmd), data=data, headers=headers)
    pprint(response.headers)
    pprint(response.content)


for s in get_servers(1):
    pprint(s)
    poweroff(s)
    poweroff(s)
    reinit(s)
