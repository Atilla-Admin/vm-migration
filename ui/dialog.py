# -*- coding: utf-8 -*-

import locale
import re

from dialog import Dialog

from .exception import CancelException

locale.setlocale(locale.LC_ALL, '')

MENU_CHOICE_START_MIGRATION = "#1"
MENU_CHOICE_ABOUT = "#2"
MENU_CHOICE_QUIT = "#3"

HOST_CHECK_REGEX='^[\w\.]+\.\w+$'

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
                            "input satisfies the following regex :\n\n" + regex)
            else:
                raise CancelException()

    def get_source_host(self):
        return self.get_string(
                "Enter source host : ",
                regex=HOST_CHECK_REGEX)

    def get_dest_host(self):
        return self.get_string(
                "Enter the destination host : ",
                regex=HOST_CHECK_REGEX)

    def show_progress(self, fp):
        self.d.progressbox(fp)

    def main_menu(self):
        main_menu_choices = [
                (MENU_CHOICE_START_MIGRATION, "Start a new migration"),
                (MENU_CHOICE_ABOUT, "Learn more about this application"),
                (MENU_CHOICE_QUIT, "Quit the program")]

        while True:
            code, tag = self.d.menu(
                    "VM-Migration / Main menu",
                    choices=main_menu_choices)

            if code == self.d.OK:
                return tag
            else:
                return None

    def show_error(self, message):
        text = 'An error occured : \n\n{}'.format(message)
        self.d.msgbox(text)

    def learn_more(self):
        text = ('This application is meant to ease XEN VMs migration over '
                'network.\n\n'
                'Source code available at : \n'
                'https://gitlab.atilla.org/adminsys/vm-migration')
        self.d.msgbox(text)
