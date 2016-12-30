class LV:
    def __init__(self, host, name):
        self.host = host
        self.name = name

    def __str__(self):
        return 'Name : {}'.format(self.name)
