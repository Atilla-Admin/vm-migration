import os

from system.host import Host

from ui.dialog import MainDialog
from ui.dialog import MENU_CHOICE_START_MIGRATION
from ui.dialog import MENU_CHOICE_ABOUT

from ui.exception import CancelException

class Migration():
    def __init__(self, interface):
        self.i = interface
        self.menu()

    def migrate(self):
        try:
            self.source_host = Host(self.i.get_source_host())
            self.source_host.load_volume_groups()
        except CancelException:
            return
        except Exception as e:
            self.i.show_error(e)

    def menu(self):
        while True:
            menu_item = self.i.main_menu()

            if menu_item == MENU_CHOICE_START_MIGRATION:
                self.migrate()
            elif menu_item == MENU_CHOICE_ABOUT:
                self.i.learn_more()
            else:
                os.system('clear')
                break

if __name__ == "__main__":
    interface = MainDialog()
    Migration(interface)
