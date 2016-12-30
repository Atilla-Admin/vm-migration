# -*- coding: utf-8 -*-

import locale

from .interface import DialogInterface

locale.setlocale(locale.LC_ALL, '')

MENU_CHOICE_START_MIGRATION = '#1'
MENU_CHOICE_ABOUT = '#2'
MENU_CHOICE_QUIT = '#3'

HOST_CHECK_REGEX = '^[\w\.]+\.\w+$'


class MainDialog:
    def __init__(self):
        self.d = DialogInterface('ATILLA - VM Migration')

    def get_source_host(self):
        return self.d.get_string(
                'Enter source host : ',
                regex=HOST_CHECK_REGEX)

    def get_dest_host(self):
        return self.d.get_string(
                'Enter the destination host : ',
                regex=HOST_CHECK_REGEX)

    def show_progress(self, fp):
        self.d.progressbox(fp)

    def show_info(self, message):
        self.d.show_info(message)

    def show_error(self, message):
        self.d.show_message('An error occured : \n\n{}'.format(message))

    def main_menu(self):
        main_menu_choices = [
                (MENU_CHOICE_START_MIGRATION, 'Start a new migration'),
                (MENU_CHOICE_ABOUT, 'Learn more about this application'),
                (MENU_CHOICE_QUIT, 'Quit the program')]

        return self.d.menu('VM-Migration / Main menu', main_menu_choices)

    def learn_more(self):
        text = ('This application is meant to ease XEN VMs migration over '
                'network.\n\n'
                'Source code available at : \n'
                'https://gitlab.atilla.org/adminsys/vm-migration')
        self.d.show_message(text)
