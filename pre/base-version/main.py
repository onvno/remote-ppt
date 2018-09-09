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
from aiohttp import web
import socketio
import eventlet
import threading
import time

portNum = 8990
exitFlag = 0
 

sio = socketio.AsyncServer()
apps = web.Application()
sio.attach(apps)

async def index(request):
    """Serve the client-side application."""
    with open('index.html') as f:
        return web.Response(text=f.read(), content_type='text/html')

@sio.on('connect')
def connect(sid, environ):
    print("connect ", sid)

@sio.on('chat')
async def message(sid, data):
    print("message ", data)
    if data == "prev":
        print('prev!')
        # cmd = """osascript -e 'tell app "Finder" to sleep'"""
        # os.system("""osascript -e 'tell app "Finder" to sleep'""")
        os.system("""osascript -e 'tell app "System Events" to key code 126'""")
    else:
        print('next!')
        # cmd = """osascript -e 'tell app "System Events" to key code 125'"""
        os.system("""osascript -e 'tell app "System Events" to key code 125'""")
    await sio.emit('reply', data)

@sio.on('disconnect')
def disconnect(sid):
    print('disconnect ', sid)

apps.router.add_static('/static', 'static')
apps.router.add_get('/', index)


class HttpStatic(QThread):
    def run(self):
        sio = socketio.AsyncServer()
        app = web.Application()
        sio.attach(app)

        async def index(request):
            """Serve the client-side application."""
            with open('index.html') as f:
                return web.Response(text=f.read(), content_type='text/html')

        @sio.on('connect')
        def connect(sid, environ):
            print("connect ", sid)

        @sio.on('chat')
        async def message(sid, data):
            print("message ", data)
            if data == "prev":
                print('prev!')
                # cmd = """osascript -e 'tell app "Finder" to sleep'"""
                # os.system("""osascript -e 'tell app "Finder" to sleep'""")
                os.system("""osascript -e 'tell app "System Events" to key code 126'""")
            else:
                print('next!')
                # cmd = """osascript -e 'tell app "System Events" to key code 125'"""
                os.system("""osascript -e 'tell app "System Events" to key code 125'""")
            await sio.emit('reply', data)

        @sio.on('disconnect')
        def disconnect(sid):
            print('disconnect ', sid)

        app.router.add_static('/static', 'static')
        app.router.add_get('/', index)
        web.run_app(app)
        # global portNum
        # HOST, PORT = '0.0.0.0', 0
        # self._server = HTTPServer(
        #     (HOST, PORT),
        #     SimpleHTTPRequestHandler
        # )
        # ip, port = self._server.server_address
        # portNum = port
        # print(ip, port, portNum)
        # self._server.serve_forever()
        






# class HttpStatic(QThread):
    # def run(self):
    #     global portNum
    #     HOST, PORT = '0.0.0.0', 0
    #     self._server = HTTPServer(
    #         (HOST, PORT),
    #         SimpleHTTPRequestHandler
    #     )
    #     ip, port = self._server.server_address
    #     portNum = port
    #     print(ip, port, portNum)
    #     self._server.serve_forever()
        
        
    
    # def stop(self):
    #     self._server.shutdown()
    #     self._server.socket.cloase()
    #     self.wait()


class Example(QWidget):

    def __init__(self):
        super().__init__()
        # self.httpStatic = HttpStatic(self)
        # self.httpStatic.run()
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
    sys.exit(app.exec_(),web.run_app(apps, port=portNum))
    


