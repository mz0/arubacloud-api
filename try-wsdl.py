#!/usr/bin/env python3

from zeep import Client
try:
    from ConfigParser import ConfigParser as iniParser
except ModuleNotFoundError:
    from configparser import ConfigParser as iniParser

wsdl_uri='https://api.dc1.computing.cloud.it/WsEndUser/v2.9/WsEndUser.svc?wsdl'

inifile = iniParser()
inifile.read("/home/mz0/.ssh/aruba/ansible.ini")
myId = inifile.get("acct0", "user")
myPw = inifile.get("acct0", "passwd")

client = Client(wsdl_uri)
result = client.service.GetHypervisors()

#from requests import Session
#from requests.auth import HTTPBasicAuth
#from zeep.transports import Transport
#send_data=[{
#  'cat:getCategories' :[{ 'startOffSet' : 0,
#    'rowCount' : 4, 'withSpecs':'true',
#    'withDeepest':'true', 'withCatalog':'true',
#    'lang':'tr' }]
#}]
#session = Session()
#session.auth = HTTPBasicAuth(user, password)
#client = Client(wsdl_uri,
#  transport=Transport(session=session))
#print(client.service.service_name(parameter1,parameter2,parameter3..))
