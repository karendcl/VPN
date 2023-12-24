import os
import socket
import struct
import json
import threading
from utils import *

class VPN:
    def __init__(self):
        self.run_thread = None
        self.stop_thread = False
        self.SERVER_ADDRESS = "127.0.0.1"
        self.SERVER_PORT = 8000
        self.raw_socket = None
        self.tabla = {}
        

        if not os.path.exists('logs.txt'):
            with open('logs.txt', 'w') as f:
                pass

        try:
            with open('users.json', 'r') as f:
                self.users = json.load(f)
        except FileNotFoundError:
            self.users = {}
            with open('users.json', 'w') as f:
                json.dump(self.users, f)

        try:
            with open('restricted_users.json', 'r') as f:
                self.restricted_users = json.load(f)
        except FileNotFoundError:
            self.restricted_users = {}
            with open('restricted_users.json', 'w') as f:
                json.dump(self.restricted_users, f)

        try:
            with open('restricted_vlans.json', 'r') as f:
                self.restricted_vlans = json.load(f)
        except FileNotFoundError:
            self.restricted_vlans = {}
            with open('restricted_vlans.json', 'w') as f:
                json.dump(self.restricted_vlans, f)

    

    def start(self):
        self.raw_socket = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_UDP)
        self.raw_socket.bind(('localhost', self.SERVER_PORT))

        # Create a new thread that will run the 'run' method, so we can still type in the console
        self.stop_thread = False
        self.run_thread = threading.Thread(target=self.run)
        self.run_thread.start()

        print(f"VPN started on {self.SERVER_ADDRESS}:{self.SERVER_PORT}")

    def stop(self):
        if self.run_thread is not None:
            self.raw_socket.close()
            self.raw_socket = None
            self.run_thread = None
            print(f"VPN is closed")

    def create_user(self, username, password, vlan_id):
        # Assign an IP address and a port to the user
        ip_address, port = assign_ip_address()
        self.users[username] = {'password': password, 'vlan_id': vlan_id, 'ip_address': ip_address, 'port': port}
        with open('users.json', 'w') as f:
            json.dump(self.users, f)

        self.log_message(f"User {username} created with IP address {ip_address}, port {port} and vlan {vlan_id}")

    def delete_user(self,user):
        """Deletes a user from the list of users."""
        del self.users[user]
        with open('users.json', 'w') as f:
            json.dump(self.users, f)

        logMessage(f"User {user} deleted")

    def restrict_user(self, user, ip):
        """Adds an IP address to the list of restricted addresses for a given user."""

        #check that it is not already a restriction
        uu = {'User': user, 'Address': ip}
        if uu in self.restricted_users.values():
            raise Exception("User is already restricted")
        

        key = len(self.restricted_users)+1
       
        self.restricted_users[key] = {"User": user, "Address": ip}
     
        with open('restricted_users.json', 'w') as f:
            json.dump(self.restricted_users, f)

        logMessage(f"User {user} restricted from {ip} IP Address")
    
    def unrestrict_user(self, user, ip):
        """Removes an IP address from the list of restricted addresses for a given user."""
        uu = {'User': user, 'Address': ip}
        index = [i for i in self.restricted_users.keys() if self.restricted_users[i] == uu][0]
        self.restricted_users.__delitem__(index)
        self.restricted_users=dict(
            zip(
                map(
                    lambda x:str(x+1),
                    list(range(0,len(self.restricted_users)))),
                self.restricted_users.values()
            ))
        with open('restricted_users.json', 'w') as f:
            json.dump(self.restricted_users, f)
        logMessage(f"User {user} unrestricted from IP {ip}")

    def restrict_vlan(self, vlan_id, ip):
        """Adds an IP address to the VLAN restriction list."""

        #check that it is not already a restriction
        vv = {'vlan': vlan_id, 'ip': ip}
        if vv in self.restricted_vlans.values():
            raise Exception("VLAN is already restricted")
        
        key = len(self.restricted_vlans)+1
        self.restricted_vlans[key] = {'vlan': vlan_id, 'ip': ip}
        with open('restricted_vlans.json', 'w') as f:
            json.dump(self.restricted_vlans, f)

        logMessage(f"All users from {vlan_id} VLAN restricted from {ip} IP Address")
    
    def unrestrict_vlan(self, vlan, ip):
        """Removes an IP address from the VLAN restriction list."""
        vv = {'vlan': vlan, 'ip': ip}
        index = [i for i in self.restricted_vlans.keys() if self.restricted_vlans[i] == vv][0]
        self.restricted_vlans.__delitem__(index)
        self.restricted_vlans=dict(
            zip(
                map(
                    lambda x:str(x+1),
                    list(range(0,len(self.restricted_vlans)))),
                self.restricted_vlans.values()
            ))
        with open('restricted_vlans.json', 'w') as f:
            json.dump(self.restricted_vlans, f)
        logMessage(f"All users from {vlan} VLAN unrestricted from IP {ip}")


    def validate_user(self, sender_addr, sender_port, dest_port):
        """Boolean if user is not restricted by any means"""

        # Check if the sender's IP address and port are registered
        user_data = next((user for user in self.users.values() if user['port'] == sender_port and user['ip_address']==sender_addr), None)
        username = next((user for user in self.users.keys() if self.users[user]['port'] == sender_port and self.users[user]['ip_address']==sender_addr), None)

        if user_data is None:
            self.log_message(f"Ignored packet coming from unregistered user: {sender_addr}:{sender_port}")
            return False
        
        #Check if user ip is not restricted 
        uu = {'User': username, 'Address': dest_port}
        #check if uu is not in restricted_users.values
        if uu in self.restricted_users.values():
            self.log_message(f"Access denied for user '{username}' on port {dest_port}" )
            return False
        
        #check if vlan is not restricted
        vv = {'vlan': int(user_data['vlan_id']), 'ip': dest_port}
        
        if vv in self.restricted_vlans.values():
            self.log_message(f"Restricted VLAN '{user_data['vlan_id']}' for ip '{dest_port}'")
            return False
       
        # If all validations pass, return True
        return True
    

    def log_message(self, message):
        # Write the message to the file
        logMessage(message)
            

    def run(self):
        while True:
            try:
                # Receive data
                data, addr = self.raw_socket.recvfrom(65535)

                # Unpack UDP header
                udp_header = data[20:28]
                udp_data = struct.unpack('!HHHH', udp_header)

                # Extract information
                source_port = udp_data[0]
                dest_port = udp_data[1]
                length = udp_data[2]

                # Check if the packet matches the filter criteria
                if dest_port == self.SERVER_PORT:

                    # Sender port is always 0 because it sends directly through the interface
                    real_sender_addr, real_sender_port = addr

                    sender_addr = data[30:].decode().split('#')[0]

                   #save into a dictionary the fake ip and port that belongs to the real user
                    self.tabla[':'.join([str(real_sender_addr),str(real_sender_port)])]  =  ':'.join([str(sender_addr),str(source_port)]) 
                    
                    # Extract destination port from data
                    forward_port = struct.unpack('!H', data[28:30])[0]

                    # Check if the user is created and not restricted
                    if not self.validate_user(sender_addr, source_port, forward_port):
                        continue

                    # Check checksum
                    received_checksum = udp_data[3]

                    # Set checksum field to zero before calculating checksum
                    zero_checksum_header = udp_header[:6] + b'\x00\x00' + udp_header[8:]
                    calculated_checksum = udp_checksum(sender_addr, self.SERVER_ADDRESS, zero_checksum_header + data[28:])

                    if received_checksum != calculated_checksum:
                        self.log_message("Checksum does not match, packet might be corrupted")
                        continue  # Skip the rest of the loop and wait for the next packet

                    

                    # Generate new UDP header with server port as source and dynamic port from data
                    new_source_port = self.SERVER_PORT
                    new_udp_header = struct.pack("!HHHH", source_port, forward_port, length, 0)

                    data_to_send = data[30:].decode().split('#')[1]

                    data_to_send = f'{sender_addr}#{data_to_send}'.encode()

                    # Calculate new checksum
                    new_udp_checksum = udp_checksum(self.SERVER_ADDRESS, self.SERVER_ADDRESS, new_udp_header +
                                                    data_to_send)
                    new_udp_header = struct.pack("!HHHH", source_port, forward_port, length, new_udp_checksum)

                    # Combine new header and original data for forwarding
                    forwarded_packet = new_udp_header + data_to_send

                    # Send the forwarded packet
                    self.raw_socket.sendto(forwarded_packet, (self.SERVER_ADDRESS, forward_port))

                    # Print confirmation
                    self.log_message(
                        f"Forwarded packet coming from {real_sender_addr}:{real_sender_port} to"
                        f" {self.SERVER_ADDRESS}:{forward_port} disguised as {sender_addr}:{source_port}")
                else:
                    # Discard the packet
                    self.log_message(f"Ignored packet meant for port {dest_port}")
            except AttributeError:
                if self.raw_socket is None:
                    break
                else:
                    raise
