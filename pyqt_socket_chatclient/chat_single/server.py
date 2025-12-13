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




app = QApplication(sys.argv)
form = ServerDlg()
form.show()
form.move(0, 0)
app.exec_()