#! /usr/bin/python
from PyQt4.QtNetwork import *
from staticvar import *

#in this file we create a threaded tcp server with blocking I/O in each thread!

class TcpServer(QTcpServer):
    def __init__(self, parent=None):
        QTcpServer.__init__(self, parent)
                
                
    def incomingConnection(self, socketId):
        thread = ServerThread(socketId, self)
        thread.finished.connect(thread.deleteLater)
        thread.start()
        
        
    def incomingConnection(self, socketId):
        socket = Socket(self)
        socket.setSocketDescriptor(socketId)
        
        

class ServerThread(QThread):

    #lock = QReadWriteLock() to use with shared resources, declared above the first class

    def __init__(self, socketId, parent):
        QThread.__init__(self, parent)
        self.socketId = socketId
        
    def run(self):
        self.socket = QTcpSocket()
        if not self.socket.setSocketDescriptor(self.socketId):
            self.emit(SIGNAL("error(int)"), socket.error()) #FIX THIS
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