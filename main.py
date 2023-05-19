import psycopg2
import sys

from PyQt5.QtWidgets import (QApplication, QWidget,
                             QTabWidget, QAbstractScrollArea,
                             QVBoxLayout, QHBoxLayout,
                             QTableWidget, QGroupBox,
                             QTableWidgetItem, QPushButton, QMessageBox)


class MainWindow(QWidget):
    def __init__(self):
        super(MainWindow, self).__init__()

        self._connect_to_db()

        self.setWindowTitle("Shedule")

        self.vbox = QVBoxLayout(self)

        self.tabs = QTabWidget(self)
        self.vbox.addWidget(self.tabs)

        self._create_shedule_tab()

        self._create_teachers_tab()

        self._create_subjects_tab()

    def _connect_to_db(self):
        self.conn = psycopg2.connect(database="laba_7_new",
                                     user="postgres",
                                     password="password",
                                     host="localhost",
                                     port="5432")

        self.cursor = self.conn.cursor()

    def _create_shedule_tab(self):
        self.shedule_tab = QWidget()
        self.tabs.addTab(self.shedule_tab, "Shedule")

        self.svbox = QVBoxLayout()
        self.shbox2 = QHBoxLayout()

        self.shedule_hbox = []
        for i in range(6):
            hbox = QHBoxLayout()
            self.svbox.addLayout(hbox)
            self.shedule_hbox.append(hbox)
        self.svbox.addLayout(self.shbox2)

        self.week_day = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday']
        self.groupboxes = []
        for i in range(6):
            groupbox = QGroupBox(self.week_day[i])
            self.shedule_hbox[i].addWidget(groupbox)
            self.groupboxes.append(groupbox)

        self._create_schedule_tables()

        self.update_shedule_button = QPushButton("Update")
        self.shbox2.addWidget(self.update_shedule_button)
        self.update_shedule_button.clicked.connect(self._update_shedule)


        self.shedule_tab.setLayout(self.svbox)


    def _create_schedule_tables(self):
        self.schedule_tables = []
        self.schedule_vbox = []
        for i in range(6):
            vbox = QVBoxLayout()
            self.schedule_vbox.append(vbox)
            table = QTableWidget()
            table.setColumnCount(7)
            table.setHorizontalHeaderLabels(["id", "subject", "start_time", "parity", "room_numb"])
            self.schedule_vbox[i].addWidget(table)
            self.schedule_tables.append(table)

            self._update_schedule_tables(table, i)

            self.groupboxes[i].setLayout(self.schedule_vbox[i])

    def _update_schedule_tables(self, table, i):
            self.cursor.execute("SELECT * FROM timetable WHERE day = %s ORDER BY parity, id", (self.week_day[i], ))
            records = list(self.cursor.fetchall())
            table.setRowCount(len(records) + 1)

            for j, r in enumerate(records):
                r = list(r)
                joinButton = QPushButton("Join")
                deleteButton = QPushButton("Delete")

                table.setItem(j, 0, QTableWidgetItem(str(r[0])))
                table.setItem(j, 1, QTableWidgetItem(str(r[2])))
                table.setItem(j, 2, QTableWidgetItem(str(r[3])))
                table.setItem(j, 3, QTableWidgetItem(str(r[4])))
                table.setItem(j, 4, QTableWidgetItem(str(r[5])))
                table.setCellWidget(j, 5, joinButton)
                table.setCellWidget(j, 6, deleteButton)

                joinButton.clicked.connect(lambda ch, num1=i, num2=j: self._edit_timetable(num1, num2))
                deleteButton.clicked.connect(lambda ch, num1=i, num2=j: self._delete_from_timetable(num1, num2))

            joinButton = QPushButton("Join")
            table.setCellWidget(len(records), 5, joinButton)
            joinButton.clicked.connect(lambda ch, num1=i, num2=len(records): self._add_to_timetable(num1, num2))
            table.resizeRowsToContents()
    def _add_to_timetable(self, num1, num2):
        row = list()
        print(num1, num2)
        for i in range(self.schedule_tables[num1].columnCount()):
            try:
                row.append(self.schedule_tables[num1].item(num2, i).text())
            except:
                row.append(None)
        print(row)
        try:
            columns = ["id", "day", "subject", "start_time", "parity", "room_numb"]
            self.cursor.execute(
                f"INSERT INTO timetable({columns[0]}, {columns[1]}, {columns[2]}, {columns[3]}, {columns[4]}, {columns[5]}) values('{row[0]}', '{self.week_day[num1]}', '{row[1]}', '{row[2]}', '{row[3]}', '{row[4]}')")
            self.conn.commit()
        except:
            QMessageBox.about(self, "Error", "Enter all fields")

    def _edit_timetable(self, num1, num2):
        row = list()
        for i in range(self.schedule_tables[num1].columnCount()):
            try:
                row.append(self.schedule_tables[num1].item(num2, i).text())
            except:
                row.append(None)
        try:
            columns = ["id", "day", "subject", "start_time", "parity", "room_numb"]
            for i in range(1, 5):
                self.cursor.execute(f"UPDATE timetable SET {columns[i]} = '{row[i]}' WHERE id = '{row[0]}'")
                self.conn.commit()
        except:
            QMessageBox.about(self, "Error", "Enter all fields")

    def _delete_from_timetable(self, num1, num2):
        row = list()
        for i in range(self.schedule_tables[num1].columnCount()):
            try:
                row.append(self.schedule_tables[num1].item(num2, i).text())
            except:
                row.append(None)
        try:
            self.cursor.execute(f"DELETE from timetable where id = '{row[0]}'")
            self.conn.commit()
        except:
            QMessageBox.about(self, "Error", "Enter all fields")

    def _create_teachers_tab(self):
        self.teachers_tab = QWidget()
        self.tabs.addTab(self.teachers_tab, "Teachers")

        self.teachers_gbox = QGroupBox("teacher")

        self.tvbox = QVBoxLayout()
        self.thbox1 = QHBoxLayout()
        self.thbox2 = QHBoxLayout()

        self.tvbox.addLayout(self.thbox1)
        self.tvbox.addLayout(self.thbox2)

        self.thbox1.addWidget(self.teachers_gbox)

        self._create_teachers_table()

        self.update_teachers_button = QPushButton("Update")
        self.thbox2.addWidget(self.update_teachers_button)
        self.update_teachers_button.clicked.connect(self._update_shedule)

        self.teachers_tab.setLayout(self.tvbox)

    def _create_teachers_table(self):
        self.teachers_table = QTableWidget()
        self.teachers_table.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)

        self.teachers_table.setColumnCount(5)
        self.teachers_table.setHorizontalHeaderLabels(["id", "full_name", "subject"])

        self._update_teachers_table()

        self.ttvbox = QVBoxLayout()
        self.ttvbox.addWidget(self.teachers_table)
        self.teachers_gbox.setLayout(self.ttvbox)

    def _update_teachers_table(self):
        self.cursor.execute("SELECT * FROM teacher ORDER BY id")
        records = list(self.cursor.fetchall())

        self.teachers_table.setRowCount(len(records) + 1)

        for i, r in enumerate(records):
            r = list(r)
            joinButton = QPushButton("Join")
            deleteButton = QPushButton("Delete")

            self.teachers_table.setItem(i, 0, QTableWidgetItem(str(r[0])))
            self.teachers_table.setItem(i, 1, QTableWidgetItem(str(r[1])))
            self.teachers_table.setItem(i, 2, QTableWidgetItem(str(r[2])))
            self.teachers_table.setCellWidget(i, 3, joinButton)
            self.teachers_table.setCellWidget(i, 4, deleteButton)

            joinButton.clicked.connect(lambda ch, num=i: self._edit_teachers_table(num))
            deleteButton.clicked.connect(lambda ch, num=i: self._delete_from_teachers_table(num))

        joinButton = QPushButton("Join")
        self.teachers_table.setCellWidget(len(records), 3, joinButton)
        joinButton.clicked.connect(lambda ch, num=len(records): self._add_to_teachers_table(num))

        self.teachers_table.resizeRowsToContents()

    def _edit_teachers_table(self, num):
        row = list()
        for i in range(self.teachers_table.columnCount()):
            try:
                row.append(self.teachers_table.item(num, i).text())
            except:
                row.append(None)
        print(row, num)
        try:
            columns = ["id", "full_name", "subject"]
            for i in range(1, 2):
                self.cursor.execute(f"UPDATE teacher SET {columns[i]} = '{row[i]}' WHERE id = '{row[0]}'")
                self.conn.commit()
        except:
            QMessageBox.about(self, "Error", "Enter all fields")

    def _delete_from_teachers_table(self, num):
        row = list()
        for i in range(self.teachers_table.columnCount()):
            try:
                row.append(self.teachers_table.item(num, i).text())
            except:
                row.append(None)
        print(row, num)
        try:
            self.cursor.execute(f"DELETE from teacher where id = '{row[0]}'")
            self.conn.commit()
        except:
            QMessageBox.about(self, "Error", "Enter all fields")

    def _add_to_teachers_table(self, num):
        row = list()
        for i in range(self.teachers_table.columnCount()):
            try:
                row.append(self.teachers_table.item(num, i).text())
            except:
                row.append(None)
        print(row, num)
        try:
            columns = ["id", "full_name", "subject"]
            self.cursor.execute(
                f"INSERT INTO teacher({columns[0]}, {columns[1]}, {columns[2]}) values('{row[0]}', '{row[1]}', '{row[2]}')")
            self.conn.commit()
        except:
            QMessageBox.about(self, "Error", "Enter all fields")

    def _create_subjects_tab(self):
        self.subjects_tab = QWidget()
        self.tabs.addTab(self.subjects_tab, "Subjects")

        self.subjects_gbox = QGroupBox("subject")

        self.fvbox = QVBoxLayout()
        self.fhbox1 = QHBoxLayout()
        self.fhbox2 = QHBoxLayout()

        self.fvbox.addLayout(self.fhbox1)
        self.fvbox.addLayout(self.fhbox2)

        self.fhbox1.addWidget(self.subjects_gbox)

        self._create_subjects_table()

        self.update_subjects_button = QPushButton("Update")
        self.fhbox2.addWidget(self.update_subjects_button)
        self.update_subjects_button.clicked.connect(self._update_shedule)

        self.subjects_tab.setLayout(self.fvbox)

    def _create_subjects_table(self):
        self.subjects_table = QTableWidget()
        self.subjects_table.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)

        self.subjects_table.setColumnCount(3)
        self.subjects_table.setHorizontalHeaderLabels(["name"])

        self._update_subjects_table()

        self.ffvbox = QVBoxLayout()
        self.ffvbox.addWidget(self.subjects_table)
        self.subjects_gbox.setLayout(self.ffvbox)

    def _update_subjects_table(self):
        self.cursor.execute("SELECT * FROM subject ORDER BY name")
        records = list(self.cursor.fetchall())

        self.subjects_table.setRowCount(len(records) + 1)

        for i, r in enumerate(records):
            r = list(r)
            joinButton = QPushButton("Join")
            deleteButton = QPushButton("Delete")

            self.subjects_table.setItem(i, 0, QTableWidgetItem(str(r[0])))
            self.subjects_table.setCellWidget(i, 1, joinButton)
            self.subjects_table.setCellWidget(i, 2, deleteButton)

            joinButton.clicked.connect(lambda ch, num=i: self._edit_subjects_table(num))
            deleteButton.clicked.connect(lambda ch, num=i: self._delete_from_subjects_table(num))

        joinButton = QPushButton("Join")
        self.subjects_table.setItem(len(records), 0,  QTableWidgetItem(""))
        self.subjects_table.setCellWidget(len(records), 1, joinButton)
        self.subjects_table.setItem(len(records), 2, QTableWidgetItem())
        joinButton.clicked.connect(lambda ch, num=len(records): self._add_to_subjects_table(num))

        self.subjects_table.resizeRowsToContents()

    def _edit_subjects_table(self, num):
        row = list()
        for i in range(self.subjects_table.columnCount()):
            try:
                row.append(self.subjects_table.item(num, i).text())
            except:
                row.append(None)
        print(row, num)
        try:
            columns = ["name"]
            self.cursor.execute(f"UPDATE subject SET {columns[0]} = '{row[0]}' WHERE name = '{row[0]}'")
            self.conn.commit()
        except:
            QMessageBox.about(self, "Error", "Enter all fields")

    def _delete_from_subjects_table(self, num):
        row = self.subjects_table.item(num, 0).text()
        print(row)
        try:
            self.cursor.execute(f"DELETE from subject where name = '{row}'")
            self.conn.commit()
        except:
            QMessageBox.about(self, "Error", "Данный предмет нельзя удалить")

    def _add_to_subjects_table(self, num):
        row = list()
        for i in range(self.subjects_table.columnCount()):
            try:
                row.append(self.subjects_table.item(num, i).text())
            except:
                row.append(None)
        print(row, num)
        try:
            columns = ["name"]
            self.cursor.execute(f"INSERT INTO subject({columns[0]}) values('{row[0]}')")
            self.conn.commit()
        except:
            QMessageBox.about(self, "Error", "Enter all fields")

    def _update_shedule(self):
        for i, table in enumerate(self.schedule_tables):
            self._update_schedule_tables(table, i)
        self._update_teachers_table()
        self._update_subjects_table()


app = QApplication(sys.argv)
win = MainWindow()
win.show()
sys.exit(app.exec_())
