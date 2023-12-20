import vpn
from utils import *

vpn = vpn.VPN()

vpn.create_user('testing','test','1')
port, ip = logIn('testing', 'test')
vpn.restrict_user('testing','11.11.11.11')

#assert user is restricted by username
assert(vpn.validate_user(ip,port,'11.11.11.11')==False)
assert(vpn.validate_user(ip,port,'11.11.11.12')==True)


vpn.create_user('testing2','test','1')
port, ip = logIn('testing2', 'test')
vpn.restrict_vlan(1,'11.11.11.11')

#assert user is restricted by vlan
assert(vpn.validate_user(ip,port,'11.11.11.11')==False)
assert(vpn.validate_user(ip,port,'11.11.11.12')==True)
