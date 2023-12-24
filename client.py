import random
from utils import *
import socket
import struct
import PySimpleGUI as sg
from utils import *


logged = False
username = ''
virtualPort = 0
virtualIp = ''
SERVER_ADDRESS = "127.0.0.1"
SERVER_PORT =8000
REAL_DEST_PORT = 0

def SendUDPpacket(message):
    """Send a UDP packet to the server"""
    # Create a raw socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_UDP)

    # Define source and destination ports
    SOURCE_ADDRESS = virtualIp
    SOURCE_PORT = virtualPort

    # Build a string array of 10 strings that build up a coherent message
    messages = str(message).split()

    for i in range(len(messages)):
        # Pack the fake IP address into the message
        message = SOURCE_ADDRESS + '#' + messages[i]
        message = message.encode()

        # Pack the real destination port before actual data
        data = struct.pack(">H", REAL_DEST_PORT) + message
     

        # Build the UDP header
        
        udp_header = struct.pack("!HHHH", SOURCE_PORT, SERVER_PORT, 8 + len(data), 0)

        # Calculate checksum
        checksum = udp_checksum(SOURCE_ADDRESS, SERVER_ADDRESS, udp_header + data)

        rand_num = random.randint(1, 5)
        message = messages[i]
        if rand_num == 1:
            checksum_to_send = 1
        else:
            checksum_to_send = checksum

        udp_header = struct.pack("!HHHH", SOURCE_PORT, SERVER_PORT, 8 + len(data), checksum_to_send)
        packet = udp_header + data
        sock.sendto(packet, (SERVER_ADDRESS, SERVER_PORT))
        print(f"Sent UDP packet #{i} to {SERVER_ADDRESS}:{SERVER_PORT} with real destination port {REAL_DEST_PORT}")

    sock.close()


def LogIn():
    global logged, username, virtualPort, virtualIp

    layout = [
            [[sg.Text("")]],
            [sg.Text('ViPeN', font=('Helvetica',42))],
            [sg.Text("Please log in first:\n")],
            [sg.Text('Username',size=(10,1),expand_x=True), sg.Input(key='username',size=(30,1))],
            [sg.Text('Password',size=(10,1),expand_x=True), sg.Input(password_char='*', key='password',size=(30,1))],
            [[sg.Text("")]],
            [sg.Button('Login'), sg.Button('Back')],
            [[sg.Text("")]]
        ]

    window = sg.Window('Chat Client', layout,element_justification='c')
    while True:
        if logged:
            sg.popup_error(f'Already log in as {username}. Please log out first')
            break
        event, values = window.read()
        if event == 'exit' or event == sg.WIN_CLOSED:
            break
        if event == "Login":
            try:
                username = values['username']
                if(username==''):
                    sg.PopupOK("Please introduce user name")
                    continue
                password = values['password']
                if(password==''):
                    sg.PopupOK("Please introduce password")
                    continue
                port1, ip1 = logIn(username, password)
                if port1 is not False:
                    virtualPort = port1
                    virtualIp = ip1
                    logged = True
                    sg.popup(f'Logged In {ip1}:{port1}')
                    break
                else:
                    sg.PopupError('Wrong Username/Password')
            except Exception as e:
                sg.popup_error(e)
                break
        if event =="Back":
            break
    window.close()
    main()


def SendMess():

    global logged, REAL_DEST_PORT

    layout = [
            [[sg.Text("")]],
            [sg.Text('ViPeN', font=('Helvetica',42))],
            [sg.Text("Connected as "+ username +"\n")],
            [sg.Text('Send Message')],
            [sg.Input(key='Message', size=(20, 4))],
            [sg.Listbox(values=['Factorial','Plus 1'], key='fun', size=(20,2))],
            [[sg.Text("")]],
            [sg.Button('Send'),sg.Button("LogOut", key="disconnect"), sg.Exit(key='exit')],
            [[sg.Text("")]]
        ]
    
    window = sg.Window('Chat Client', layout,element_justification='c')

    if logged==False:
        sg.popup_error('Log In First')
    else:
        while True:
            event, values = window.read()
            if event == 'exit' or event== sg.WIN_CLOSED:
                break
            if event=='Send':
                try:
                    mes = values['Message']
                    prt = values['fun'][0]
                    if mes is not None and prt is not None and mes is not '':
                        if prt == 'Factorial':
                            REAL_DEST_PORT = 7000
                        else:
                            REAL_DEST_PORT = 7001

                        SendUDPpacket(mes)
                        window['Message'].update('')
                    else:
                        sg.popup_error('No fields can be empty')
                except Exception as e:
                    sg.popup_error(e)
                    break
            elif event=="disconnect":
                logged = False
                break
    window.close()
    main()
    

def main():
    """Main function"""
    #create MainWindow
    sg.theme('DarkAmber')   # Add a touch of color
    sg.set_options(font=('Arial Bold',18))
    
    layout=[
        [[sg.Text("")]],
        [sg.Text('  Welcome to ViPeN  ', font=('Helvetica',42))],
        [sg.Text("The best V.P.N. in the market\n",font=('Arial',18))],
        [sg.Button('Log In'),sg.Button('Send Message'),sg.Button('Exit')],
        [[sg.Text("")]]
    ]
    
    window = sg.Window('Chat Client', layout,element_justification='c')
    while True:
        event, values = window.read()
        if event == 'Exit' or event== sg.WIN_CLOSED:
            break
        if event == 'Log In':
            window.close()
            LogIn()
        if event=='Send Message':
            window.close()
            SendMess()
    
    window.close()


if __name__ =="__main__":
    main()