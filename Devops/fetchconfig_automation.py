import datetime
import os
import socket
import time

import paramiko
import schedule


def main():
    print('###### Start automative job: ' + datetime.date.today().isoformat() + ' ######')

    SrcFile = os.getcwd() + '\\fetchlist.txt'
    DstPath = 'E:\\zxchen\\logs\\' + datetime.date.today().isoformat()
    print('### Source list is: ' + SrcFile)
    check_dir(DstPath)
    print('### Destination dir is: ' + DstPath + '\n')
    autojob(SrcFile, DstPath)
    
def autojob(srcfile, dstpath):    
    f = open(srcfile, 'r')
    for line in f.readlines():
        ip, name, password, sleeptime = line.split()
        dstfilepath = dstpath + os.sep + name + '.txt'

        print('### Start '+ name + '...\n')
        
        sshcilent, isSuccess = ssh_connect(ip, 'admin', password)
        if not isSuccess:
            print('### Connection Failed.')
            generate_report('Failed', dstfilepath)
            continue
        
        cmdlist = ['screen-length 0 temporary\n', 'display curr\n']
        timelist = [0.5, int(sleeptime)]
        output = ssh_execute(sshcilent, cmdlist, timelist)
        sshcilent.close()
        generate_report(output, dstfilepath)
    f.close()

def check_dir(dirpath):
    if not os.path.exists(dirpath):
        os.mkdir(dirpath)
    else:
        pass

def ssh_connect(hip, user, hpassword):
    print('\n### Trying to connect to host...')
    ssh_success = False
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        client.connect(hostname=hip, port=22, username=user, password=hpassword)
        ssh_success = True
    except paramiko.AuthenticationException as auth_error:
        print(repr(auth_error))
    except paramiko.SSHException as ssh_error:
        print(repr(ssh_error))
    except socket.error as socket_error:
        print(repr(socket_error))
    return client, ssh_success

def ssh_execute(client, cmds, slptime):
    print('### Connection established. Executing command.')
    cmd_line = client.invoke_shell()
    for i in range(0, len(cmds)):
        cmd_line.send(cmds[i])
        time.sleep(slptime[i])
    res = cmd_line.recv(131071).decode(encoding='gbk')
    res.replace('\r', '')
    return res


def generate_report(res, filepath):
    with open(filepath, 'w+') as new_file:
        new_file.write(res)
        new_file.close()
        

if __name__ == '__main__':
#     password = getpass.getpass('input password: ')
#     print('Automation schedule is processing, please do not end it... ...')
#     schedule.every().day.at('12:00').do(autojob)
#     while True:
#         schedule.run_pending()
    main()
