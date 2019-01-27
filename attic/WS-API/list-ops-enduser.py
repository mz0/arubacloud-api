#!/usr/bin/env python3

import operator
from zeep import Client
from zeep.wsse.username import UsernameToken

wsdl_uri='https://api.dc1.computing.cloud.it/WsEndUser/v2.9/WsEndUser.svc?wsdl'
client = Client(wsdl_uri)

for service in client.wsdl.services.values():
    print("service:", service.name)
    for port in service.ports.values():
        ops = sorted(port.binding._operations.values(),key=operator.attrgetter('name'))
        for op in ops:
            print("method :", op.name)
            print(" input :", op.input.signature())
            print()
