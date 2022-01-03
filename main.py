from src.ui.ui import Ui_MainWindow
from src.ui.slamwindow import SLAMWindow
from PyQt5 import QtCore, QtGui, QtWidgets
import sys


if __name__ == "__main__":

    # Create the window and setup the UI
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()

    # Create and run the application
    window = SLAMWindow(ui)
    sys.exit(app.exec_())