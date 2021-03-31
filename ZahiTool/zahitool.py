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
    url_ = 'http://ip.cip.cc/'
    url_sub = 'https://checkip.amazonaws.com'
    try:
        r = requests.get(url_)
    except :
        r = requests.get(url_sub)
    if not r:
        print('The websiites are all unavaliable.')
        return '0.0.0.0'
    pub_ip = r.text.strip()
    return pub_ip


def get_cpu_stat():
    print('*******************')
    print(' CPU usage is {} '.format(psutil.cpu_percent(interval=1, percpu=True))) # catch cpu usage per 0.1s
    print(' CPU has {} cores '.format(psutil.cpu_count()))
    print('*******************\n')


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

def run():
    print("Your host ip is", get_host_ip())
    print("Your public ip is", get_public_ip())
    get_cpu_stat()
    get_disk_stat()
    get_memory_stat()

if __name__ == "__main__":
    # pass
    run()
