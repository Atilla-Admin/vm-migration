import os

from ui.dialog import MainDialog
from ui.dialog import MENU_CHOICE_START_MIGRATION
from ui.dialog import MENU_CHOICE_ABOUT


class Migration():
    def __init__(self, interface):
        self.i = interface
        self.menu()

    def migrate(self):
        # TODO : Refactor
        source_vg = self.i.get_source_VG()
        if source_vg is None:
            return

        dest_vg = self.i.get_dest_VG(source_vg)
        if dest_vg is None:
            return

        source_lv_prefix = self.i.get_source_LV_prefix()
        if source_lv_prefix is None:
            return

        dest_lv_prefix = self.i.get_dest_LV_prefix(source_lv_prefix)
        if dest_lv_prefix is None:
            return

        source_bridge = self.i.get_source_bridge()
        if source_bridge is None:
            return

        dest_bridge = self.i.get_dest_bridge()
        if dest_bridge is None:
            return

        remote_host = self.i.get_dest_host()
        if remote_host is None:
            return

        out_file = 'output'
        out_pipe = ' > ' + out_file

        if os.path.isfile(out_file):
            os.remove(out_file)
        os.mkfifo(out_file)

        self.i.show_progress(out_file)

        os.system('echo Starting migration …' + out_pipe)

        disk_size = os.system(
                'lvs /dev/' + source_vg + '/' + source_lv_prefix
                + '-disk -o LV_SIZE '
                + '--noheadings --units K --nosuffix').replace(' ', '')

        swap_size = os.system(
                'lvs /dev/' + source_vg + '/' + source_lv_prefix
                + '-swap -o LV_SIZE --noheadings --units K --nosuffix')

        os.system('echo Creating LVM volumes on remote host …' + out_pipe)

        os.system(
                'ssh ' + remote_host + ' '
                + '"lvcreate -L +' + disk_size + 'K '
                + '-n ' + dest_lv_prefix + '-disk '
                + '/dev/' + dest_vg + '"' + out_pipe)

        os.system(
                'ssh ' + remote_host + ' '
                + '"lvcreate -L +' + swap_size + 'K '
                + '-n ' + dest_lv_prefix + '-swap '
                + '/dev/' + dest_vg + '"' + out_pipe)

        os.system('echo Moving swap …' + out_pipe)

        os.system(
                'dd if=/dev/' + source_vg + '/' + source_lv_prefix + '-swap '
                + '| ssh ' + remote_host + ' '
                + '" dd of=/dev/' + dest_vg + '/' + dest_lv_prefix + '-swap"'
                + out_pipe)

        os.system('echo Moving disk …' + out_pipe)

        os.system(
                'dd if=/dev/' + source_vg + '/' + source_lv_prefix + '-disk '
                + '| ssh ' + remote_host + ' '
                + '" dd of=/dev/' + dest_vg + '/' + dest_lv_prefix + '-disk"'
                + out_pipe)

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
