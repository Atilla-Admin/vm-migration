# -*- coding: utf-8 -*-

import locale
import re

from dialog import Dialog

from .exception import CancelException

locale.setlocale(locale.LC_ALL, '')

class DialogInterface:
    def __init__(self, title):
        self.d = Dialog(dialog='dialog', autowidgetsize=True)
        self.d.set_background_title(title)

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
                    self.d.msgbox('Invalid input, please make sure that your '
                            'input satisfies the following regex :\n\n' + regex)
            else:
                raise CancelException()

    def select(self, text, items):
        code, it = self.d.checklist(text, items=items)

        if code == self.d.OK:
            return it
        else:
            raise CancelException()

    def show_progress(self, fp):
        self.d.progressbox(fp)

    def show_message(self, message):
        self.d.msgbox(message)

    def show_info(self, message):
        self.d.infobox(message)

    def menu(self, title, choices):
        while True:
            code, tag = self.d.menu(
                    title,
                    choices=choices)

            if code == self.d.OK:
                return tag
            else:
                raise CancelException()
