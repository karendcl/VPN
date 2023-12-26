import vpn
from utils import *
import socket

vpn = vpn.VPN()

vpn.create_user('testing','test','1')
port, ip = logIn('testing', 'test')
vpn.restrict_user('testing','11.11.11.11')


#assert user is restricted by username
assert (vpn.validate_user(ip, port, '11.11.11.11') is False)
assert (vpn.validate_user(ip, port, '11.11.11.12') is True)


vpn.create_user('testing2', 'test', '1')
port, ip = logIn('testing2', 'test')
vpn.restrict_vlan(1, '11.11.11.11')


# assert user is restricted by vlan
assert (vpn.validate_user(ip, port, '11.11.11.11') is False)
assert (vpn.validate_user(ip, port, '11.11.11.12') is True)


# testing packing and unpacking
SOURCE_ADDRESS = '127.127.0.2'
REAL_DEST_PORT = 15
message = SOURCE_ADDRESS + '#testing'
message = message.encode()
data = struct.pack(">H", REAL_DEST_PORT) + message

# unpack
real_port = struct.unpack(">H", data[:2])[0]
print(real_port)
SOURCE_ADDRESS = data[2:].decode().split('#')[0]
print(SOURCE_ADDRESS)

print(':'.join([SOURCE_ADDRESS,str(real_port)] ))

