#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#import logging.config
#logging.config.dictConfig({
#    'version': 1,
#    'formatters': {
#        'verbose': {
#            'format': '%(name)s: %(message)s'
#        }
#    },
#    'handlers': {
#        'console': {
#            'level': 'DEBUG',
#            'class': 'logging.StreamHandler',
#            'formatter': 'verbose',
#        },
#    },
#    'loggers': {
#        'zeep.transports': {
#            'level': 'DEBUG',
#            'propagate': True,
#            'handlers': ['console'],
#        },
#    }
#})

from configparser import ConfigParser as iniParser

inifile = iniParser()
inifile.read("/home/mz0/.ssh/aruba/ansible.ini")
myId = inifile.get("acct0", "user")
myPw = inifile.get("acct0", "passwd")

from zeep import Client
from zeep.wsse.username import UsernameToken

wsdl_uri='https://api.dc1.computing.cloud.it/WsEndUser/v2.9/WsEndUser.svc?wsdl'
client = Client(wsdl_uri, wsse=UsernameToken(myId, myPw))
print("Login OK.")
#templates = client.service.GetHypervisors()
#print(templates)
print("Balance: {:0.2f}€".format(client.service.GetCredit()['Value']['Value']))

for contact in client.service.GetUserInfo()['Value']['UserContacts']['UserContact']:
    print("{}: {}".format(contact['ContactType'], contact['Value']))
