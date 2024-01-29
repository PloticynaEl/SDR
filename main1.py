import sys
import time

from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QDialog, QMainWindow, QMessageBox

#USB
import re
import subprocess

import SoapySDR

class Window1(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('window_input.ui',self)
        self.continue_1.clicked.connect(self.button_continue_1)
        self.comboBox_devices.activated.connect(self.comboBox_activated)

    def button_continue_1(self):
        self.openWindow5()
        pass

    def comboBox_activated(self, index):
        print("Activated index:", index)
        if index == 0:
            pass
        elif index == 1:
            self.show_remoute()
        elif index == 2:
            self.show_usb()
        elif index == 3:
            self.show_usb_soapy()
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

    def show_usb_soapy(self):
        print("запускаем окно с выбором устройства soapy")
        self.openWindow4()

    def openWindow4(self):
        self.window4 = Window4() #Soapy(USB)
        self.window4.exec_()
    def openWindow5(self):
        self.window5 = Window5() #Soapy(USB)
        self.window5.exec_()

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
        self.device = 0
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
        print(devices)
        for i in devices:
            self.listWidget.addItem(i['tag'])


    def pushButton_choose_func(self):
        window1.comboBox_devices.addItem(self.listWidget.selectedIndexes()[0].data())
        window1.comboBox_devices.setCurrentIndex(window1.comboBox_devices.count() - 1)
        self.close()


    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Внимание',
                                     "Продолжть?",
                                     QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            event.accept() # Если пользователь подтверждает, то окно закрывается
        else:
            event.ignore() # Если нет, то событие игнорируется


class Window4(QDialog): #SoapySDR(USB)
    def __init__(self):
        super().__init__()
        uic.loadUi('window_usb.ui',self)
        self.pushButton_cancel.clicked.connect(lambda: self.close())
        self.pushButton_update.clicked.connect(self.pushButton_update_func)
        self.pushButton_choose.clicked.connect(self.pushButton_choose_func)


    def pushButton_update_func(self):
        self.listWidget.clear()
        for d in SoapySDR.Device.enumerate(''):
            self.listWidget.addItem(str(d['label'] ))


    def pushButton_choose_func(self):
        window1.comboBox_devices.addItem(self.listWidget.selectedIndexes()[0].data())
        window1.comboBox_devices.setCurrentIndex(window1.comboBox_devices.count() - 1)
        self.close()
        self.device = SDRDevice()
        self.device.print_info()


    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Внимание',
                                     "Продолжть?",
                                     QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            event.accept() # Если пользователь подтверждает, то окно закрывается
        else:
            event.ignore() # Если нет, то событие игнорируется

class SDRDevice():
    def __init__(self):
        self.soapy_device = "sdrplay"
        self.device = SoapySDR.Device(dict(driver=self.soapy_device))

    def print_info(self):
        channels = list(range(self.device.getNumChannels(SoapySDR.SOAPY_SDR_RX)))
        ch = channels[0]
        sample_rates = self.device.listSampleRates(SoapySDR.SOAPY_SDR_RX, ch)
        for i in sample_rates:
            window1.comboBox.addItem(str(i))
        window1.comboBox.setCurrentIndex(0)

        bandwidths = list(map(lambda r: int(r.maximum()), self.device.getBandwidthRange(SoapySDR.SOAPY_SDR_RX, ch)))
        for i in bandwidths:
            window1.comboBox_3.addItem(str(i))
        window1.comboBox_3.setCurrentIndex(0)

    def get_text(self):
        channels = list(range(self.device.getNumChannels(SoapySDR.SOAPY_SDR_RX)))
        text = "Channels:" + str(channels) + "\n"
        ch = channels[0]
        sample_rates = self.device.listSampleRates(SoapySDR.SOAPY_SDR_RX, ch)
        text += "Sample rates:\n" + str(sample_rates) + "\n"

        bandwidths = list(map(lambda r: int(r.maximum()), self.device.getBandwidthRange(SoapySDR.SOAPY_SDR_RX, ch)))
        text += "Bandwidths:\n" + str(bandwidths) + "\n"

        text += "Gain controls:" + "\n"
        for gain in self.device.listGains(SoapySDR.SOAPY_SDR_RX, ch):
            text += "  %s: %s" % (gain, self.device.getGainRange(SoapySDR.SOAPY_SDR_RX, ch, gain))

        frequencies = self.device.listFrequencies(SoapySDR.SOAPY_SDR_RX, ch)
        text += "Frequencies names:" +str(frequencies) + "\n"

        frequency_name = frequencies[0]
        text += "Frequency channel name:" + str(frequency_name) + "\n"

        text += "Frequency range:" +str( self.device.getFrequencyRange(SoapySDR.SOAPY_SDR_RX, ch, frequency_name)[0])
        return text

class Window5(QDialog): #modulation
    def __init__(self):
        super().__init__()
        uic.loadUi('window_modulation.ui',self)
        #self.pushButton_cancel.clicked.connect(lambda: self.close())
        self.device = SDRDevice()
        self.text2 = self.device.get_text()
        self.textEdit.setText(str(self.text2))


    def pushButton_update_func(self):
        self.listWidget.clear()
        for d in SoapySDR.Device.enumerate(''):
            self.listWidget.addItem(str(d['label'] ))


    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Внимание',
                                     "Продолжть?",
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