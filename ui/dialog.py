# -*- coding: utf-8 -*-

import locale
import re

from dialog import Dialog

locale.setlocale(locale.LC_ALL, '')

MENU_CHOICE_START_MIGRATION = "#1"
MENU_CHOICE_ABOUT = "#2"
MENU_CHOICE_QUIT = "#3"

class MainDialog:
    def __init__(self):
        self.d = Dialog(dialog="dialog", autowidgetsize=True)
        self.d.set_background_title("ATILLA - VM Migration")

    def check_regex(self, regex, message):
        if regex is not None:
            comp = re.compile(regex)
            return comp.match(message)
        else:
            return True

    def get_string(self, message, default='', regex=None):
        while True:
            code, string = self.d.inputbox(message, init=default)

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

    def get_dest_VG(self, default=''):
        return self.get_string("Enter the destination VG name : ", default)

    def get_source_LV_prefix(self):
        return self.get_string("Enter the source LV prefix : ")

    def get_dest_LV_prefix(self, default=''):
        return self.get_string("Enter the destination LV prefix : ", default)

    def get_source_bridge(self):
        return self.get_string("Enter the source bridge name : ")

    def get_dest_bridge(self, default=''):
        return self.get_string("Enter the destination bridge name : ", default)

    def get_dest_host(self):
        return self.get_string("Enter the destination host : ")

    def show_progress(self, fp):
        self.d.progressbox(fp)

    def main_menu(self):
        main_menu_choices = [
                (MENU_CHOICE_START_MIGRATION, "Start a new migration"),
                (MENU_CHOICE_ABOUT, "Learn more about this application"),
                (MENU_CHOICE_QUIT, "Quit the program")]

        while True:
            code, tag = self.d.menu(
                    "VM-Migration / Hello !",
                    choices=main_menu_choices)

            if code == self.d.OK:
                return tag
            else:
                return None

    def learn_more(self):
        text = ("This application is meant to ease XEN VMs migration over "
                "network.\n\n"
                "Source code available at : \n"
                "https://gitlab.atilla.org/adminsys/vm-migration")
        self.d.msgbox(text)
