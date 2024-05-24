from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QVBoxLayout, QWidget
import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QDialog, QMainWindow, QMessageBox, QFileDialog
import re
import subprocess
import SoapySDR
import fmfm_wav_iq
import os
import datetime
from pathlib import Path


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('win_start.ui', self)
        self.pushButton_server.clicked.connect(self.openWindow_server)
        self.pushButton_client.clicked.connect(self.openWindow_client)
        # Вызываемые окна
        self.window_server = Window_server()
        self.window_client = Window_client()

    def openWindow_server(self):
        self.hide()
        self.window_server.show()

    def openWindow_client(self):
        self.hide()
        self.window_client.show()


class Window_server(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('win_server.ui', self)
        # self.run_button_remoute.clicked.connect(self.button_run)
        self.cancel_button_remoute.clicked.connect(self.button_cancel)

    def button_cancel(self):
        self.hide()
        mainwindow.show()


class Window_client(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('win_client.ui', self)
        self.pushButton_conti_client.clicked.connect(self.button_continue)
        self.comboBox_devices.activated.connect(self.comboBox_activated)
        self.window_info = Window_info()
        self.window_remoute = Window_remoute()
        self.window_usb = Window_usb()
        self.window_soapy = Window_soapy()

    def comboBox_activated(self, index):
        if index == 0:
            pass
        elif index == 1:
            # запускаем окно настройки удаленного подключения
            self.hide()
            self.window_remoute.show()
        elif index == 2:
            # запускаем окно с выбором устройства usb
            self.hide()
            self.window_usb.show()
        elif index == 3:
            # запускаем окно с выбором устройства soapy
            self.hide()
            self.window_soapy.show()

    def button_continue(self):
        self.hide()
        self.window_info.show()


class Window_remoute(QWidget):  # REMOUTE
    def __init__(self):
        super().__init__()
        uic.loadUi('win_remoute.ui', self)
        self.continue_button_remoute.clicked.connect(self.pushButton_continue_button_remoute)
        self.cancel_button_remoute.clicked.connect(self.button_cancel)

    def pushButton_continue_button_remoute(self):
        fmfm_wav_iq.REMOUTE = True
        port = self.textEdit_port_remoute.toPlainText()
        fmfm_wav_iq.DRIVER_ID = 'soapy=0,driver=remote,remote=tcp://%s' % port
        self.close()
        mainwindow.window_client.show()

    def button_cancel(self):
        self.close()
        self.hide()
        mainwindow.window_client.show()

    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Внимание',
                                     "Продолжить?",
                                     QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()


class Window_usb(QWidget):  # USB
    def __init__(self):
        super().__init__()
        uic.loadUi('win_usb.ui', self)
        self.device = 0
        self.cancel_button_usb.clicked.connect(self.button_cancel)
        self.update_button_usb.clicked.connect(self.pushButton_update_func)
        self.continue_button_usb.clicked.connect(self.pushButton_choose_func)

    def pushButton_update_func(self):
        self.listWidget_usb.clear()
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
            self.listWidget_usb.addItem(i['tag'])

    def pushButton_choose_func(self):
        mainwindow.window_client.comboBox_devices.addItem(self.listWidget_usb.selectedIndexes()[0].data())
        mainwindow.window_client.comboBox_devices.setCurrentIndex(mainwindow.window_client.comboBox_devices.count() - 1)
        self.close()
        mainwindow.window_client.show()
        # self.device = SDRDevice("sdrplay")
        # DEVICE = True
        # self.device.print_info()

    def button_cancel(self):
        self.close()
        self.hide()
        mainwindow.window_client.show()

    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Внимание',
                                     "Продолжть?",
                                     QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            event.accept()  # Если пользователь подтверждает, то окно закрывается
        else:
            event.ignore()  # Если нет, то событие игнорируется


class Window_soapy(QDialog):  # SoapySDR(USB)
    def __init__(self):
        super().__init__()
        uic.loadUi('win_usb.ui', self)
        self.cancel_button_usb.clicked.connect(self.button_cancel)
        self.update_button_usb.clicked.connect(self.pushButton_update_func)
        self.continue_button_usb.clicked.connect(self.pushButton_choose_func)

    def pushButton_update_func(self):
        self.listWidget_usb.clear()
        for d in SoapySDR.Device.enumerate(''):
            self.listWidget_usb.addItem(str(d['label']))

    def pushButton_choose_func(self):
        mainwindow.window_client.comboBox_devices.addItem(self.listWidget_usb.selectedIndexes()[0].data())
        mainwindow.window_client.comboBox_devices.setCurrentIndex(mainwindow.window_client.comboBox_devices.count() - 1)
        self.close()
        mainwindow.window_client.show()
        # self.device = SDRDevice("sdrplay")
        # DEVICE = True
        # self.device.print_info()

    def button_cancel(self):
        self.close()
        self.hide()
        mainwindow.window_client.show()

    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Внимание',
                                     "Продолжть?",
                                     QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            event.accept()  # Если пользователь подтверждает, то окно закрывается
        else:
            event.ignore()  # Если нет, то событие игнорируется


class Window_info(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('win_info.ui', self)
        # if (fmfm_wav_iq.REMOUTE == False):
        # self.device = window_usb.device.device
        # self.device = SDRDevice(DEVICE)
        # self.text2 = window_usb.device.device.get_text()
        # self.textEdit.setText(str(self.text2))
        self.cancel_button_info.clicked.connect(self.button_cancel)
        self.continue_button_info.clicked.connect(self.button_continue)
        self.window_demod = Window_demod()

    def button_continue(self):
        # запускаем окно демодуляции
        self.hide()
        self.window_demod.show()

    def button_cancel(self):
        self.close()
        self.hide()
        mainwindow.window_client.show()

    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Внимание',
                                     "Продолжть?",
                                     QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            event.accept()  # Если пользователь подтверждает, то окно закрывается
        else:
            event.ignore()  # Если нет, то событие игнорируется


class Window_demod(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('win_demodulation.ui', self)
        # self.pushButton_cancel.clicked.connect(lambda: self.close())
        if (fmfm_wav_iq.REMOUTE == False):
            print("print")
            self.device = SDRDevice('sdrplay')
            for i in self.device.sample_rates:
                self.comboBox_sampl.addItem(str(i))
            self.comboBox_sampl.setCurrentIndex(0)
        self.cancel_button_demod.clicked.connect(self.button_cancel)
        self.continue_button_demod.clicked.connect(self.start_DSP)
        # self.checkBox.stateChanged.connect(self.onStateChanged)

    def start_DSP(self):
        fmfm_wav_iq.BASE_FREQ = self.doubleSpinBox_freq.value() * 1000000
        print(fmfm_wav_iq.BASE_FREQ)
        sampl_currentText = self.comboBox_sampl.currentText()
        print(sampl_currentText)
        dot_index = sampl_currentText.find('.')
        print(dot_index)
        if dot_index > -1:
            sampl_currentText = sampl_currentText[:dot_index]
        fmfm_wav_iq.SAMP_RATE = int(sampl_currentText)
        print(fmfm_wav_iq.SAMP_RATE)
        self.hide()
        fmfm_wav_iq.fmfm_start_dsp()

    def button_cancel(self):
        self.close()
        self.hide()
        mainwindow.window_client.window_info.show()

    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Внимание',
                                     "Продолжть?",
                                     QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            event.accept()  # Если пользователь подтверждает, то окно закрывается
        else:
            event.ignore()  # Если нет, то событие игнорируется


class SDRDevice():
    def __init__(self, soapy_device):
        self.soapy_device = soapy_device
        self.sample_rates = []
        fmfm_wav_iq.DRIVER_ID[0] = soapy_device
        self.device = SoapySDR.Device(dict(driver=self.soapy_device))


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('win_start.ui', self)
        self.pushButton_server.clicked.connect(self.openWindow_server)
        self.pushButton_client.clicked.connect(self.openWindow_client)

        # 1 вызываемое окно
        self.window_server = Window_server()
        # 2 вызываемое окно
        self.window_client = Window_client()

    def openWindow_server(self, checked):
        self.hide()
        self.window_server.show()

    def openWindow_client(self, checked):
        self.hide()
        self.window_client.show()


app = QApplication(sys.argv)
mainwindow = MainWindow()
mainwindow.show()
app.exec()