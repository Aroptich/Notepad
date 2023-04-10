import os.path
import sys
import json
from datetime import datetime
from email.mime import image

from PyQt5 import QtGui
from PyQt5.QtWidgets import *
from GUI.GUI import Ui_mainWindow


class Notepad(QMainWindow, ):
    """Класс Notepad представляет из себя мини-приложение, которое позволяет по средствам API редактировать, создавать
    удалять заметки и сохранять все заметки в файл json. В классе реализовано GUI"""
    def __init__(self):
        super(Notepad, self).__init__()
        self.ui = Ui_mainWindow()
        self.ui.setupUi(self)

        self.ui.btn_create.clicked.connect(self.create_note)
        self.ui.btn_del.clicked.connect(self.del_row_table)
        self.ui.btn_edit.clicked.connect(self.edit_notes)
        self.ui.btn_save.clicked.connect(self.save_changes)

    def main(self):
        if os.path.isfile("Json/notes.json"):
            notes = self.read_json()
        else:
            self.create_json()
            notes = self.read_json()
        self.view_table(notes)
        self.ui.field_note.clear()
        self.ui.lineEdit.clear()

    def create_note(self) -> None:
        """Функция создает запись"""
        notes = self.read_json()
        # Отследивание строки в таблице QTableWidget
        rowPosition = self.ui.table_notes.rowCount()
        self.ui.table_notes.insertRow(rowPosition)

        title = self.ui.lineEdit.text()
        note = self.ui.field_note.toPlainText()
        id = str(self.assignment_id(notes))
        date_time = datetime.now().strftime("%d-%m-%Y %H:%M")
        # Запись данных из полей(QlineEdit, QTextEdit) в таблицу
        self.ui.table_notes.setItem(rowPosition, 1, QTableWidgetItem(title))
        self.ui.table_notes.setItem(rowPosition, 2, QTableWidgetItem(str(date_time)))
        self.ui.table_notes.setItem(rowPosition, 0, QTableWidgetItem(id))
        # Добавление данных в json-файл введенных пользователем
        self.add_json(title, note)
        # Очистка полей ввода
        self.ui.field_note.clear()
        self.ui.lineEdit.clear()

    def create_json(self) -> None:
        """Функция создает json-файл в указанной директории"""
        db = {"notes": []}
        with open("Json/notes.json", 'w', encoding="UTF-8") as file:
            json.dump(db, file)

    def add_json(self, title: str, note: str) -> None:
        """Функция принимает на вход данные с полей ввода"""
        # Чтение данных с json-файла
        notes = self.read_json()
        # Присваивание id записи
        id = self.assignment_id(notes)
        date_time = datetime.now().strftime("%d-%m-%Y %H:%M")
        new_data = {id: [title, note, date_time]}
        with open("Json/notes.json", encoding="UTF-8") as f:
            data = json.load(f)
            data['notes'].append(new_data)
            with open("Json/notes.json", 'w', encoding="UTF-8") as file:
                json.dump(data, file, ensure_ascii=False, indent=2)

    def read_json(self) -> list[dict]:
        """Функция считывет json-файл и возвращает список словарей"""
        with open("Json/notes.json", encoding="UTF-8") as file:
            data = json.load(file)
            return data['notes']

    def view_table(self) -> None:
        """Функция отображает данные заметок в GUI из json-файла в таблицу"""
        # Считывание данных из json-файла
        notes = self.read_json()
        for i in notes:
            for k, v in i.items():
                id = k
                title, note, data_time = v
                rowPosition = self.ui.table_notes.rowCount()
                self.ui.table_notes.insertRow(rowPosition)
                self.ui.table_notes.setItem(rowPosition, 1, QTableWidgetItem(title))
                self.ui.table_notes.setItem(rowPosition, 0, QTableWidgetItem(id))
                self.ui.table_notes.setItem(rowPosition, 2, QTableWidgetItem(data_time))

    def del_json(self, id: int) -> None:
        """Функция получает на вход id записи и удаляет ее из json-файла"""
        if os.path.isfile("Json/notes.json"):
            with open("Json/notes.json", encoding="UTF-8") as file:
                data = json.load(file)
                data["notes"].pop(id)
                with open("Json/notes.json", 'w', encoding="UTF-8") as file:
                    json.dump(data, file, ensure_ascii=False, indent=2)

    def del_row_table(self) -> None:
        """Функция удаляет запись из таблицы в GUI"""
        # Определение выбраной строки в таблице в GUI
        row = self.ui.table_notes.currentRow()
        if row > -1:
            self.del_json(row)
            self.ui.table_notes.removeRow(row)
            self.ui.table_notes.selectionModel().clearCurrentIndex()

    def edit_notes(self) -> tuple[list[dict], int]:
        """Функция возвращает данные об выделенной заметке для ее редактривания"""
        row = self.ui.table_notes.currentRow()
        if os.path.isfile("Json/notes.json"):
            with open("Json/notes.json", encoding="UTF-8") as file:
                data = json.load(file)
                list_values = data["notes"][row]
                for temp_list in list_values.values():
                    title, note, date_time = temp_list
                    self.ui.field_note.setPlaceholderText(note)
                    self.ui.lineEdit.setPlaceholderText(title)
                    return list_values, row

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

    def save_changes(self):

        data_note, row = self.edit_notes()
        self.del_json(row)
        title = self.ui.lineEdit.text()
        note = self.ui.field_note.toPlainText()
        if title == "" or note == "":
            title = self.ui.lineEdit.placeholderText()
            note = self.ui.field_note.placeholderText()
        print(title)
        note = self.ui.field_note.toPlainText()
        print(note)
        date_time = datetime.now().strftime("%d-%m-%Y %H:%M")

        self.add_json(title, note, date_time)
        self.ui.table_notes.clearContents()
        self.view_table()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Notepad()
    window.setWindowIcon((QtGui.QIcon("icons/icon-notebook.ico")))
    window.setStyleSheet("QMainWindow {background-color: rgba(251,206,177, 0.5);}")
    window.main()
    window.show()
    sys.exit(app.exec_())
