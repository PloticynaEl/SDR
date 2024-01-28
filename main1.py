import sys
import time

from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QDialog, QMainWindow, QMessageBox

#USB
import re
import subprocess

class Window1(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('window_input.ui',self)
        self.continue_1.clicked.connect(self.button_continue_1)
        self.comboBox_devices.activated.connect(self.comboBox_activated)

    def button_continue_1(self):
        pass

    def comboBox_activated(self, index):
        print("Activated index:", index)
        if index == 0:
            pass
        elif index == 1:
            self.show_remoute()
        elif index == 2:
            self.show_usb()

    def openWindow2(self):
        self.window2 = Window2() #REMOUTE
        self.window2.exec_()

    def show_remoute(self):
        print("запускаем окно настройки удаленного подключения")
        self.openWindow2()

    def openWindow3(self):
        self.window3 = Window3() #USB
        self.window3.exec_()

    def show_usb(self):
        print("запускаем окно с выбором устройства usb")
        self.openWindow3()

class Window2(QDialog): #REMOUTE
    def __init__(self):
        super().__init__()
        uic.loadUi('window_remoute.ui',self)
        self.pushButton_choose.clicked.connect(self.pushButton_choose_func)
        self.pushButton_cancel.clicked.connect(lambda: self.close())

    def pushButton_choose_func(self):
        print(self.comboBox_choose.currentText())
        print(self.textEdit_port.toPlainText())
    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Внимание',
                                     "Вы хотите отменить действие?",
                                     QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            event.accept() # Если пользователь подтверждает, то окно закрывается
        else:
            event.ignore() # Если нет, то событие игнорируется

class Window3(QDialog): #USB
    def __init__(self):
        super().__init__()
        uic.loadUi('window_usb.ui',self)
        self.pushButton_cancel.clicked.connect(lambda: self.close())
        self.pushButton_update.clicked.connect(self.pushButton_update_func)
        self.pushButton_choose.clicked.connect(self.pushButton_choose_func)


    def pushButton_update_func(self):
        self.listWidget.clear()
        device_re = re.compile("Bus\s+(?P<bus>\d+)\s+Device\s+(?P<device>\d+).+ID\s(?P<id>\w+:\w+)\s(?P<tag>.+)$", re.I)
        df = str(subprocess.check_output("lsusb"), 'utf-8')
        devices = []
        for i in df.split('\n'):
            if i:
                info = device_re.match(i)
                if info:
                    dinfo = info.groupdict()
                    dinfo['device'] = '/dev/bus/usb/%s/%s' % (dinfo.pop('bus'), dinfo.pop('device'))
                    devices.append(dinfo)

        for i in devices:
            self.listWidget.addItem(i['tag'])

    def pushButton_choose_func(self):
        window1.comboBox_devices.addItem(self.listWidget.selectedIndexes()[0].data())
        window1.comboBox_devices.setCurrentIndex(window1.comboBox_devices.count() - 1)
        self.close()


    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Внимание',
                                     "Вы хотите отменить действие?",
                                     QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            event.accept() # Если пользователь подтверждает, то окно закрывается
        else:
            event.ignore() # Если нет, то событие игнорируется


if __name__ == '__main__':
    print('SDR')
    app = QApplication(sys.argv)
    window1 = Window1()
    window1.show()
    sys.exit(app.exec_())