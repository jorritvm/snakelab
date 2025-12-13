'''
Created on 21-jul-2009

@author: Jorrit
'''

from PyQt4.QtGui import *
from PyQt4.QtCore import *

from qrc_resource import *


class test(QWidget):
    
    def __init__(self,parent=None):
        super(test, self).__init__(parent)
        
        x = QPushButton()
        x.setIcon(QIcon(":/alfa.jpg"))
        
        y = QPushButton()
        y.setIcon(QIcon(":/beta.png"))
        
        layout = QHBoxLayout(self)
        layout.addWidget(x)
        layout.addWidget(y)