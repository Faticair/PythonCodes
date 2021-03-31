import os
import socket
import psutil
import requests


def get_host_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('114.114.114.114', 80))
        ip = s.getsockname()[0]
        # print(s.getsockname())
    finally:
        s.close()
    return ip


def get_public_ip():
    # url_ = 'https://checkip.amazonaws.com'
    url_ = 'http://ip.cip.cc/'
    pub_ip = requests.get(url_).text.strip()
    return pub_ip


def get_cpu_stat():
    print('*******************')
    print(' CPU usage is {} '.format(psutil.cpu_percent(interval=1, percpu=True))) # catch cpu usage per 0.1s
    print(' CPU has {} cores '.format(psutil.cpu_count()))
    print('*******************\n')

def get_cpu_stat_test():
    print(psutil.cpu_freq())
    print('\n')
    print(psutil.cpu_stats())
    print('\n')
    print(psutil.cpu_times_percent(interval=1))
    CPUList = psutil.cpu_times_percent(interval=1, percpu=True)
    for member in CPUList:
        print(member)

def get_memory_stat():
    vm = psutil.virtual_memory()
    print('Virtual memory: {}%'.format(vm.percent))
    print('total: {}\tused: {}\tfree: {}\n'.format(byte_transfer(vm.total), byte_transfer(vm.used), byte_transfer(vm.free)))


def get_disk_stat():
    diskinfo = psutil.disk_partitions(all=False)
    rootdick = []
    for d in diskinfo:
        rootdick.append(d[1])
    print('Your system has {} disk'.format(len(rootdick)))
    for rd in rootdick:
        rdinfo = psutil.disk_usage(rd)
        print('Disk {}\tusage percent:{}%'.format(rd, rdinfo.percent))
        print('total: {:<20}used: {:<20}free: {:<20}'.format(byte_transfer(rdinfo.total), byte_transfer(rdinfo.used), byte_transfer(rdinfo.free)))
    print('')

def byte_transfer(b: int) -> str:
    fb = float(b)
    layer = {0: 'B', 1: 'KB', 2: 'MB', 3: 'GB', 4: 'TB'}
    count = 0
    while fb > 1024 and count < 5:
        fb = fb / 1024
        count += 1
    return str(round(fb, 4)) + layer[count]


if __name__ == '__main__':

    # print(os.getcwd())
    # print(os.listdir(os.getcwd()))
    # print(socket.gethostname())
    # print(socket.gethostbyname(socket.gethostname()))

    get_cpu_stat_test()
    # get_disk_stat()
    # get_memory_stat()
