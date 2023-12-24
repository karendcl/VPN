from utils import *
from vpn import VPN  # Import the VPN class from vpn.py
import PySimpleGUI as sg

# Create a VPN instance
vpn = VPN()

def CreateUser():
    """Create a window to input a user"""
    layout = [
        [sg.Text('')],
        [sg.Text('ViPeN', font=('Helvetica',42))],
        [sg.Text("Create User",font=('Arial',18))],
        [sg.Text('Username:',size=(15,1),expand_x=True), sg.Input(key='username')],
        [sg.Text('Password:',size=(15,1),expand_x=True), sg.Input(key='password',password_char='*')],
        [sg.Text('Check password:',size=(15,1),expand_x=True), sg.Input(key='Check',password_char='*')],
        [sg.Text('VLAN:',size=(15,1),expand_x=True), sg.Input(key='vlan')],
        [sg.Text('')],
        [sg.Button('Submit', bind_return_key=True), sg.Cancel('Exit')],
        [sg.Text('')]
        ]
    window = sg.Window('VPN User Creator', layout, return_keyboard_events=True,element_justification='c')
    while True:
        event, values = window.Read()
        if event == 'Submit':
            try:
                username = values['username']
                if(list(vpn.users).__contains__(username)):
                    sg.PopupOK("The user already exist!!")
                    continue
                if(username==''):
                    sg.PopupOK("Please introduce user name")
                    continue
                
                password = values['password']
                if(password==''):
                    sg.PopupOK("Please introduce password")
                    continue
                if(values['Check']!=password):
                    sg.PopupOK("The password doesn't match")
                    continue
                
                vlan = int(values['vlan'])
                vpn.create_user(username, password, vlan)
                sg.PopupOK('User Created')
                #update values
                window['username'].Update("")
                window['password'].Update("")
                window['Check'].Update("")
                window['vlan'].Update("")
            except Exception as e:
                sg.PopupError(f'Error {e}')
        if event=='Exit':
            break
        if event == sg.WIN_CLOSED:
            break
    window.Close()
    main()

def RestrictUser():
    """Create a Window to restrict user"""

    allUsers = list(vpn.users)
    layout=[
        [sg.Text('')],
        [sg.Text('ViPeN', font=('Helvetica',42))],
        [sg.Text('Username to restrict:')],
        [sg.Listbox(values=allUsers, key='name', size=(25,6), enable_events=True)],
        [sg.Text('IP Address:'),sg.Input(key="ip", size=(15,1))],
        [sg.Text('')],
        [sg.Button('Restrict Access',bind_return_key=True),sg.Button('Go Back')],
        [sg.Text('')]
    ]
    restricted_window = sg.Window('Restricted Area',layout, return_keyboard_events=True,element_justification='c')
    
    while True:
        event, values = restricted_window.Read()
        if event=='Restrict Access':
            try:
                name = values["name"][0]
                ip = int(values["ip"])
                vpn.restrict_user(name,ip)
                sg.PopupOK('Access Restricted')
            except Exception as e:
                sg.PopupError(f'Error {e}')
        elif event=='Go Back':
            break
        if event == sg.WIN_CLOSED:
            break
    
    restricted_window.close()
    main()

def DeleteUser():
    """Create a Window for deleting users"""
    allUsers = list(vpn.users)
    deleted = False
    layout=[
        [sg.Text('')],
        [sg.Text('ViPeN', font=('Helvetica',42))],
        [sg.Text('Username to delete:')],
        [sg.Listbox(values=allUsers, key='name', size=(25,6), enable_events=True)],
        [sg.Text('')],
        [sg.Button('Delete User',bind_return_key=True),sg.Button('Go Back')],
        [sg.Text('')]
    ]
    restricted_window = sg.Window('Restricted Area',layout, return_keyboard_events=True,element_justification='c')
    
    while True:
        event, values = restricted_window.read()
        if event=='Delete User':
            try:
                name = values["name"][0]
                vpn.delete_user(name)
                sg.PopupOK('User Deleted')
                deleted=True
                break
            except Exception as e:
                sg.PopupError(f'Error {e}')
        elif event=='Go Back':
            break
        if event == sg.WIN_CLOSED:
            break
    
    restricted_window.close()
    if deleted:
        DeleteUser()
    else:
        main()

def RestrictVLAN():
    """Create a Window for VLAN restriction"""
    layout=[
        [sg.Text('')],
        [sg.Text('ViPeN', font=('Helvetica',42))],
        [sg.Text('Enter the VLAN to restrict')],
        [sg.Input(key='vlans',size=(35,1),enable_events=True)],
        [sg.Text('Enter the IP address')],
        [sg.Input(key='ips',size=(35,1))],
        [sg.Text('')],
        [sg.Button('Restrict'), sg.Button('Return')],
        [sg.Text('')]
    ]
  
    restricted_window = sg.Window('Restricted Area',layout, return_keyboard_events=True,element_justification='c')
    
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
    cleared = False
    log_text = VPNLogs()
    # Add lines from the log file to the text element
    

    # Create a scrollable Text element with the log messages
    layout = [
            [sg.Text('ViPeN', font=('Helvetica',42))],
            [sg.Listbox(log_text, size=(80,20), key="logs", enable_events=True, horizontal_scroll=True)],
            [sg.Button('Return'), sg.Button('Clear Logs')]
        ]
    logs_window = sg.Window('Server Logs', layout,element_justification='c').Finalize()
    while True:
        event, _ = logs_window.Read()
        if event == 'Return':
            break
        if event == sg.WIN_CLOSED:
            break
        if event == 'Clear Logs':
            clearLogs()
            cleared=True
            break
               
    logs_window.close()
    if cleared:
        ShowLogs()
    else:
        main()

def DeleteRestrictionByUser():
    """Create a Window for deleting restriction by user"""
    allRestrictions = list(vpn.restricted_users.values())
    toShow = allRestrictions.copy()

    for i in range(len(allRestrictions)):
        user =allRestrictions[i]['User']
        ip = allRestrictions[i]['Address']
        toShow[i] = f'User {user} restricted from {ip}'

    deleted = False
    layout=[
        [sg.Text('')],
        [sg.Text('ViPeN', font=('Helvetica',42))],
        [sg.Text('Restriction to Delete:')],
        [sg.Listbox(values=toShow, key='name', size=(50,6), enable_events=True, horizontal_scroll=True)],
        [sg.Text('')],
        [sg.Button('Delete Restriction',bind_return_key=True),sg.Button('Go Back')],
        [sg.Text('')]
    ]
    restricted_window = sg.Window('Restricted Area',layout, return_keyboard_events=True,element_justification='c')
    
    while True:
        event, values = restricted_window.read()
        if event=='Delete Restriction':
            try:
                name = values["name"][0]
                index = toShow.index(name)
               
                user = allRestrictions[index]['User']
                ip = allRestrictions[index]['Address']
        
                vpn.unrestrict_user(user,ip)
                sg.PopupOK('Restriction Deleted')
                deleted=True
                break
            except Exception as e:
                sg.PopupError(f'Error {e}')
        elif event=='Go Back':
            break
        if event == sg.WIN_CLOSED:
            break
    
    restricted_window.close()
    if deleted:
        DeleteRestrictionByUser()
    else:
        main()

def DeleteRestrictionByVLAN():
    """Create a Window for deleting restriction by VLAN"""
    allRestrictions = list(vpn.restricted_vlans.values())
    toShow = allRestrictions.copy()

    for i in range(len(allRestrictions)):
        vlan =allRestrictions[i]['vlan']
        ip = allRestrictions[i]['ip']
        toShow[i] = f'VLAN {vlan} restricted from {ip}'

    deleted = False
    layout=[
        [sg.Text('')],
        [sg.Text('ViPeN', font=('Helvetica',42))],
        [sg.Text('Restriction to Delete:')],
        [sg.Listbox(values=toShow, key='name', size=(50,6), enable_events=True, horizontal_scroll=True)],
        [sg.Text('')],
        [sg.Button('Delete Restriction',bind_return_key=True),sg.Button('Go Back')],
        [sg.Text('')]
    ]
    restricted_window = sg.Window('Restricted Area',layout, return_keyboard_events=True,element_justification='c')
    
    while True:
        event, values = restricted_window.read()
        if event=='Delete Restriction':
            try:
                name = values["name"][0]
                index = toShow.index(name)
               
                vlan = allRestrictions[index]['vlan']
                ip = allRestrictions[index]['ip']
        
                vpn.unrestrict_vlan(vlan,ip)
                sg.PopupOK('Restriction Deleted')
                deleted=True
                break
            except Exception as e:
                sg.PopupError(f'Error {e}')
        elif event=='Go Back':
            break
        if event == sg.WIN_CLOSED:
            break
    
    restricted_window.close()
    if deleted:
        DeleteRestrictionByVLAN()
    else:
        main()

def main():

    """Main function of the program."""
    # Set up GUI layout and window

    sg.theme('DarkAmber')
    sg.set_options(font=('Arial Bold',18))

    layout = [
        [sg.Text('')],
        [sg.Text('ViPeN', font=('Helvetica',42))],
        [sg.Text("The best V.P.N. in the market",font=('Arial',18))],
        [sg.Text('')],
        [sg.Button('Start VPN'),sg.Button('Stop VPN')],
        [sg.Button('Create User'), sg.Button('Delete User')],
        [sg.Button('Restrict User'),sg.Button('Restrict VLAN')],
        [sg.Button('Unrestrict User'),sg.Button('Unrestrict VLAN')],
        [sg.Button('Show Logs'),sg.Button('Exit')],
        [sg.Text('')],
    ]
    
    window2 = sg.Window('VPN', layout, element_justification='c')
    
    window2.size = (400, 400)
    

    window2.Resizable = False
    while True:
        event, values = window2.read()
        if event == sg.WIN_CLOSED or event=='Exit' :
            window2.close()
            break
        if event =='Start VPN':
            vpn.start()
        if event == 'Stop VPN':
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
        if event == 'Delete User':
            window2.close()
            DeleteUser()
        if event == 'Unrestrict User':
            window2.close()
            DeleteRestrictionByUser()
        if event == 'Unrestrict VLAN':
            window2.close()
            DeleteRestrictionByVLAN()
        


if __name__ == "__main__":
    main()
