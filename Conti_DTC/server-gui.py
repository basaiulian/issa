#!/usr/bin/env python
import psutil
from PyQt4 import QtCore, QtGui
import socket
import os
import threading
import sys, time

HOST = 'localhost'
PORT = 5005

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
client = None

server_created_flag = False

dtc_to_check = "00"


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        global server_created_flag
        MainWindow.setObjectName("MainWindow")
        MainWindow.setFixedSize(600, 800)
        MainWindow.setWindowTitle('Server')
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        MainWindow.setCentralWidget(self.centralwidget)

        self.centralwidget.setStyleSheet("background-color:white;")

        self.dtc1_state, self.dtc2_state, self.dtc3_state, self.dtc4_state, self.all_dtcs_state = 0, 0, 0, 0, 0

        # Start server button
        self.server_start = QtGui.QPushButton(MainWindow)
        self.server_start.setText("Start server")
        self.server_start.setStyleSheet("font: bold; font-size: 15px;")
        self.server_start.setGeometry(QtCore.QRect(200, 170, 200, 40))
        self.server_start.clicked.connect(self.start_server)

        ### Set DTC

        # Set DTC1
        self.dtc1 = QtGui.QPushButton(MainWindow)
        self.dtc1.setText("Set DTC1 active")
        self.dtc1.setStyleSheet("font: bold; font-size: 15px;")
        self.dtc1.setGeometry(QtCore.QRect(70, 300, 200, 40))
        self.dtc1.clicked.connect(lambda: self.set_dtc1(7, 0.1))

        # Set DTC2
        self.dtc2 = QtGui.QPushButton(MainWindow)
        self.dtc2.setText("Set DTC2 active")
        self.dtc2.setStyleSheet("font: bold; font-size: 15px;")
        self.dtc2.setGeometry(QtCore.QRect(70, 370, 200, 40))
        self.dtc2.clicked.connect(lambda: self.set_dtc2(6, 0.1))

        # Set DTC3
        self.dtc3 = QtGui.QPushButton(MainWindow)
        self.dtc3.setText("Set DTC3 active")
        self.dtc3.setStyleSheet("font: bold; font-size: 15px;")
        self.dtc3.setGeometry(QtCore.QRect(70, 440, 200, 40))
        self.dtc3.clicked.connect(lambda: self.set_dtc3(5, 0.1))

        # Set DTC4
        self.dtc4 = QtGui.QPushButton(MainWindow)
        self.dtc4.setText("Set DTC4 active")
        self.dtc4.setStyleSheet("font: bold; font-size: 15px;")
        self.dtc4.setGeometry(QtCore.QRect(70, 510, 200, 40))
        self.dtc4.clicked.connect(lambda: self.set_dtc4(4, 0.1))

        ### LEDS
        # Led 1
        self.led1_state = QtGui.QLabel(MainWindow)
        self.led1_state.setGeometry(QtCore.QRect(330, 300, 40, 40))

        # Led 2
        self.led2_state = QtGui.QLabel(MainWindow)
        self.led2_state.setGeometry(QtCore.QRect(330, 370, 40, 40))

        # Led 3
        self.led3_state = QtGui.QLabel(MainWindow)
        self.led3_state.setGeometry(QtCore.QRect(330, 441, 40, 40))

        # Led 4
        self.led4_state = QtGui.QLabel(MainWindow)
        self.led4_state.setGeometry(QtCore.QRect(330, 510, 40, 40))

        # Set all DTC's
        self.set_all_dtc = QtGui.QPushButton(MainWindow)
        self.set_all_dtc.setText("Set all DTC")
        self.set_all_dtc.setStyleSheet("font: bold; font-size: 15px;")
        self.set_all_dtc.setGeometry(QtCore.QRect(70, 580, 200, 40))
        self.set_all_dtc.clicked.connect(self.set_all)

        # Start server label
        self.server_label = QtGui.QLabel(self.centralwidget)
        self.server_label.setGeometry(QtCore.QRect(200, 210, 200, 40))
        self.server_label.setStyleSheet("font:bold;font-size: 15px;qproperty-alignment: AlignCenter;")

        # Continental image
        self.conti_label = QtGui.QLabel(self.centralwidget)
        self.conti_label.setGeometry(QtCore.QRect(110, 30, 400, 100))
        self.conti_label.setStyleSheet("qproperty-alignment: AlignCenter;")
        continental = QtGui.QImage(QtGui.QImageReader('./rsz_conti.png').read())
        self.conti_label.setPixmap(QtGui.QPixmap(continental))

        self.statusbar = QtGui.QStatusBar(MainWindow)
        MainWindow.setStatusBar(self.statusbar)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        MainWindow.show()

    ############################### EXERCISE 0 ###############################
    def start_server(self):
        self.set_all_dtc.setText('Set all DTC')

        self.dtc1.setText("Set DTC1 active")
        self.dtc2.setText("Set DTC2 active")
        self.dtc3.setText("Set DTC3 active")
        self.dtc4.setText("Set DTC4 active")

        self.dtc1.setStyleSheet("background-color:green;border-radius:5px;font: bold; font-size: 15px;")
        self.dtc2.setStyleSheet("background-color:green;border-radius:5px;font: bold; font-size: 15px;")
        self.dtc3.setStyleSheet("background-color:green;border-radius:5px;font: bold; font-size: 15px;")
        self.dtc4.setStyleSheet("background-color:green;border-radius:5px;font: bold; font-size: 15px;")

        self.led1_state.setStyleSheet('')
        self.led2_state.setStyleSheet('')
        self.led3_state.setStyleSheet('')
        self.led4_state.setStyleSheet('')
        ''' Complete with necessary code'''

        global server, client

        # Waiting for client
        server.listen(1)

        # Accepting client's connection
        client, addr = server.accept()

        print("Client with address " + str(addr) + " connected.")

        for _ in range(50):
            recv_data = self.recv()

    ############################### EXERCISE 1 ###############################
    def recv_handler(self, stop_event):
        global client
        recv_data = client.recv(1024).decode("utf-8")
        # print("Received data:", recv_data)
        diag_mode = ""
        if recv_data == '0x3E0':
            diag_mode = 0
        elif recv_data == '0x3E01':
            diag_mode = 1
        if diag_mode != "":
            print(diag_mode)

        global dtc_to_check

        if str(recv_data).__contains__('0x22'):
            dtc_to_check = str(recv_data)[-2:]
            if dtc_to_check == '01':
                self.read_dtc1()
            elif dtc_to_check == '02':
                self.read_dtc2()
            elif dtc_to_check == '03':
                self.read_dtc3()
            elif dtc_to_check == '04':
                self.read_dtc4()

        if str(recv_data).__contains__('0x2E'):
            dtc_to_set = str(recv_data)[-3:-1]
            if dtc_to_set == '01':
                self.set_led0(dtc_to_set)
            elif dtc_to_set == '02':
                self.set_led1(dtc_to_set)
            elif dtc_to_set == '03':
                self.set_led2(dtc_to_set)
            elif dtc_to_set == '04':
                self.set_led3(dtc_to_set)

    def recv(self):
        self.stop_event = threading.Event()
        self.c_thread = threading.Thread(target=self.recv_handler, args=(self.stop_event,))
        self.c_thread.start()

    ############################### EXERCISE 2 ###############################
    # DTC1
    def set_dtc1(self, led, bright):
        if self.dtc1_state == 0:
            self.dtc1.setStyleSheet("background-color:red;border-radius:5px;font: bold; font-size: 15px;")
            self.dtc1_state = 1
            self.dtc1.setText("Set DTC1 inactive")
        elif self.dtc1_state == 1:
            self.dtc1_state = 0
            self.dtc1.setStyleSheet("background-color:green;border-radius:5px;font: bold; font-size: 15px;")
            self.dtc1.setText("Set DTC1 active")

    # DTC2
    def set_dtc2(self, led, bright):
        if self.dtc2_state == 0:
            self.dtc2.setStyleSheet("background-color:red;border-radius:5px;font: bold; font-size: 15px;")
            self.dtc2_state = 1
            self.dtc2.setText("Set DTC2 inactive")
        elif self.dtc2_state == 1:
            self.dtc2_state = 0
            self.dtc2.setStyleSheet("background-color:green;border-radius:5px;font: bold; font-size: 15px;")
            self.dtc2.setText("Set DTC2 active")

    # DTC3
    def set_dtc3(self, led, bright):
        if self.dtc3_state == 0:
            self.dtc3.setStyleSheet("background-color:red;border-radius:5px;font: bold; font-size: 15px;")
            self.dtc3_state = 1
            self.dtc3.setText("Set DTC3 inactive")
        elif self.dtc3_state == 1:
            self.dtc3_state = 0
            self.dtc3.setStyleSheet("background-color:green;border-radius:5px;font: bold; font-size: 15px;")
            self.dtc3.setText("Set DTC3 active")

    # DTC4
    def set_dtc4(self, led, bright):
        if self.dtc4_state == 0:
            self.dtc4.setStyleSheet("background-color:red;border-radius:5px;font: bold; font-size: 15px;")
            self.dtc4_state = 1
            self.dtc4.setText("Set DTC4 inactive")
        elif self.dtc4_state == 1:
            self.dtc4_state = 0
            self.dtc4.setStyleSheet("background-color:green;border-radius:5px;font: bold; font-size: 15px;")
            self.dtc4.setText("Set DTC4 active")

    def set_all(self):
        if self.all_dtcs_state == 0:
            self.dtc1.setStyleSheet("background-color:red;border-radius:5px;font: bold; font-size: 15px;")
            self.dtc2.setStyleSheet("background-color:red;border-radius:5px;font: bold; font-size: 15px;")
            self.dtc3.setStyleSheet("background-color:red;border-radius:5px;font: bold; font-size: 15px;")
            self.dtc4.setStyleSheet("background-color:red;border-radius:5px;font: bold; font-size: 15px;")
            self.dtc1.setText("Set DTC1 inactive")
            self.dtc2.setText("Set DTC2 inactive")
            self.dtc3.setText("Set DTC3 inactive")
            self.dtc4.setText("Set DTC4 inactive")
            self.all_dtcs_state, self.dtc1_state, self.dtc2_state, self.dtc3_state, self.dtc4_state = 1, 1, 1, 1, 1
        elif self.all_dtcs_state == 1:
            self.dtc1.setStyleSheet("background-color:green;border-radius:5px;font: bold; font-size: 15px;")
            self.dtc2.setStyleSheet("background-color:green;border-radius:5px;font: bold; font-size: 15px;")
            self.dtc3.setStyleSheet("background-color:green;border-radius:5px;font: bold; font-size: 15px;")
            self.dtc4.setStyleSheet("background-color:green;border-radius:5px;font: bold; font-size: 15px;")
            self.dtc1.setText("Set DTC1 active")
            self.dtc2.setText("Set DTC2 active")
            self.dtc3.setText("Set DTC3 active")
            self.dtc4.setText("Set DTC4 active")
            self.all_dtcs_state, self.dtc1_state, self.dtc2_state, self.dtc3_state, self.dtc4_state = 0, 0, 0, 0, 0

    ############################### EXERCISE 3 ###############################
    def read_dtc1(self):
        if self.dtc1_state == 1:
            data_to_send = "25500"
        elif self.dtc1_state == 0:
            data_to_send = "02550"
        client.send(bytes('0x62' + '01' + data_to_send, "utf-8"))

    def read_dtc2(self):
        if self.dtc2_state == 1:
            data_to_send = "25500"
        elif self.dtc2_state == 0:
            data_to_send = "02550"
        client.send(bytes('0x62' + '02' + data_to_send, "utf-8"))

    def read_dtc3(self):
        if self.dtc3_state == 1:
            data_to_send = "25500"
        elif self.dtc3_state == 0:
            data_to_send = "02550"
        client.send(bytes('0x62' + '03' + data_to_send, "utf-8"))

    def read_dtc4(self):
        if self.dtc4_state == 1:
            data_to_send = "25500"
        elif self.dtc4_state == 0:
            data_to_send = "02550"
        client.send(bytes('0x62' + '04' + data_to_send, "utf-8"))

    ############################### EXERCISE 4 ###############################
    def set_led0(self, data):
        self.set_dtc1(7, 0.1)
        client.send(bytes('0x6E' + data + str(self.dtc1_state), "utf-8"))

    def set_led1(self, data):
        self.set_dtc2(6, 0.1)
        client.send(bytes('0x6E' + data + str(self.dtc2_state), "utf-8"))

    def set_led2(self, data):
        self.set_dtc3(5, 0.1)
        client.send(bytes('0x6E' + data + str(self.dtc3_state), "utf-8"))

    def set_led3(self, data):
        self.set_dtc4(4, 0.1)
        client.send(bytes('0x6E' + data + str(self.dtc4_state), "utf-8"))


##########################################################################


class MyWindow(QtGui.QMainWindow):
    def closeEvent(self, event):
        result = QtGui.QMessageBox.question(self,
                                            "Confirm Exit",
                                            "Are you sure you want to exit ?",
                                            QtGui.QMessageBox.Yes | QtGui.QMessageBox.No)

        if result == QtGui.QMessageBox.Yes:
            event.accept()
        elif result == QtGui.QMessageBox.No:
            event.ignore()

    def center(self):
        frameGm = self.frameGeometry()
        screen = QtGui.QApplication.desktop().screenNumber(QtGui.QApplication.desktop().cursor().pos())
        centerPoint = QtGui.QApplication.desktop().screenGeometry(screen).center()
        frameGm.moveCenter(centerPoint)
        self.move(frameGm.topLeft())


def kill_proc_tree(pid, including_parent=True):
    parent = psutil.Process(pid)
    if including_parent:
        parent.kill()


def main():
    global server_created_flag
    import sys
    global app
    app = QtGui.QApplication(sys.argv)
    MainWindow = MyWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.center()

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()

me = os.getpid()
kill_proc_tree(me)
