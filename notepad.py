import os.path
import sys
import json
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
        id = rowPosition + 1

        write_title = self.ui.table_notes.setItem(rowPosition, 1, QTableWidgetItem(text_title))
        write_date_time = self.ui.table_notes.setItem(rowPosition, 2,
                                                      QTableWidgetItem(str(datetime.now().strftime("%d-%m-%Y %H:%M"))))
        write_id = self.ui.table_notes.setItem(rowPosition, 0, QTableWidgetItem(str(rowPosition + 1)))

        self.create_json()
        self.add_json(id, text_title, text_note)

        self.ui.field_note.clear()
        self.ui.lineEdit.clear()

    def create_json(self):
        if not os.path.isfile("Json/notes.json"):
            db = {"notes": []}
            with open("Json/notes.json", 'w', encoding="cp1251") as file:
                json.dump(db, file)

    def add_json(self, id, title, note):
        new_data = {id: [title, note]}
        with open("Json/notes.json", encoding="cp1251") as f:
            data = json.load(f)
            data['notes'].append(new_data)
            print(data)
            with open("Json/notes.json", 'w', encoding="cp1251") as file:
                json.dump(data, file, ensure_ascii=False, indent=2)



if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Notepad()
    window.show()
    sys.exit(app.exec_())
