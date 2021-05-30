#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import struct
import socket
import configparser
import time
import numpy as np
from PyQt5.QtWidgets import QListView, QAction
from PyQt5 import QtWidgets, uic, QtCore, QtGui

class MainWindow(QtWidgets.QMainWindow):
    """
    A main window class
    """
    def __init__(self, *args, **kwargs):
        """
        A function for connecting actions and creating a main window
        """
        super(MainWindow, self).__init__(*args, **kwargs)
        
        #self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # SOCK_DGRAM is UDP

        self.destroyed.connect(lambda: self._on_destroyed())         # connect some actions to exit
        # Load the UI Page
        uic.loadUi('gui/main_window.ui', self)                       # Design file

        # configuration data
        path_to_main = os.path.abspath(os.getcwd())
        path_config_file = os.path.join(path_to_main,'config.ini')
        config = configparser.ConfigParser()
        config.read(path_config_file)

        UDP_IP = str(config['DEFAULT']['UDP_IP'])
        UDP_PORT = int(config['DEFAULT']['UDP_PORT'])

        # Connection of different action to different Menus and Buttons
        self.button_initialize.clicked.connect(self.initialize)
        self.button_initialize.setStyleSheet("QPushButton {border-radius: 4px; background-color: rgb(63, 63, 97);\
         border-style: outset; color: rgb(193, 202, 227);}\
          QPushButton:pressed {background-color: rgb(211, 194, 78); ; border-style: inset}")
        self.button_off.clicked.connect(self.turn_off)
        self.button_off.setStyleSheet("QPushButton {border-radius: 4px; background-color: rgb(63, 63, 97);\
         border-style: outset; color: rgb(193, 202, 227);}\
          QPushButton:pressed {background-color: rgb(211, 194, 78); ; border-style: inset}")
        self.button_telemetry.clicked.connect(self.telemetry)
        self.button_telemetry.setStyleSheet("QPushButton {border-radius: 4px; background-color: rgb(63, 63, 97);\
         border-style: outset; color: rgb(193, 202, 227);}\
          QPushButton:pressed {background-color: rgb(211, 194, 78); ; border-style: inset}")

        # text labels
        self.label.setStyleSheet("QLabel { color : rgb(193, 202, 227); }")
        self.label_2.setStyleSheet("QLabel { color : rgb(193, 202, 227); }")
        self.label_3.setStyleSheet("QLabel { color : rgb(193, 202, 227); }")
        self.label_4.setStyleSheet("QLabel { color : rgb(193, 202, 227); }")
        self.label_5.setStyleSheet("QLabel { color : rgb(193, 202, 227); }")
        self.label_6.setStyleSheet("QLabel { color : rgb(193, 202, 227); }")
        self.label_7.setStyleSheet("QLabel { color : rgb(193, 202, 227); }")
        self.label_8.setStyleSheet("QLabel { color : rgb(193, 202, 227); }")

        self.telemetry_text.setStyleSheet("QPlainTextEdit { color : rgb(193, 202, 227); }")

        # Spinboxes
        self.Att1_prd.valueChanged.connect(self.att1_prd)
        self.Att1_prd.setStyleSheet("QDoubleSpinBox { color : rgb(193, 202, 227); }")
        self.Att2_prd.valueChanged.connect(self.att2_prd)
        self.Att2_prd.setStyleSheet("QDoubleSpinBox { color : rgb(193, 202, 227); }")
        self.Fv_ctrl.valueChanged.connect(self.fv_ctrl)
        self.Fv_ctrl.setStyleSheet("QDoubleSpinBox { color : rgb(193, 202, 227); }")
        self.Fv_prm.valueChanged.connect(self.fv_prm)
        self.Fv_prm.setStyleSheet("QDoubleSpinBox { color : rgb(193, 202, 227); }")
        self.Att_prm.valueChanged.connect(self.att_prm)
        self.Att_prm.setStyleSheet("QSpinBox { color : rgb(193, 202, 227); }")
        self.K_prm.valueChanged.connect(self.k_prm)
        self.K_prm.setStyleSheet("QSpinBox { color : rgb(193, 202, 227); }")
        self.Synt.valueChanged.connect(self.synt)
        self.Synt.setStyleSheet("QSpinBox { color : rgb(193, 202, 227); }")

        # Radio Buttons
        self.cutoff_1.clicked.connect(self.cutoff_changed_1)
        self.cutoff_1.setStyleSheet("QRadioButton { color : rgb(193, 202, 227); }")
        self.cutoff_2.clicked.connect(self.cutoff_changed_2)
        self.cutoff_2.setStyleSheet("QRadioButton { color : rgb(193, 202, 227); }")
        self.cutoff_3.clicked.connect(self.cutoff_changed_3)
        self.cutoff_3.setStyleSheet("QRadioButton { color : rgb(193, 202, 227); }")

        self.initialize()


    def _on_destroyed(self):
        """
        A function to do some actions when the main window is closing.
        """
        pass
        #sock.shutdown(socket.SHUT_RDWR)
        #sock.close()
        #self.process_python.close()

    def quit(self):
        """
        A function to quit the programm
        """
        #sock.shutdown(socket.SHUT_RDWR)
        #sock.close()
        sys.exit()

    def att1_prd(self):
        """
        A function to send a value to the attenuator 1 in the PRD channel
        """

        param = self.Att1_prd.value()
        temp = 2*param
        MESSAGE = b'0x15' + b'0x01' + struct.pack(">B", int(temp))
        # all variats give the same result. Struct.pack is the fastest
        #print( (int(temp)).to_bytes(1, byteorder='big') )
        #print( struct.pack(">B", int(temp)) )
        #print( bytes([int(temp)]) )

        # binary format
        #print("{0:{fill}8b}".format(10, fill='0'))
        
        #sock.sendto(MESSAGE, (UDP_IP, UDP_PORT))    

    def att2_prd(self):
        """
        A function to send a value to the attenuator 2 in the PRD channel
        """

        param = self.Att2_prd.value()
        temp = 2*param
        MESSAGE = b'0x16' + b'0x01' + struct.pack(">B", int(temp))
        
        #sock.sendto(MESSAGE, (UDP_IP, UDP_PORT))    

    def fv_ctrl(self):
        """
        A function to send a value to the phase shifter in the CTRL channel
        """

        param = self.Fv_ctrl.value()
        temp = param/5.625
        MESSAGE = b'0x17' + b'0x01' + struct.pack(">B", int(temp))
        
        #sock.sendto(MESSAGE, (UDP_IP, UDP_PORT))

    def fv_prm(self):
        """
        A function to send a value to the phase shifter in the PRM channel
        """

        param = self.Fv_prm.value()
        temp = param/5.625
        MESSAGE = b'0x19' + b'0x01' + struct.pack(">B", int(temp))
        
        #sock.sendto(MESSAGE, (UDP_IP, UDP_PORT))

    def att_prm(self):
        """
        A function to send a value to the attenuator 3 in the PRM channel
        """

        param = self.Att_prm.value()
        temp = param/2
        MESSAGE = b'0x1c' + b'0x01' + struct.pack(">B", int(temp))
        
        #sock.sendto(MESSAGE, (UDP_IP, UDP_PORT))    

    def k_prm(self):
        """
        A function to change the amplification coefficient in the PRM channel
        """

        param = self.Att_prm.value()
        temp = param
        MESSAGE = b'0x1a' + b'0x01' + struct.pack(">B", int(temp))
        
        #sock.sendto(MESSAGE, (UDP_IP, UDP_PORT))  

    def cutoff_changed_2(self):
        """
        A function to change the amplification coefficient in the PRM channel
        """

        MESSAGE = b'0x1b' + b'0x01' + b'0x00'
        #sock.sendto(MESSAGE, (UDP_IP, UDP_PORT))   

    def cutoff_changed_3(self):
        """
        A function to change the amplification coefficient in the PRM channel
        """

        MESSAGE = b'0x1b' + b'0x01' + b'0x01'
        #sock.sendto(MESSAGE, (UDP_IP, UDP_PORT))

    def cutoff_changed_1(self):
        """
        A function to change the amplification coefficient in the PRM channel
        """

        MESSAGE = b'0x1b' + b'0x01' + b'0x02'
        #sock.sendto(MESSAGE, (UDP_IP, UDP_PORT))

    def string2bits(self, s = ''):
        # maybe useless
        return [bin(ord(x))[2:].zfill(8) for x in s]

    def synt(self):
        """
        A function to change the frequency
        """

        param = self.Synt.value()
        temp = str(param)
        if len( temp ) == 4:
            temp = '0' + '0' + '0' + '0' + temp
        elif len( temp ) == 5:
            temp = '0' + '0' + '0' + temp

        #print( ''.join(self.string2bits(temp)) )
        MESSAGE = b'0x04' + b'0x08' + temp.encode()
        
        #sock.sendto(MESSAGE, (UDP_IP, UDP_PORT))  

    def initialize(self):
        """
        A function to initialize a bridge.
        """

        MESSAGE = b'0x27' + b'0x01' + b'0x00'

        #sock.sendto(MESSAGE, (UDP_IP, UDP_PORT))  

    def turn_off(self):
        """
         A function to turn off a bridge.
        """
        self.initialize()
        sock.shutdown(socket.SHUT_RDWR)
        sock.close()

    def telemetry(self):
        """
        A function to get the telemetry.
        """

        MESSAGE = b'0x0d' + b'0x08' + (0).to_bytes(8, byteorder='big')
        #sock.sendto(MESSAGE, (UDP_IP, UDP_PORT))

        #data_raw, addr = sock.recvfrom(8)                 # buffer size is 1024 bytes

        #data = data_raw.decode()
        #self.telemetry_text.appendPlainText( str(data) )

    def help(self):
        """
        A function to open a documentation
        """
        pass

def main():
    """
    A function to run the main window of the programm.
    """
    app = QtWidgets.QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
