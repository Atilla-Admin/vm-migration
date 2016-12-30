class VG:
    def __init__(self, name, uid):
        self.name = name
        self.uid = uid
    
    def __str__(self):
        return 'Name : {}, UID : {}'.format(self.name, self.uid)
