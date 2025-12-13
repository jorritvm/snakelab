## THE SERVER ECHOES WHAT HE RECEIVES TO EVERYONE

import sys
import datetime
from PyQt5.Qt import *
from tcpsub import *
from staticvar import *

class ServerDlg(QPushButton):

    def __init__(self, parent=None):
        QPushButton.__init__(self, parent)
        self.setupGui()        
        self.setupTCPServer()
   
    def setupGui(self):
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowTitle("Server")
        font = self.font()
        font.setPointSize(24)
        self.setText("Shutdown Server")
        self.clicked.connect(self.close)
    
    def setupTCPServer(self):
        #self.connections = []
        self.tcpServer = TcpServer(self)               
        if not self.tcpServer.listen(QHostAddress("0.0.0.0"), PORT):
            QMessageBox.critical(self, "Server", "Failed to start server.\nReason: %s" % self.tcpServer.errorString())
            self.close()
            return

class TcpServer(QTcpServer):
    """ 
    de TCP server beheert zijn connecties in verschillende threads
    er zijn enkele functies aanwezig om broadcasts te doen 
    """
    def __init__(self, parent=None):
        QTcpServer.__init__(self, parent)
                
                
    def incomingConnection(self, socketId):
        thread = ThreadedConnection(socketId, self)
        thread.finished.connect(thread.deleteLater)
        thread.start()
        
    def newMessage(self):
        pass
    
    def broadcastMessage(self):
        pass

class ThreadedConnection(QThread):

    #lock = QReadWriteLock() to use with shared resources, declared above the first class

    def __init__(self, socketId, parent):
        QThread.__init__(self, parent)
        self.socketId = socketId
        
    def run(self):
        self.socket = QTcpSocket()
        if not self.socket.setSocketDescriptor(self.socketId):
            #self.emit(SIGNAL("error(int)"), self.socket.error()) #FIX THIS
            return
        while self.socket.state() == QAbstractSocket.ConnectedState:
            #we get here every time there we handled an entire request
            nextBlockSize = 0
            stream = QDataStream(self.socket)
            stream.setVersion(QDATASTREAMVERSION)
            #retreive the request size
            while True:
                self.socket.waitForReadyRead(-1)
                if self.socket.bytesAvailable() >= SIZEOF_UINT:
                    nextBlockSize = stream.readUInt16()
                    break
            #wait until the entire request has arrived
            if self.socket.bytesAvailable() < nextBlockSize:
                while True:
                    self.socket.waitForReadyRead(-1)
                    if self.socket.bytesAvailable() >= nextBlockSize:
                        break
            #now process the request
            mtype = ""
            nick = ""
            value = ""
            
            mtype = stream.readQString()
            nick = stream.readQString()
            value = stream.readQString()  
                
            if mtype == "SENDMSG":
                self.sendReply(mtype, nick, value)
        
        
    def sendReply(self, mtype, nick, value):
        reply = QByteArray()
        stream = QDataStream(reply, QIODevice.WriteOnly)
        stream.setVersion(QDATASTREAMVERSION)
        stream.writeUInt16(0)
        stream.writeQString(mtype)
        stream.writeQString(nick)
        stream.writeQString(value)
        stream.device().seek(0)
        stream.writeUInt16(reply.size() - SIZEOF_UINT)
        self.socket.write(reply)
        
        
app = QApplication(sys.argv)
form = ServerDlg()
form.show()
form.move(0, 0)
app.exec_()