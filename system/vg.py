import re

from lv import LV

class VG:
    def __init__(self, host, name, uid):
        self.host = host
        self.name = name
        self.uid = uid
        self.lvs = []

    def __str__(self):
        return 'Name : {}, UID : {}'.format(self.name, self.uid)

    def load_logical_volumes(self):
        stdout = self.host.execute_command(
                'lvdisplay -c /dev/{}'.format(self.name))

        pattern = r'^\s*[\w\/\-]+\/(?P<name>[\w\-]+):.*$'
        for line in stdout:
            reg = re.match(pattern, line)
            self.lvs.append(LV(self, reg.group('name')))
