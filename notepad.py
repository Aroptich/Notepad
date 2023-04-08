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
        self.ui.btn_del.clicked.connect(self.del_row_table)

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

        self.add_json(id, text_title, text_note, str(datetime.now().strftime("%d-%m-%Y %H:%M")))

        self.ui.field_note.clear()
        self.ui.lineEdit.clear()

    def create_json(self):
        if not os.path.isfile("Json/notes.json"):
            db = {"notes": []}
            with open("Json/notes.json", 'w', encoding="UTF-8") as file:
                json.dump(db, file)

    def add_json(self, id, title, note, date_time):
        new_data = {id: [title, note, date_time]}
        with open("Json/notes.json", encoding="UTF-8") as f:
            data = json.load(f)
            data['notes'].append(new_data)
            with open("Json/notes.json", 'w', encoding="UTF-8") as file:
                json.dump(data, file, ensure_ascii=False, indent=2)

    def read_json(self):
        if os.path.isfile("Json/notes.json"):
            with open("Json/notes.json", encoding="UTF-8") as file:
                data = json.load(file)
                print(data["notes"])
                for i in data["notes"]:
                    for k, v in i.items():
                        id = k
                        title, note, data_time = v
                        rowPosition = self.ui.table_notes.rowCount()
                        self.ui.table_notes.insertRow(rowPosition)
                        self.ui.table_notes.setItem(rowPosition, 1, QTableWidgetItem(title))
                        self.ui.table_notes.setItem(rowPosition, 0, QTableWidgetItem(id))
                        self.ui.table_notes.setItem(rowPosition, 2,
                                                    QTableWidgetItem(data_time))

    def del_json(self, id):
        if os.path.isfile("Json/notes.json"):
            with open("Json/notes.json", encoding="UTF-8") as file:
                data = json.load(file)
                data["notes"].pop(id)
                with open("Json/notes.json", 'w', encoding="UTF-8") as file:
                    json.dump(data, file, ensure_ascii=False, indent=2)


    def del_row_table(self):
        row = self.ui.table_notes.currentRow()
        if row > -1:
            self.del_json(row)
            self.ui.table_notes.removeRow(row)
            self.ui.table_notes.selectionModel().clearCurrentIndex()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Notepad()
    window.read_json()
    window.show()
    sys.exit(app.exec_())
