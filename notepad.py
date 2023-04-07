import sys
from datetime import datetime

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from GUI.GUI import Ui_mainWindow


class Notepad(QMainWindow):
    def __init__(self):
        super(Notepad, self).__init__()
        self.ui = Ui_mainWindow()
        self.ui.setupUi(self)

        self.ui.btn_create.clicked.connect(self.create_note)

    def create_note(self):
        rowPosition = self.ui.table_notes.rowCount()
        self.ui.table_notes.insertRow(rowPosition)

        text_title = self.ui.lineEdit.text()
        text_note = self.ui.field_note.toPlainText()

        write_title = self.ui.table_notes.setItem(rowPosition, 0, QTableWidgetItem(text_title))
        write_date_time = self.ui.table_notes.setItem(rowPosition, 1,
                                                      QTableWidgetItem(str(datetime.now().strftime("%d-%m-%Y %H:%M"))))

        self.ui.field_note.clear()
        self.ui.lineEdit.clear()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Notepad()
    window.show()
    sys.exit(app.exec_())
