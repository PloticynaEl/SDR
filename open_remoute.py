import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QComboBox

class App2(QMainWindow):
    def __init__(self):
        super().__init__()
        #self.uifile_name = namfile
        uic.loadUi('window_remoute.ui',self)

        self.pushButton_choose.clicked.connect(self.pushButton_choose_func)
        self.pushButton_cancel.clicked.connect(self.pushButton_cancel_func)

        self.comboBox_choose.activated.connect(self.pushButton_cancel_func)
        self.textEdit_port.textChanged.connect(self.update_text)


    def pushButton_choose_func(self):
        pass

    def pushButton_cancel_func(self):
        print("запускаем окно настройки удаленного подключения")

    def update_text(self):

        text = self.textEdit_port.toPlainText()
        print(text)
        self.textEdit_port.textChanged.connect(self.update_text)

    def comboBox_activated(self, index):
        print("Activated index:", index)
        if index == 0:
            pass
        elif index == 1:
            self.show_remoute()
        elif index == 2:
            self.show_usb()

def start_add_remoute():
    print('start_add_remoute')
    ex2 = App2()
    ex2.show()
