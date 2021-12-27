from ui import Ui_MainWindow
from src.slam import SLAM
from PyQt5 import QtCore, QtGui, QtWidgets
import sys

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    slam = SLAM(ui)
    sys.exit(app.exec_())
