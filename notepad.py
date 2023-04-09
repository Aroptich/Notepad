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
        self.ui.btn_edit.clicked.connect(self.edit_notes)
        self.ui.btn_save.clicked.connect(self.find_notes)

    def main(self):
        if os.path.isfile("Json/notes.json"):
            notes = self.read_json()
        else:
            self.create_json()
            notes = self.read_json()
        self.view_table(notes)
        self.ui.field_note.clear()
        self.ui.lineEdit.clear()

    def create_note(self):
        notes = self.read_json()
        print(notes)
        rowPosition = self.ui.table_notes.rowCount()
        self.ui.table_notes.insertRow(rowPosition)

        title = self.ui.lineEdit.text()
        note = self.ui.field_note.toPlainText()
        id = str(self.assignment_id(notes))
        date_time = datetime.now().strftime("%d-%m-%Y %H:%M")
        self.ui.table_notes.setItem(rowPosition, 1, QTableWidgetItem(title))
        self.ui.table_notes.setItem(rowPosition, 2, QTableWidgetItem(str(date_time)))
        self.ui.table_notes.setItem(rowPosition, 0, QTableWidgetItem(id))
        self.add_json(id, title, note, date_time)

    def create_json(self):
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
        with open("Json/notes.json", encoding="UTF-8") as file:
            data = json.load(file)
            return data['notes']

    def view_table(self, notes):
        for i in notes:
            for k, v in i.items():
                id = k
                title, note, data_time = v
                rowPosition = self.ui.table_notes.rowCount()
                self.ui.table_notes.insertRow(rowPosition)
                self.ui.table_notes.setItem(rowPosition, 1, QTableWidgetItem(title))
                self.ui.table_notes.setItem(rowPosition, 0, QTableWidgetItem(id))
                self.ui.table_notes.setItem(rowPosition, 2, QTableWidgetItem(data_time))

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

    def edit_notes(self):
        note = self.ui.table_notes.currentRow()
        if os.path.isfile("Json/notes.json"):
            with open("Json/notes.json", encoding="UTF-8") as file:
                data = json.load(file)
                list_values = data["notes"][note]
                for temp_list in list_values.values():
                    title, note, date_time = temp_list
                    self.ui.field_note.setPlainText(note)
                    self.ui.lineEdit.setText(title)
                    return temp_list



    def assignment_id(self, notes: list[dict]) -> int:
        try:
            id = 1
            if notes == []:
                id = 1
                return id
            temp_id = []
            for i in notes:
                for k, v in i.items():
                    temp_id.append(int(k))
            while True:
                if id not in temp_id:
                    return id
                id += 1
        except ValueError:
            print("Неверный формат записей")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Notepad()
    window.main()
    window.show()
    sys.exit(app.exec_())
