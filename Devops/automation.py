import os
import time
import getpass
import datetime
import schedule
import paramiko

def autojob():
    print('###### Start automative job: ' + datetime.date.today().isoformat() + ' ######')
    f = open(os.getcwd() + '\\iplist.txt', 'r')
    for line in f.readlines():
        ip, name = line.split()
        print('\tStart '+ name + '...')
        client = SSHConnetion(ip, name, 'admin')
        if client:
            output = SSHcommand(client, 'display int brief\n', 5)
            output = output.replace('\r', '').replace('---- More ----[42D                                          [42D', '')
        else:
            output = '\nConnection Failed.'
        client.close()
        generate_report(output, name)
        print('\t' + name + ' done.')
    f.close()
    print('\n###### Automative job: ' + datetime.date.today().isoformat() + ' Finished ######\n')
    print('Automation schedule is processing, please do not end it... ...')
    

def SSHConnetion(ipaddress, devicename, user):
    SSHclient = paramiko.SSHClient()
    SSHclient.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        SSHclient.connect(hostname=ipaddress, port=22, username=user, password=password)
        print('\tConnected to ' + devicename + ', ip: ' + ipaddress)
    except:
        print('\tConnection Failed.')
        return False
    return SSHclient


def SSHcommand(myclient, mycommand, spacecount):
    if not mycommand:
        return ''
    try:
        shell = myclient.invoke_shell()
        shell.send(mycommand)
        for i in range(spacecount):
            shell.send(' ')
            time.sleep(0.1)
        res = shell.recv(65535).decode('ascii')
    except:
        print('\tExecution Failed.')
        res = '\nError.'
    return res
    

def generate_report(res, devname):
    NewPath = os.getcwd() + os.sep + 'report' + os.sep + datetime.date.today().isoformat() + '.txt'
    with open(NewPath, 'a+') as new_file:
        new_file.write('##################################### ' + devname + ' ########################################')
        new_file.write(res)
        new_file.write('\n\n\n')
        new_file.close()
        

if __name__ == '__main__':
    password = getpass.getpass('input password: ')
    print('\n\nAutomation schedule is processing, please do not end it... ...')
    schedule.every().day.at('12:00').do(autojob)
    while True:
        schedule.run_pending()