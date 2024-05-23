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

DEVICE = None

class Window0(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('win_start.ui',self)
        self.pushButton_server.clicked.connect(self.openWindow_server)
        self.pushButton_client.clicked.connect(self.openWindow_client)

    def openWindow_server(self):
        global window_server
        self.close()
        window_server = Window_server()
        window_server.show()
    def openWindow_client(self):
        global window_client
        self.close()
        window_client = Window_client()
        window_client.show()

class Window_server(QDialog):
    def __init__(self):
        super().__init__()
        uic.loadUi('win_server.ui',self)
        self.run_button_remoute.clicked.connect(self.button_run)
        self.cancel_button_remoute.clicked.connect(self.button_cancel)

    def button_run(self):
        print("server run")

    def button_cancel(self):
        self.close()
        window0.show()

class Window_client(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('win_client.ui',self)
        self.pushButton_conti_client.clicked.connect(self.button_continue)
        self.comboBox_devices.activated.connect(self.comboBox_activated)

    def button_continue(self):
    #if DEVICE != None:
        print("sdr connect")
        # запускаем окно с информацией о устройстве
        self.close()
        window_info = Window_info()
        window_info.show()

    def comboBox_activated(self, index):
        if index == 0:
            pass
        elif index == 1:
            # запускаем окно настройки удаленного подключения
            global window_remoute
            window_remoute = Window_remoute()  # REMOUTE
            window_remoute.exec_()
        elif index == 2:
            # запускаем окно с выбором устройства usb
            global window_usb
            window_usb = Window_usb()  # USB
            window_usb.exec_()
        elif index == 3:
            # запускаем окно с выбором устройства soapy
            global window_soapy
            window_soapy = Window_soapy()
            window_soapy.exec_()



    def openWindow6(self):
        self.window6 = Window6() # path
        self.window6.exec_()


class Window_remoute(QDialog): #REMOUTE
    def __init__(self):
        super().__init__()
        uic.loadUi('win_remoute.ui',self)
        self.continue_button_remoute.clicked.connect(self.pushButton_continue_button_remoute)
        self.cancel_button_remoute.clicked.connect(lambda: self.close())

    def pushButton_continue_button_remoute(self):
        fmfm_wav_iq.REMOUTE = True
        port = self.textEdit_port_remoute.toPlainText()
        fmfm_wav_iq.DRIVER_ID = 'soapy=0,driver=remote,remote=tcp://%s' % port
        self.close()

    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Внимание',
                                     "Продолжить?",
                                     QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

class Window_usb(QDialog): #USB
    def __init__(self):
        super().__init__()
        uic.loadUi('win_usb.ui',self)
        self.device = 0
        self.cancel_button_usb.clicked.connect(lambda: self.close())
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
        window_client.comboBox_devices.addItem(self.listWidget_usb.selectedIndexes()[0].data())
        window_client.comboBox_devices.setCurrentIndex(window_client.comboBox_devices.count() - 1)
        self.close()
        self.device = SDRDevice("sdrplay")
        #DEVICE = True
        self.device.print_info()

    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Внимание',
                                     "Продолжть?",
                                     QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            event.accept() # Если пользователь подтверждает, то окно закрывается
        else:
            event.ignore() # Если нет, то событие игнорируется

class Window_soapy(QDialog): #SoapySDR(USB)
    def __init__(self):
        super().__init__()
        uic.loadUi('win_usb.ui',self)
        self.cancel_button_usb.clicked.connect(lambda: self.close())
        self.update_button_usb.clicked.connect(self.pushButton_update_func)
        self.continue_button_usb.clicked.connect(self.pushButton_choose_func)

    def pushButton_update_func(self):
        self.listWidget_usb.clear()
        for d in SoapySDR.Device.enumerate(''):
            self.listWidget_usb.addItem(str(d['label'] ))

    def pushButton_choose_func(self):
        window_client.comboBox_devices.addItem(self.listWidget_usb.selectedIndexes()[0].data())
        window_client.comboBox_devices.setCurrentIndex(window_client.comboBox_devices.count() - 1)
        self.close()
        self.device = SDRDevice("sdrplay")
        DEVICE = True
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
    def __init__(self,soapy_device):
        self.soapy_device = soapy_device
        self.sample_rates = []
        fmfm_wav_iq.DRIVER_ID[0] = soapy_device
        self.device = self.soap()
    def soap(self):
        global SELFDEVICE
        SELFDEVICE = SoapySDR.Device(dict(driver=self.soapy_device))
        return SELFDEVICE

    def print_info(self):
        channels = list(range(self.device.getNumChannels(SoapySDR.SOAPY_SDR_RX)))
        ch = channels[0]
        self.sample_rates = self.device.listSampleRates(SoapySDR.SOAPY_SDR_RX, ch)
        for i in self.sample_rates:
            window_client.comboBox_first_samp_freq.addItem(str(i))
        window_client.comboBox_first_samp_freq.setCurrentIndex(0)

        bandwidths = list(map(lambda r: int(r.maximum()), self.device.getBandwidthRange(SoapySDR.SOAPY_SDR_RX, ch)))
        for i in bandwidths:
            window_client.comboBox_bandwidth.addItem(str(i))
        window_client.comboBox_bandwidth.setCurrentIndex(0)

    def get_text(self):
        channels = list(range(self.device.getNumChannels(SoapySDR.SOAPY_SDR_RX)))
        text = "Channels:" + str(channels) + "\n"
        ch = channels[0]
        self.sample_rates = self.device.listSampleRates(SoapySDR.SOAPY_SDR_RX, ch)
        text += "Sample rates:\n" + str(self.sample_rates) + "\n"

        bandwidths = list(map(lambda r: int(r.maximum()), self.device.getBandwidthRange(SoapySDR.SOAPY_SDR_RX, ch)))
        text += "Bandwidths:\n" + str(bandwidths) + "\n"

        text += "Gain controls:" + "\n"
        for gain in self.device.listGains(SoapySDR.SOAPY_SDR_RX, ch):
            text += "  %s: %s" % (gain, self.device.getGainRange(SoapySDR.SOAPY_SDR_RX, ch, gain))

        frequencies = self.device.listFrequencies(SoapySDR.SOAPY_SDR_RX, ch)
        text += " \n Frequencies names:" + str(frequencies) + "\n"

        frequency_name = frequencies[0]
        text += "Frequency channel name:" + str(frequency_name) + "\n"

        text += "Frequency range:" +str( self.device.getFrequencyRange(SoapySDR.SOAPY_SDR_RX, ch, frequency_name)[0])
        return text

class Window_info(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('win_info.ui',self)
        # self.pushButton_cancel.clicked.connect(lambda: self.close())
        #if (fmfm_wav_iq.REMOUTE == False):
            #self.device = window_usb.device.device
            #self.device = SDRDevice(DEVICE)
            #self.text2 = window_usb.device.device.get_text()
            #self.textEdit.setText(str(self.text2))

        self.cancel_button_info.clicked.connect(lambda: self.close())
        self.continue_button_info.clicked.connect(self.button_continue)


    def button_continue(self):
        # запускаем окно демодуляции
        self.close()
        window_demod = Window_demod()
        window_demod.show()

class Window_demod(QDialog): # demodulation
    def __init__(self):
        super().__init__()
        uic.loadUi('win_demodulation.ui',self)
        # self.pushButton_cancel.clicked.connect(lambda: self.close())
        if (fmfm_wav_iq.REMOUTE == False):
            print("print")
            #self.device = window_usb.device.device
            #self.device = SDRDevice(DEVICE)
            #for i in self.device.sample_rates:
                #self.comboBox_sampl.addItem(str(i))
            #self.comboBox_sampl.setCurrentIndex(0)
        self.cancel_button_demod.clicked.connect(lambda: self.close())
        self.continue_button_demod.clicked.connect(self.start_DSP)
        self.checkBox.stateChanged.connect(self.onStateChanged)

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
        self.close()
        fmfm_wav_iq.fmfm_start_dsp()

    def onStateChanged(self):
        if self.checkBox.isChecked():
            # Запись файлов
            Window_client.openWindow6(window_client)
            fmfm_wav_iq.SAVE=True
        else:
            # Без записи файлов
            fmfm_wav_iq.SAVE = False


    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Внимание',
                                     "Продолжть?",
                                     QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            event.accept() # Если пользователь подтверждает, то окно закрывается
        else:
            event.ignore() # Если нет, то событие игнорируется

class Window6(QDialog): # select path
    def __init__(self):
        super().__init__()
        uic.loadUi('window_path.ui',self)
        self.cancel_button_5.clicked.connect(lambda: self.close())
        self.continue_button_5.clicked.connect(lambda: self.close())
        self.path_button.clicked.connect(self.open_dir_dialog)

    def open_dir_dialog(self):
        dir_name = QFileDialog.getExistingDirectory(self, "Select a Directory")
        if dir_name:
            path = Path(dir_name)
            fmfm_wav_iq.DIRECTORY_PATH = str(path)
            self.lineEdit_path.setText(str(path))
            self.textEdit_path.setText(str(os.path.join(path,"SDR_%s_%dkHz_RF.wav"
                                                        % (datetime.datetime.utcnow().strftime("%Y%m%d_%H%M%SZ"),
                                                        2 / 1000)))+"\n"+
                                       str(os.path.join(path,"SDR_%s_%dkHz_RF.iq"
                                       % (datetime.datetime.utcnow().strftime("%Y%m%d_%H%M%SZ"),
                                       2 / 1000))))

    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Внимание',
                                     "Продолжть?",
                                     QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            event.accept() # Если пользователь подтверждает, то окно закрывается
        else:
            event.ignore() # Если нет, то событие игнорируется


if __name__ == '__main__':
    global window0
    app = QApplication(sys.argv)
    window0 = Window0()
    window0.show()
    sys.exit(app.exec_())