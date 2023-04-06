import sys

from PyQt5.QtWidgets import QApplication, QMainWindow
from GUI.GUI import Ui_mainWindow

class Notepad(QApplication):
    def __init__(self):
        super(Notepad, self).__init__()
        self.ui = Ui_mainWindow()
        self.ui.setupUi(self)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = QMainWindow()
    ui = Ui_mainWindow()
    ui.setupUi(window)

    window.show()
    sys.exit(app.exec_())