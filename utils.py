import random
import json
import socket
import struct
import datetime



def assign_ip_address():
    ip_address = f"127.0.0.1"
    port = random.randint(1024, 20000)
    return ip_address, port


#logIn
def logIn(username, password):
    users ={}
    try:
        with open('users.json', 'r') as f:
            users = json.load(f)
    except FileNotFoundError:
            users = {}
            with open('users.json', 'w') as f:
                json.dump(users, f)

    if username in users and users[username]['password'] == password:
            return users[username]['port']
    else:
            return False
    

def VPNLogs():
      """ Return a list with all logs of the vpn"""
      logs=[]
      with open("logs.txt", "r") as file:
            for line in file:
                  logs.append(line)
      return logs

def logMessage(message):
     """ Add a message to the logs.txt file """

     #get current datetime
     now = datetime.datetime.now()


     with open("logs.txt","a+") as file:
          file.write(str(now) + ' :  ' + str(message) + '\n')


            

def udp_checksum(source_ip, dest_ip, udp_packet):
    pseudo_header = struct.pack('!4s4sBBH',
                                socket.inet_aton(source_ip),
                                socket.inet_aton(dest_ip),
                                0,
                                socket.IPPROTO_UDP,
                                len(udp_packet))
    return calc_checksum(pseudo_header + udp_packet)


def calc_checksum(packet):
    if len(packet) % 2 != 0:
        packet += b'\0'
    res = sum((int.from_bytes(packet[i:i + 2], 'big') for i in range(0, len(packet), 2)))
    res = (res >> 16) + (res & 0xffff)
    res += res >> 16
    return ~res & 0xffff