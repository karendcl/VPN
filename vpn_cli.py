from utils import assign_ip_address
from vpn import VPN  # Import the VPN class from vpn.py
import PySimpleGUI as sg


# Create a VPN instance
vpn = VPN()

def CreateUser():
    """Create a window to input a user"""
    layout = [
        [sg.Text('Username:'), sg.Input(key='username')],
        [sg.Text('Password:'), sg.Input(key='password')],
        [sg.Text('VLAN:'), sg.Input(key='vlan')],
        [sg.Button('Submit', bind_return_key=True), sg.Cancel('Exit')]
        ]
    window = sg.Window('VPN User Creator', layout, return_keyboard_events=True)
    while True:
        event, values = window.Read()
        if event == 'Submit':
            try:
                username = values['username']
                password = values['password']
                vlan = int(values['vlan'])
                vpn.create_user(username, password, vlan)
                sg.PopupOK('User Created')
            except:
                sg.PopupError("Failed to create user")
        if event=='Exit':
            break
        if event == sg.WIN_CLOSED:
            break
    window.Close()
    main()


def RestrictUser():
    """Create a Window to restrict user"""
    layout=[
        [sg.Text('Username to restrict:')],
        [sg.Input(key="name", size=(25,1))],
        [sg.Text('IP Address:')],
        [sg.Input(key="ip", size=(20,1))],
        [sg.Button('Restrict Access',bind_return_key=True)],
        [sg.Button('Go Back')]
    ]
    restricted_window = sg.Window('Restricted Area',layout, return_keyboard_events=True)
    
    while True:
        event, values = restricted_window.Read()
        if event=='Restrict Access':
            try:
                name = values["name"]
                ip = int(values["ip"])
                vpn.restrict_user(name,ip)
                sg.PopupOK('Access Restricted')
            except:
                sg.PopupError("Invalid Input!")
        elif event=='Go Back':
            break
        if event == sg.WIN_CLOSED:
            break
    
    restricted_window.close()
    main()

        

def RestrictVLAN():
    """Create a Window for VLAN restriction"""
    layout=[
        [sg.Text('Enter the VLAN to restrict')],
        [sg.Input(key='vlans',size=(35,1),enable_events=True)],
        [sg.Text('Enter the IP address')],
        [sg.Input(key='ips',size=(40,6))],
        [sg.Button('Restrict'), sg.Button('Return')]
    ]
  
    restricted_window = sg.Window('Restricted Area',layout, return_keyboard_events=True)
    
    while True:
        event, values = restricted_window.Read()
        if event=='Restrict':
            try:
                vlan = int(values["vlans"])
                ip = int(values["ips"])
                vpn.restrict_vlan(vlan,ip)
                sg.PopupOK('Access Restricted')
            except:
                sg.PopupError("Invalid Input!")
        elif event=='Return':
            break
        if event == sg.WIN_CLOSED:
            break
    
    restricted_window.close()
    main()



def ShowLogs():
    """Show Logs in a new window"""
    log_text = []
    # Add lines from the log file to the text element
    while not vpn.log_queue.empty():
        log_text.append(vpn.log_queue.get())

    # Create a scrollable Text element with the log messages
    layout = [
            [sg.Listbox(log_text, size=(80,20), key="logs", enable_events=True)],
            [sg.Button('Return')]
        ]
    logs_window = sg.Window('Server Logs', layout).Finalize()
    while True:
        event, _ = logs_window.Read()
        if event == 'Return':
            break
        if event == sg.WIN_CLOSED:
            break
      

    logs_window.close()
    main()

def main():

    """Main function of the program."""
    # Set up GUI layout and window

    layout = [
        [sg.Button('Create User')],
        [sg.Button('Restrict User'),sg.Button('Restrict VLAN')],
        [sg.Button('Show Logs')],
        [sg.Button('Start'),sg.Button('Stop')]
        
    ]
    
    window2 = sg.Window('CV', layout)
    window2.size = (100, 100)

    window2.Resizable = True
    while True:
        event, values = window2.read()
        if event == sg.WIN_CLOSED :
            window2.close()
            break
        if event =='Start':
            vpn.start()
        if event == 'Stop':
            vpn.stop()
        if event == 'Create User':
            window2.close()
            CreateUser()
        if event == 'Restrict User':
            window2.close()
            RestrictUser()
        if event == 'Restrict VLAN':
            window2.close()
            RestrictVLAN()
        if event == 'Show Logs':
            window2.close()
            ShowLogs()


if __name__ == "__main__":
    main()
