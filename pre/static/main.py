#!/usr/bin/python3
# -*- coding: utf-8 -*-

# from PyQt5.QtWidgets import (QWidget, QHBoxLayout, QLabel, QApplication)
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from http.server import HTTPServer, SimpleHTTPRequestHandler

import sys
import os
import qrcode
import socket

portNum = 3000

class HttpStatic(QThread):
    def run(self):
        global portNum
        HOST, PORT = '0.0.0.0', 0
        self._server = HTTPServer(
            (HOST, PORT),
            SimpleHTTPRequestHandler
        )
        ip, port = self._server.server_address
        portNum = port
        print(ip, port, portNum)
        self._server.serve_forever()
        
        
    
    def stop(self):
        self._server.shutdown()
        self._server.socket.cloase()
        self.wait()


class Example(QWidget):

    def __init__(self):
        super().__init__()
        self.httpStatic = HttpStatic(self)
        self.httpStatic.start()
        self.initUI()
        

    def initUI(self):      
        # 显示二维码
        global portNum
        IP = os.popen("ifconfig|grep 'inet '|grep -v '127.0'|xargs|awk -F '[ :]' '{print $2}'").readline().rstrip()
        print(IP, portNum, ',test')
        img = qrcode.make('http://%s:%s/' % (IP, portNum))
        img.save('lee.png')
        hbox = QHBoxLayout(self)
        pixmap = QPixmap("lee.png")

        lbl = QLabel(self)
        lbl.setPixmap(pixmap)

        hbox.addWidget(lbl)
        self.setLayout(hbox)

        self.move(300, 200)
        self.resize(330, 330)
        self.setWindowTitle('Remote PPT')
        self.show()        


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())
