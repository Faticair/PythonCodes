import datetime
import time
import os
import paramiko
import schedule
import getpass


def myjob():
    print('### Schedule begin ###\n')
    filepath = os.getcwd() + '\\Python\\Devops\\iplist.txt'
    f = open(filepath)
    for line in f.readlines(): 
        ip = line.strip()
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(hostname=ip, port=22, username='zxchen', password=password)
        
        #### for Huawei & Cisco switches ####
        # command = client.invoke_shell()
        # command.send('ifconfig\n')
        # time.sleep(1)
        # output = command.recv(65535).decode('ascii')
        #### for Linux ####
        stdin, stdout, stderr = client.exec_command("ifconfig")
        output = ''.join(stdout.readlines())
        output = output.replace('\r', '')
        client.close()
        generateFile(output)
        print(ip + ' executed!')

def generateFile(res: str):
    NewFilePath = os.getcwd() + '\\Python\\Devops\\' + datetime.date.today().isoformat()
    with open(NewFilePath, 'a+') as new_file:
        new_file.write(res)
        new_file.close()


if __name__ == '__main__':
    password = getpass.getpass('input password: ')
    schedule.every().day.at('16:02').do(myjob)
    while True:
        schedule.run_pending()