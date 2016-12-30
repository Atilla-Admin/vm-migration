import re
import time

from paramiko import AutoAddPolicy
from paramiko import SSHClient

from .vg import VG
from .exception import *

class Host:
    def __init__(self, hostname):
        self.hostname = hostname
        self.vgs = []
        self.client = SSHClient()
        self.client.set_missing_host_key_policy(AutoAddPolicy())

    def __str__(self):
        vg_string = ''
        for vg in self.vgs:
            vg_string += '- {}\n'.format(vg)
        return ('Host : {}\n'
                'Volume groups :\n'
                '{}').format(self.hostname, vg_string)

    def test_ssh_access(self):
        try:
            self.client.connect(self.hostname, username='root')
        except:
            return false
        self.close()
        return true

    def execute_command(self, command):
        self.client.connect(self.hostname, username='root')
        stdin, stdout, stderr = self.client.exec_command(command)
        while (not stdout.channel.exit_status_ready()
                and not stdout.channel.recv_ready()):
            time.sleep(1)

        self.client.close()
        if len(stderr.readlines()) is not 0:
            raise StandardError(stderr.readlines())
        return stdout.readlines()

    def load_volume_groups(self):
        stdout = self.execute_command('vgdisplay -A -c')
       
        # Parse output
        pattern = r'^\s*(?P<name>[\w\-]+):.*:(?P<uid>[\w\-]+)$'
        for line in stdout:
            reg = re.match(pattern, line)
            self.vgs.append(VG(self, reg.group('name'), reg.group('uid')))
