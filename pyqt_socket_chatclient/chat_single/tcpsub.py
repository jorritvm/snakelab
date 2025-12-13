#! /usr/bin/python
from PyQt4.QtNetwork import *
from staticvar import *

#we create our own QTcpServer subclass
#this server creates a new socket for each incomming connection

class TcpServer(QTcpServer):
    def __init__(self, parent=None):
        QTcpServer.__init__(self, parent)
                
                
    def incomingConnection(self, socketId):
        socket = Socket(self)
        socket.setSocketDescriptor(socketId)
        
        
        
class Socket(QTcpSocket):
    def __init__(self, parent = None):
        QTcpSocket.__init__(self, parent)
        self.readyRead.connect(self.readRequest)
        self.disconnected.connect(self.deleteLater)
        self.nextBlockSize = 0
        
        
    def readRequest(self):
        stream = QDataStream(self)
        stream.setVersion(QDATASTREAMVERSION)
        
        if self.nextBlockSize == 0:
            if self.bytesAvailable() < SIZEOF_UINT:
                return
            self.nextBlockSize = stream.readUInt16()
        if self.bytesAvailable() < self.nextBlockSize:
            return

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
        self.write(reply)
        pass