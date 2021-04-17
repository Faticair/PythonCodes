import datetime
import os
import socket
import time

import paramiko
import schedule

class SshServer():

    commandlist = [] # list contain all the command
    nodelist = [] # every list element contains [ip, name, password]

    def get_commands(self, cmdfile):
        with open(cmdfile, 'r') as cf:
            for line in cf.readlines():
                if not line:
                    continue
                self.commandlist.append(line.strip() + '\n')
    
    def get_nodes(self, srcfile):
        with open(srcfile, 'r') as sf:
            for line in sf.readlines():
                ip, name, password = line.split()
                self.nodelist.append([ip, name, password])

    def node_connect(self, nodeip, nodename, nodepwd): # modification need
        node = paramiko.SSHClient()
        node.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            node.connect(hostname=nodeip, port=22, username=nodename, password=nodepwd)
        except:
            pass
        return node

    def execute_command(self, nodes, cmds): # modification need
        cmd_line = nodes.invoke_shell()
        for cmd in cmds:
            cmd_line.send(cmd)
            time.sleep(1)
        res = cmd_line.recv(131071).decode(encoding='gbk')
        res.replace('\r', '')
        return res

