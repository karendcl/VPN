from utils import *
import socket
import struct

def process_data(data):
    #return data+1
    try:
        num = int(data)
        return num+1
    except Exception as e:
        print(f'Error: {e}')


# Create and bind raw socket
SERVER_ADDRESS = "127.0.0.1"
SERVER_PORT = 7000
raw_socket = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_UDP)
raw_socket.bind(('localhost', SERVER_PORT))

while True:
    # Receive data
    data, addr = raw_socket.recvfrom(65535)

    # Unpack UDP header
    udp_header = data[20:28]
    udp_data = struct.unpack('!HHHH', udp_header)

    # Extract information
    source_port = udp_data[0]
    dest_port = udp_data[1]
    length = udp_data[2]
    checksum = udp_data[3]

    # Check if the packet matches the filter criteria
    if dest_port == SERVER_PORT:

        # Check checksum
        received_checksum = udp_data[3]

        sender_address, sender_port = addr

        # Set checksum field to zero before calculating checksum
        zero_checksum_header = udp_header[:6] + b'\x00\x00' + udp_header[8:]
        calculated_checksum = udp_checksum(sender_address, SERVER_ADDRESS, zero_checksum_header + data[28:])

        if received_checksum != calculated_checksum:
            logMessage('Checksum does not match. Packet corrupted')

        # Process the packet
        rec = data[28:].decode()

        # separate the address and port
        rec = rec.split('#')
        address = rec[0]
        data = rec[1]

        # Print basic information
        print("Basic Information: ")
        print(f"UDP packet received from {address}:{source_port}")
        print(f"Length: {length}, Checksum: {checksum}")
        print("Received valid packet:", data)
        try:
            res = process_data(data)
            print(f'Factorial of {data} is {res}')
        except:
            pass
    else:
        # Discard the packet
        print("Ignoring packet coming from: ", source_port)

    print("---------------------------------------------------------")

# Close socket
raw_socket.close()