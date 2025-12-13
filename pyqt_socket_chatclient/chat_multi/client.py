#! /usr/bin/python
import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtNetwork import *
from staticvar import *

class Chatclient(QDialog):

    def __init__(self, parent=None):
        QDialog.__init__(self, parent)

        # Ititialize socket
        self.socket = QTcpSocket()

        # Initialize data IO variables
        self.nextBlockSize = 0
        self.request = None

        #create the GUI
        self.createGui()
        
        #connect the GUI signals
        self.connectGuiSignals()
        
        #connect the socket signals
        self.connectSocketSignals()
        
    
    def createGui(self):
        # Create widgets/layout
        self.browser = QTextBrowser()
        self.nick = QLineEdit("Nickname")
        self.lineedit = QLineEdit("Enter text here, dummy")
        self.lineedit.selectAll()
        self.connectButton = QPushButton("Connect")
        layout = QVBoxLayout()
        layout.addWidget(self.connectButton)
        layout.addWidget(self.nick)
        layout.addWidget(self.browser)
        layout.addWidget(self.lineedit)
        self.setLayout(layout)
        self.lineedit.setFocus()
        self.setWindowTitle("Client")
    
    
    def connectGuiSignals(self):
        # Signals and slots for line edit and connect button
        self.lineedit.returnPressed.connect(lambda: self.issueRequest("SENDMSG", self.nick.text(), self.lineedit.text()))
        self.connectButton.clicked.connect(self.connectToServer)
       
       
    def connectSocketSignals(self):
        # new style signals and slots
        self.socket.connected.connect(self.connectedToServer)
        self.socket.readyRead.connect(self.readFromServer)
        self.socket.disconnected.connect(self.serverHasStopped)
        self.socket.error.connect(self.serverHasError)
        
        
    def updateUi(self, text):
        #update GUI
        self.browser.append(text)

        
    def setButtonsEnabled(self, b):
        self.nick.setEnabled(b)
        self.connectButton.setEnabled(b)
    
    
    def connectToServer(self):
        # Create connection to server
        self.updateGui("Connecting to server...")
        self.socket.connectToHost("localhost", PORT)
        self.setButtonsEnabled(False)
    
    
    def connectedToServer(self):
        self.updateGui("Connected to server...")

        
    def issueRequest(self, mtype, nick=None, value=None):
        request = QByteArray()
        stream = QDataStream(self.request, QIODevice.WriteOnly)
        stream.setVersion(QDATASTREAMVERSION)
        stream.writeUInt16(0)
        stream.writeQString(mtype)
        stream.writeQString(nick)
        stream.writeQString(value)
        stream.device().seek(0)
        stream.writeUInt16(self.request.size() - SIZEOF_UINT)
        self.sendRequest(request)
    
    
    def sendRequest(self):
        self.socket.write(request)
        self.nextBlockSize = 0
        self.lineedit.setText("") # try to put this somewhere else

        
    def readFromServer(self):
        stream = QDataStream(self.socket)
        stream.setVersion(QDATASTREAMVERSION)

        while True:
            if self.nextBlockSize == 0:
                if self.socket.bytesAvailable() < SIZEOF_UINT:
                    break
                self.nextBlockSize = stream.readUInt16()
            if self.socket.bytesAvailable() < self.nextBlockSize:
                break
            mtype = ""
            nick = ""
            value = ""
            
            #receiving the message
            mtype = stream.readQString()
            nick = stream.readQString()
            value = stream.readQString()
            
            #do something with the received message here...
            if mtype == "SENDMSG":
                self.updateUi(nick + ": " + value)
            
            self.nextBlockSize = 0

            
    def serverHasStopped(self):
        self.updateUi("Server has stopped...")
        self.socket.close()
        self.setButtonsEnabled(True)

        
    def serverHasError(self):
        self.updateUi("Server error: {}".format(
                self.socket.errorString()))
        self.socket.close()
        self.setButtonsEnabled(True)
        
        
    def closeEvent(self, event):
        self.socket.close()
        event.accept()
    



app = QApplication(sys.argv)
form = Chatclient()
form.show()
app.exec_()