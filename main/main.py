from PyQt5 import QtCore, QtWebSockets,  QtNetwork, QtWidgets
from PyQt5.QtCore import (QThread, pyqtSignal)
from PyQt5.QtWidgets import (QWidget, QHBoxLayout, QApplication, QLabel)
from PyQt5.QtGui import QPixmap

from http.server import HTTPServer, SimpleHTTPRequestHandler

import os
import time
import sys
import qrcode
import re
from os import curdir, sep

WS_PORT = None

# websocket server
class SocketServer(QtCore.QObject):
    def __init__(self, parent):
        super(QtCore.QObject, self).__init__(parent)

        self.clients = []
        self.server = QtWebSockets.QWebSocketServer(parent.serverName(), parent.secureMode(), parent)
        if self.server.listen(QtNetwork.QHostAddress.Any, 0):
            global WS_PORT
            WS_PORT = self.server.serverPort()
            print(self.server.serverName()+' : '+self.server.serverAddress().toString()+':'+str(self.server.serverPort()))
        else:
            print('error')
        self.serverThread = QThread()
        # self.server.moveToThread(self.serverThread)
        self.server.newConnection.connect(self.onNewConnection)

        print(self.server.isListening())

    def onNewConnection(self):
        self.clientConnection = self.server.nextPendingConnection()
        self.clientConnection.textMessageReceived.connect(self.processTextMessage)

        self.clientConnection.binaryMessageReceived.connect(self.processBinaryMessage)
        self.clientConnection.disconnected.connect(self.socketDisconnected)

        self.clients.append(self.clientConnection)

    def processTextMessage(self,  message):
        if (self.clientConnection):
            print("receive:", message);

            if message == 'prev':
                os.system("""osascript -e 'tell app "System Events" to key code 126'""")
            elif message == 'next':
                os.system("""osascript -e 'tell app "System Events" to key code 125'""")
            elif message == 'start':
                os.system("""osascript -e 'tell application "Keynote" to key code {58,55,35}'""")
            elif message == 'end':
                os.system("""osascript -e 'tell application "Keynote" to key code {58,55,35}'""")
            # 此处部分情况下会报错，先暂时不做返回处理
            # self.clientConnection.sendTextMessage(message)

    def processBinaryMessage(self,  message):
        if (self.clientConnection):
            self.clientConnection.sendBinaryMessage(message)

    def socketDisconnected(self):
        if (self.clientConnection):
            self.clients.remove(self.clientConnection)
            self.clientConnection.deleteLater()


class myHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        # print(self.path
        global WS_PORT
        root = os.path.abspath(os.path.dirname(__file__))
        htmlPath= root + "/static/index.html"
        htmlpage =open(htmlPath, 'rb')
        if self.path == '/':
            self.send_response(301)
            self.send_header('Location','/index.html?query='+str(WS_PORT))
            self.end_headers()
            self.wfile.write(htmlpage.read())
        elif re.match(r'/index.html', self.path):
            self.send_response(200)
            self.end_headers()
            self.wfile.write(htmlpage.read())
        else:
            self.send_response(200)
            self.end_headers()
            self.wfile.write(open(root + '/static' + self.path, 'rb').read())

# static server
class StaticServer(QThread):
    myfinish = pyqtSignal(int)

    def run(self):
        Handler = myHandler
        HOST, PORT = '0.0.0.0', 0
        self._server = HTTPServer(
            (HOST, PORT),
            Handler
        )
        ip, port = self._server.server_address
        print("Static Server:", ip, port)
        self.myfinish.emit(port)
        self._server.serve_forever()
    

    

    def stop(self):
        self._server.shutdown()
        self._server.socket.cloase()
        self.wait()



# ui window
class RemoteUI(QWidget):
    def __init__(self):
        super().__init__()
        self.httpStatic = StaticServer(self)
        self.httpStatic.start() #这里写run()无法渲染出UI窗口，原因见这里：https://www.qtcentre.org/threads/4486-QThread-run()-Vs-start()

        # time.sleep(2)
        self.httpStatic.myfinish.connect(self.initUI)
    
    def initUI(self, port):
        # global PORTNUM
        IP = os.popen("ifconfig|grep 'inet '|grep -v '127.0'|xargs|awk -F '[ :]' '{print $2}'").readline().rstrip()
        print('QRCode: http://%s:%s/' % (IP, port))
        img = qrcode.make('http://%s:%s/' % (IP, port))
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
    window = RemoteUI()

    serverObject = QtWebSockets.QWebSocketServer('Socket', QtWebSockets.QWebSocketServer.NonSecureMode)
    server = SocketServer(serverObject)
    serverObject.closed.connect(app.quit)

    sys.exit(app.exec_())