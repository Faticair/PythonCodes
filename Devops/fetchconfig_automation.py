import os
import time
import getpass
import datetime
import schedule
import paramiko

def autojob():
    print('###### Start automative job: ' + datetime.date.today().isoformat() + ' ######')
    f = open(os.getcwd() + '\\fetchlist.txt', 'r')
    for line in f.readlines():
        ip, name, password, sleeptime = line.split()
        print('Start '+ name + '...')
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            client.connect(hostname=ip, port=22, username='admin', password=password)
            time.sleep(1)
            print('Connected... Now execute command...')
            command_line = client.invoke_shell()
            command_line.send('screen-length 0 temporary\n')
            time.sleep(0.5)
            command_line.send('display curr\n')
            time.sleep(int(sleeptime))
            output = command_line.recv(131071).decode(encoding='gbk')
            # output = ''
            # while recv_ready():
            #     output += command_line.recv(65535).decode(encoding='gbk')
            output.replace('\r', '')
            print(name + ' success.')
        except:
            print('!!!!!! Alert: ' + name + ' failed !!!!!!')
            output = "Failed."
        client.close()
        generate_report(output, name)
    f.close()
    
#     print('\n###### Automative job: ' + datetime.date.today().isoformat() + ' Finished ######\n')
#     print('Automation schedule is processing, please do not end it... ...')
    
    
def generate_report(res, devname):
    NewPath = 'E:\\zxchen\\logs\\' + datetime.date.today().isoformat() + os.sep + devname + '.txt'
    with open(NewPath, 'w+') as new_file:
#         new_file.write('##################################### ' + devname + ' ########################################')
        new_file.write(res)
#         new_file.write('\n\n\n')
        new_file.close()
        

if __name__ == '__main__':
#     password = getpass.getpass('input password: ')
#     print('Automation schedule is processing, please do not end it... ...')
#     schedule.every().day.at('12:00').do(autojob)
#     while True:
#         schedule.run_pending()
    todaypath = 'E:\\zxchen\\logs\\' + datetime.date.today().isoformat()
    if not os.path.exists(todaypath):
        os.mkdir(todaypath)
    autojob()