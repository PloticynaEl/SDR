from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QVBoxLayout, QWidget
import sys
from PyQt5 import uic
from PyQt5.QtGui import QTextCursor, QFont
from PyQt5.QtWidgets import QApplication, QDialog, QMainWindow, QMessageBox, QFileDialog, QTextEdit
import re
import subprocess
import SoapySDR
import fmfm_wav_iq
import configparser


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
        uic.loadUi('win_server.ui',self)
        self.run_button_remoute.clicked.connect(self.button_run)
        self.cancel_button_remoute.clicked.connect(self.button_cancel)
        self.pushButton_1.clicked.connect(self.push_1)
        self.pushButton_2.clicked.connect(self.push_2)
        self.pushButton_3.clicked.connect(self.push_3)
        self.pushButton_4.clicked.connect(self.push_4)
        self.pushButton_5.clicked.connect(self.push_5)
        self.pushButton_6.clicked.connect(self.push_6)
        self.pushButton_7.clicked.connect(self.push_7)
        self.pushButton_8.clicked.connect(self.push_8)
        self.pushButton_9.clicked.connect(self.push_9)
        self.pushButton_0.clicked.connect(self.push_0)
        self.pushButton_x.clicked.connect(self.clear)
        self.font = QFont("Arial", 20)
        self.textEdit_port_server.setFont(self.font)

        # Вызываемые окна
        self.window_run = Window_run()

    def button_cancel(self):
        self.hide()
        mainwindow.show()
        self.textEdit_port_server.setText("___.__.__.___: ____")

    def button_run(self):
        self.hide()
        address_run = self.textEdit_port_server.toPlainText()
        self.window_run.show()
    def cursor_input(self, input):
        text = self.textEdit_port_server.toPlainText()
        position = 0
        for i in range(len(text)):
            if text[i] == "_":
                position = i
                break
        self.textEdit_port_server.setText( text[:position] + input + text[position + 1:])
    def clear(self):
        text = self.textEdit_port_server.toPlainText()
        position = -1
        for i in range(len(text)):
            if text[i] == "_":
                position = i
                break
        if position == 4 or position == 7 or position == 10:
            self.textEdit_port_server.setText(text[:position - 2] + "_." + text[position :])
        elif position == 14:
            self.textEdit_port_server.setText(text[:position - 2] + "_:" + text[position :])
        elif position == -1:
            self.textEdit_port_server.setText(text[:position - 1] +  "_")
        else:
            self.textEdit_port_server.setText(text[:position - 1] + "__" + text[position + 1:])
    def push_1(self):
        self.cursor_input('1')
    def push_2(self):
        self.cursor_input('2')
    def push_3(self):
        self.cursor_input('3')
    def push_4(self):
        self.cursor_input('4')
    def push_5(self):
        self.cursor_input('5')
    def push_6(self):
        self.cursor_input('6')
    def push_7(self):
        self.cursor_input('7')
    def push_8(self):
        self.cursor_input('8')
    def push_9(self):
        self.cursor_input('9')
    def push_0(self):
        self.cursor_input('0')

class Window_run(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('win_run.ui', self)
        self.stop_button_run.clicked.connect(self.button_stop)

    def button_stop(self):
        self.hide()
        mainwindow.window_server.show()

class Window_client(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('win_client.ui', self)
        self.device = None
        self.config = None
        self.pushButton_conti_client.clicked.connect(self.button_continue)
        self.comboBox_devices.activated.connect(self.comboBox_activated)
        self.window_info = Window_info()
        self.window_remoute = Window_remoute()
        self.window_usb = Window_usb()
        self.window_soapy = Window_soapy()
        self.window_demod = Window_demod()

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
        self.configuration_file()
        if (self.device is not None):
            self.hide()
            self.configuration_file()
            self.window_demod.show()

    def configuration_file(self):
        self.config = configparser.ConfigParser()
        self.config.add_section('SIGNAL_SOURCE CONFIG')
        self.config.set('SIGNAL_SOURCE CONFIG', 'sampling_frequency', self.comboBox_first_samp_freq.currentText())
        self.config.set('SIGNAL_SOURCE CONFIG', 'driver', 'sss')
        with open('myconfig.conf', 'w') as config_file:
            self.config.write(config_file)


class Window_remoute(QWidget): #REMOUTE
    def __init__(self):
        super().__init__()
        uic.loadUi('win_remoute.ui',self)
        self.continue_button_remoute.clicked.connect(self.pushButton_continue_button_remoute)
        self.cancel_button_remoute.clicked.connect(self.button_cancel)
        self.pushButton_1.clicked.connect(self.push_1)
        self.pushButton_2.clicked.connect(self.push_2)
        self.pushButton_3.clicked.connect(self.push_3)
        self.pushButton_4.clicked.connect(self.push_4)
        self.pushButton_5.clicked.connect(self.push_5)
        self.pushButton_6.clicked.connect(self.push_6)
        self.pushButton_7.clicked.connect(self.push_7)
        self.pushButton_8.clicked.connect(self.push_8)
        self.pushButton_9.clicked.connect(self.push_9)
        self.pushButton_0.clicked.connect(self.push_0)
        self.pushButton_x.clicked.connect(self.clear)
        self.font = QFont("Arial", 20)
        self.textEdit_port_remoute.setFont(self.font)

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
        self.textEdit_port_remoute.setText("___.__.__.___: ____")

    def cursor_input(self, input):
        text = self.textEdit_port_remoute.toPlainText()
        position = 0
        for i in range(len(text)):
            if text[i] == "_":
                position = i
                break
        self.textEdit_port_remoute.setText( text[:position] + input + text[position + 1:])

    def clear(self):
        text = self.textEdit_port_remoute.toPlainText()
        position = -1
        for i in range(len(text)):
            if text[i] == "_":
                position = i
                break
        if position == 4 or position == 7 or position == 10:
            self.textEdit_port_remoute.setText(text[:position - 2] + "_." + text[position :])
        elif position == 14:
            self.textEdit_port_remoute.setText(text[:position - 2] + "_:" + text[position :])
        elif position == -1:
            self.textEdit_port_remoute.setText(text[:position - 1] +  "_")
        else:
            self.textEdit_port_remoute.setText(text[:position - 1] + "__" + text[position + 1:])
    def push_1(self):
        self.cursor_input('1')
    def push_2(self):
        self.cursor_input('2')
    def push_3(self):
        self.cursor_input('3')
    def push_4(self):
        self.cursor_input('4')
    def push_5(self):
        self.cursor_input('5')
    def push_6(self):
        self.cursor_input('6')
    def push_7(self):
        self.cursor_input('7')
    def push_8(self):
        self.cursor_input('8')
    def push_9(self):
        self.cursor_input('9')
    def push_0(self):
        self.cursor_input('0')
    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Внимание',
                                     "Продолжить?",
                                     QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

class Window_usb(QWidget): #USB
    def __init__(self):
        super().__init__()
        uic.loadUi('win_usb.ui',self)
        self.device = None
        self.cancel_button_usb.clicked.connect(self.button_cancel)
        self.update_button_usb.clicked.connect(self.pushButton_update_func)
        self.continue_button_usb.clicked.connect(self.pushButton_choose_func)
        self.window_error = Window_connection_error()

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
        devices =['airspy', 'bladerf', 'hackrf', 'lime', 'osmosdr',
                  'redpitaya', 'rfspace', 'rtlsdr', 'sdrplay']

        if len(self.listWidget_usb.selectedIndexes()) > 0:
            string = self.listWidget_usb.selectedIndexes()[0].data()
            new_string = string.lower()
            result = new_string.split()
            for i in result:
                for ii in devices:
                    if i == ii:
                        self.device = ii
            if (self.device is not None):
                mainwindow.window_client.device = SDRDevice(self.device)
                mainwindow.window_client.device.print_info()
                mainwindow.window_client.comboBox_devices.addItem(self.listWidget_usb.selectedIndexes()[0].data())
                mainwindow.window_client.comboBox_devices.setCurrentIndex(
                    mainwindow.window_client.comboBox_devices.count() - 1)
                self.hide()
                mainwindow.window_client.window_info.print()
                mainwindow.window_client.window_info.show()
            else:
                self.hide()
                mainwindow.window_client.window_usb.window_error.textEdit_device.setText(str(string))
                mainwindow.window_client.window_usb.window_error.show()

        #self.device.print_info()

    def button_cancel(self):
        self.close()
        self.hide()
        mainwindow.window_client.show()
    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Внимание',
                                     "Продолжть?",
                                     QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            event.accept() # Если пользователь подтверждает, то окно закрывается
        else:
            event.ignore() # Если нет, то событие игнорируется

class Window_connection_error(QWidget): #USB
    def __init__(self):
        super().__init__()
        uic.loadUi('win_connection_error.ui',self)
        self.cancel_button.clicked.connect(self.button_cancel)

    def button_cancel(self):
        self.close()
        self.hide()
        mainwindow.window_client.show()

class Window_soapy(QDialog): #SoapySDR(USB)
    def __init__(self):
        super().__init__()
        uic.loadUi('win_usb.ui',self)
        self.device = None
        self.cancel_button_usb.clicked.connect(self.button_cancel)
        self.update_button_usb.clicked.connect(self.pushButton_update_func)
        self.continue_button_usb.clicked.connect(self.pushButton_choose_func)
        self.window_error = Window_connection_error()

    def pushButton_update_func(self):
        self.listWidget_usb.clear()
        for d in SoapySDR.Device.enumerate(''):
            self.listWidget_usb.addItem(str(d['label'] ))

    def pushButton_choose_func(self):
        devices = ['airspy', 'bladerf', 'hackrf', 'lime', 'osmosdr',
                   'redpitaya', 'rfspace', 'rtlsdr', 'sdrplay']

        if len(self.listWidget_usb.selectedIndexes()) > 0:
            string = self.listWidget_usb.selectedIndexes()[0].data()
            new_string = string.lower()
            result = new_string.split()
            for i in result:
                for ii in devices:
                    if i == ii:
                        self.device = ii
            if (self.device is not None):
                mainwindow.window_client.device = SDRDevice(self.device)
                mainwindow.window_client.device.print_info()
                mainwindow.window_client.comboBox_devices.addItem(self.listWidget_usb.selectedIndexes()[0].data())
                mainwindow.window_client.comboBox_devices.setCurrentIndex(
                    mainwindow.window_client.comboBox_devices.count() - 1)
                self.hide()
                mainwindow.window_client.window_info.print()
                mainwindow.window_client.window_info.show()
            else:
                self.hide()
                self.window_error.textEdit_device.setText(str(string))
                self.window_error.show()


    def button_cancel(self):
        self.close()
        self.hide()
        mainwindow.window_client.show()

    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Внимание',
                                     "Продолжть?",
                                     QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            event.accept() # Если пользователь подтверждает, то окно закрывается
        else:
            event.ignore() # Если нет, то событие игнорируется

class Window_info(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('win_info.ui',self)
        self.continue_button_info.clicked.connect(self.button_continue)

    def print(self):
        if (fmfm_wav_iq.REMOUTE == False):
            self.text2 = mainwindow.window_client.device.get_text()
            self.textEdit.setText(str(self.text2))

    def button_continue(self):
        self.hide()
        mainwindow.window_client.show()

    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Внимание',
                                     "Продолжть?",
                                     QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            event.accept() # Если пользователь подтверждает, то окно закрывается
        else:
            event.ignore() # Если нет, то событие игнорируется

class Window_demod(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('win_demodulation.ui', self)
        # self.pushButton_cancel.clicked.connect(lambda: self.close())
        if (fmfm_wav_iq.REMOUTE == False):
            print("print")
            #self.device = SDRDevice('sdrplay')
            #for i in self.device.sample_rates:
            #    self.comboBox_sampl.addItem(str(i))
            #self.comboBox_sampl.setCurrentIndex(0)
        self.cancel_button_demod.clicked.connect(self.button_cancel)
        self.continue_button_demod.clicked.connect(self.start_DSP)
        #self.checkBox.stateChanged.connect(self.onStateChanged)
        
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
        mainwindow.window_client.show()

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
        self.device = SoapySDR.Device(dict(driver=self.soapy_device))

    def get_text(self):
        text = "#######################################################\n"
        text += "Driver Key:" +  str(self.device.getDriverKey()) + "\n"
        text += "#######################################################\n"
        text += "Hardware Key: " + str(self.device.getHardwareKey()) + "\n"
        text += "#######################################################\n"
        text += "Hardware Info: \n"
        text += str(self.device.getHardwareInfo()) + "\n"
        text += "#######################################################\n"
        channels = list(range(self.device.getNumChannels(SoapySDR.SOAPY_SDR_RX)))
        text += "Channels:" + str(channels) + "\n"
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

    def print_info(self):
        channels = list(range(self.device.getNumChannels(SoapySDR.SOAPY_SDR_RX)))
        ch = channels[0]
        self.sample_rates = self.device.listSampleRates(SoapySDR.SOAPY_SDR_RX, ch)
        for i in self.sample_rates:
            mainwindow.window_client.comboBox_first_samp_freq.addItem(str(i))
        mainwindow.window_client.comboBox_first_samp_freq.setCurrentIndex(0)

        bandwidths = list(map(lambda r: int(r.maximum()), self.device.getBandwidthRange(SoapySDR.SOAPY_SDR_RX, ch)))
        for i in bandwidths:
            mainwindow.window_client.comboBox_bandwidth.addItem(str(i))
        mainwindow.window_client.comboBox_bandwidth.setCurrentIndex(0)

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