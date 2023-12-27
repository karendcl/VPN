from utils import *
import socket
import struct

rp=0

def process_data(coordenada, caracter_nuevo):
    # Abre el archivo en modo lectura
    with open('draw.txt', 'r') as file:
        lines = file.readlines()
    caracter_nuevo='◾' if caracter_nuevo==1 else '◽'
    # Modifica el caracter en la coordenada especificada
    y, x = coordenada
    if 0 <= y < len(lines) and 0 <= x < len(lines[y]):
        nueva_linea = lines[y][:x] + caracter_nuevo + lines[y][x+1:]
        lines[y] = nueva_linea

    # Escribe los cambios de vuelta al archivo
    with open('draw.txt', 'w') as file:
        file.writelines(lines)

# Create and bind raw socket
SERVER_ADDRESS = "127.0.0.1"
SERVER_PORT = 7002
raw_socket = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_UDP)
raw_socket.bind(('localhost', SERVER_PORT))

while True:
    corrupted = False
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
            corrupted = True

        # Process the packet
        rec = data[28:].decode()

        # separate the address and port
        rec = rec.split('#')
        address = rec[0]
        data = rec[1]
        data=data.split(',')
        coordinates=(int(data[1]),int(data[0]))
        
        # Print basic information
        corrupted = False
        try:
            process_data(coordinates,int(data[2]))
            rp+=1
            print(rp)
        except:
            pass
    else:
        # Discard the packet
        print("Ignoring packet coming from: ", source_port)

# Close socket
raw_socket.close()
