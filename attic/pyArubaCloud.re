ArubaCloud/
PyArubaAPI.py:        self.wcf_baseurl = 'https://api.dc%s.computing.cloud.it/WsEndUser/v2.9/WsEndUser.svc/json' % (str(dc))
objects/Scheduled.py: self.wcf_baseurl = 'https://api.dc%s.computing.cloud.it/WsEndUser/v2.9/WsEndUser.svc/json' % (str(DC))
=============================
PyArubaAPI.py
class CloudInterface(...)
  templates = []
  vmlist = VMList()
  iplist = IpList()
  json_templates = None
  json_servers = None
  hypervisors = {3: "LC", 4: "SMART", 2: "VW", 1: "HV"}
  def get_servers(self):
  def find_template(self, name=None, hv=None): -> get_hypervisors()
  def get_hypervisors(self):
  def poweroff_server(self, server=None, server_id=None):
  def poweron_server(self, server=None, server_id=None):
  def get_jobs(self):
  
VmTypes/__init.py__
class Smart(VM):
    def __init__(self, interface, sid):
        super(Smart, self).__init__(interface)
        self.cltype = 'smart'
        self.sid = sid
        self.ip_addr = Ip()
        self.package = None # Packages available are: 1, 2, 3, 4.
        
base/vm.py
    def reinitialize(self, admin_password=None, debug=False, ConfigureIPv6=False, OSTemplateID=None):
