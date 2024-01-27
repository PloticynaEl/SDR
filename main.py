import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QComboBox

#USB
import re
import subprocess

class App(QMainWindow):
    def __init__(self):
        super().__init__()
        #self.uifile_name = namfile
        uic.loadUi('window_input.ui',self)
        self.continue_1.clicked.connect(self.button_continue_1)
        #self.update.clicked.connect(self.button_update)
        #self.update_button.clicked.connect(self.remoute)
        self.comboBox_devices.activated.connect(self.comboBox_activated)


    def button_continue_1(self):
        pass

    def show_remoute(self):
        print("запускаем окно настройки удаленного подключения")

    def show_usb(self):
        print("запускаем окно с выбором устройства usb")

    def comboBox_activated(self, index):
        print("Activated index:", index)
        if index == 0:
            pass
        elif index == 1:
            self.show_remoute()
        elif index == 2:
            self.show_usb()


    def button_update(self):

        device_re = re.compile("Bus\s+(?P<bus>\d+)\s+Device\s+(?P<device>\d+).+ID\s(?P<id>\w+:\w+)\s(?P<tag>.+)$", re.I)
        df = str(subprocess.check_output("lsusb"), 'utf-8')
        #print(df)
        devices = []
        for i in df.split('\n'):
            if i:
                info = device_re.match(i)
                if info:
                    dinfo = info.groupdict()
                    dinfo['device'] = '/dev/bus/usb/%s/%s' % (dinfo.pop('bus'), dinfo.pop('device'))
                    devices.append(dinfo)

        for i in devices:
            print(i['tag'])

        pass





if __name__ == '__main__':
    print('SDR')
    app = QApplication(sys.argv)
    ex = App()
    ex.show()
    sys.exit(app.exec())
