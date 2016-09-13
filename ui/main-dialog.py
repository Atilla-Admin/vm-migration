import re

from dialog import Dialog

locale.setlocale(locale.LC_ALL, '')

class MainDialog:
    def __init__(self, auto_run=True):
        self.d = Dialog(dialog="dialog", autowidgets=True)
        self.d.set_background_title("ATILLA - VM Migration")
        if auto_run:
            self.run()

    def check_regex(self, regex, message):
        if regex is not None:
            comp = re.compile(regex)
            return comp.match(message)
        else:
            return True

    def get_string(self, message, regex=None):
        while True:
            code, string = self.d.inputbox(message)

            if code == self.d.OK:
                if self.check_regex(regex, string):
                    return string
                else:
                    self.d.msgbox("Invalid input, please make sure that your "
                            "input satisfies the following regex : " + regex)
            else:
                return None

    def get_source_VG(self):
        return self.get_string("Enter the source VG name : ")

    def get_dest_VG(self):
        return self.get_string("Enter the destination VG name : ")

    def get_source_LV(self):
        return self.get_string("Enter the source LV name : ")

    def get_dest_LV(self):
        return self.get_string("Enter the destination LV name : ")

    def get_source_bridge(self):
        return self.get_string("Enter the source bridge name : ")

    def get_dest_bridge(self):
        return self.get_string("Enter the destination bridge name : ")

    def get_dest_host(self):
        return self.get_string("Enter the destination host : ")

    def learn_more(self):
        text = ("This application is meant to ease XEN VMs migration over "
                "network.\n\n"
                "Source code available at : \n"
                "https://gitlab.atilla.org/adminsys/vm-migration")
        self.d.msgbox(text)
