import sys
from mainwidget import * # work on this!

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainwidget = mainwindow()
    mainwidget.show()
    sys.exit(app.exec_())