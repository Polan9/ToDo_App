import sys
import numpy as np
from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QDate
from PyQt5.QtWidgets import QListView, QApplication, QWidget, QVBoxLayout
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtCore import QModelIndex
import time
from PyQt5 import QtCore, QtGui, QtWidgets
import sqlite3


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(507, 614)
        self.db = sqlite3.connect('Baza_danych.db')
        self.cursor = self.db.cursor()
        try:
            self.cursor.execute("""

                                    CREATE TABLE tasks (
                                    name string,
                                    data_dodania string,
                                    deadline string,
                                    stan string)

                                    """)
        except sqlite3.OperationalError:
            print("Tabela juz istnieje")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.Main_listWidget = QtWidgets.QListWidget(self.centralwidget)
        self.Main_listWidget.setGeometry(QtCore.QRect(0, 150, 511, 211))
        self.Main_listWidget.setObjectName("Main_listWidget")
        self.Info_listWidget = QtWidgets.QLabel(self.centralwidget)
        self.Info_listWidget.setGeometry(QtCore.QRect(0, 370, 511, 201))
        self.Info_listWidget.setObjectName("Info_listWidget")
        self.info_deadline = QtWidgets.QLabel(self.centralwidget)
        self.info_deadline.setGeometry(QtCore.QRect(0, 370, 511, 180))
        self.checkbox_info = QtWidgets.QLabel(self.centralwidget)
        self.checkbox_info.setGeometry(QtCore.QRect(0, 390, 511, 180))
        self.checkbox_info_napis = QtWidgets.QLabel(self.centralwidget)
        self.checkbox_info_napis.setGeometry(QtCore.QRect(0, 80, 111, 100))
        self.checkbox_info_napis.setText("Wykonane?")
        self.checkbox = QtWidgets.QCheckBox(self.centralwidget)
        self.checkbox.setGeometry(QtCore.QRect(0, 60, 111, 100))
        self.checkbox_info_napis2 = QtWidgets.QLabel(self.centralwidget)
        self.checkbox_info_napis2.setGeometry(QtCore.QRect(405, 80, 111, 100))
        self.checkbox_info_napis2.setText("Usunac Wykoane?")
        self.checkbox2 = QtWidgets.QCheckBox(self.centralwidget)
        self.checkbox2.setGeometry(QtCore.QRect(390, 60, 111, 100))
        self.checkbox_button2 = QtWidgets.QPushButton(self.centralwidget)
        self.checkbox_button2.setGeometry(QtCore.QRect(410, 100, 91, 19))
        self.checkbox_button2.setObjectName("Zatwierdz")
        self.checkbox_button2.clicked.connect(self.zatwierdz_wyswietlanie)
        self.Dodaj = QtWidgets.QPushButton(self.centralwidget)
        self.Dodaj.setGeometry(QtCore.QRect(0, 60, 111, 23))
        self.Dodaj.setObjectName("Dodaj")
        self.Dodaj.clicked.connect(self.Dodawanie)
        self.usun = QtWidgets.QPushButton(self.centralwidget)
        self.usun.setGeometry(QtCore.QRect(130, 60, 101, 23))
        self.usun.setObjectName("usun")
        self.usun.clicked.connect(self.usuwanie)
        self.Dodaj_deadline = QtWidgets.QPushButton(self.centralwidget)
        self.Dodaj_deadline.setGeometry(QtCore.QRect(270, 60, 91, 23))
        self.Dodaj_deadline.setObjectName("Dodaj_deadline")
        self.Dodaj_deadline.clicked.connect(self.Deadline)
        self.Zapisz = QtWidgets.QPushButton(self.centralwidget)
        self.Zapisz.setGeometry(QtCore.QRect(400, 60, 101, 23))
        self.Zapisz.setObjectName("Pokaz info")
        self.Zapisz.clicked.connect(self.update)
        self.Task_input = QtWidgets.QLineEdit(self.centralwidget)
        self.Task_input.setGeometry(QtCore.QRect(2, 10, 231, 20))
        self.Task_input.setText("")
        self.Task_input.setObjectName("Task_input")
        self.Deadline_input = QtWidgets.QLineEdit(self.centralwidget)
        self.Deadline_input.setGeometry(QtCore.QRect(270, 10, 231, 20))
        self.Deadline_input.setObjectName("Deadline_input")
        MainWindow.setCentralWidget(self.centralwidget)
        self.save_button = QtWidgets.QPushButton(self.centralwidget)
        self.save_button.setGeometry(QtCore.QRect(210, 100, 91, 19))
        self.save_button.setObjectName("Zapisz")
        self.save_button.clicked.connect(self.save)
        self.checkbox_button = QtWidgets.QPushButton(self.centralwidget)
        self.checkbox_button.setGeometry(QtCore.QRect(15, 100, 91, 19))
        self.checkbox_button.setObjectName("Zatwierdz")
        self.checkbox_button.clicked.connect(self.zatwierdz_wykonane)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 507, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        self.zaznaczony = self.Main_listWidget.currentRow()
        self.deadline_text = self.Deadline_input.text
        self.lista = []
        self.lista_deadline = []
        self.lista_wykonane = []
        self.lista_dat_dodania = []
        try:
            self.cursor.execute("""
                   select * 
                   from tasks
                   """)
            rows = self.cursor.fetchall()
            for r in rows:
                self.lista.append(r[0])
                self.Main_listWidget.addItem(r[0])
                self.lista_dat_dodania.append(r[1])
                self.lista_deadline.append(r[2])
                if r[3] == 'Wykonane':
                    self.lista_wykonane.append(1)
                else:
                    self.lista_wykonane.append(0)
        except sqlite3.OperationalError:
            print('lol')
        print(self.lista, self.lista_wykonane, self.lista_deadline, self.lista_dat_dodania)

    def save(self):
        for _ in range(len(self.lista)):
            self.cursor.execute(f"""

                insert into tasks (name,data_dodania,deadline,stan) values ("{self.lista[_]}","{self.lista_dat_dodania[_]}","{self.lista_deadline[_]}","{'Wykonane' if self.lista_wykonane[_] != 0 else "Nie wykonane"}")

            """)
            self.db.commit()

    def zatwierdz_wyswietlanie(self):
        zaznaczony = self.Main_listWidget.currentRow()
        if self.checkbox2.isChecked() == True:
            for i in self.lista_wykonane:
                if self.lista_wykonane[zaznaczony] == 1:
                    self.Main_listWidget.takeItem(zaznaczony)
                    self.lista_wykonane.pop(zaznaczony)
                    self.lista_deadline.pop(zaznaczony)
                else:
                    pass
        else:
            pass

    def zatwierdz_wykonane(self):
        zaznaczony = self.Main_listWidget.currentRow()
        if self.checkbox.isChecked() == True:
            self.lista_wykonane.insert(zaznaczony, 1)
        else:
            self.lista_wykonane.insert(zaznaczony, 0)

    def update(self):
        zaznaczony = self.Main_listWidget.currentRow()
        if zaznaczony < 0:
            print("Zły index")
        else:
            self.Info_listWidget.setText(f"Data Dodania: {self.lista_dat_dodania[zaznaczony]}")
            self.info_deadline.setText(f"Deadline: {self.lista_deadline[zaznaczony]}")

            if self.lista_wykonane[zaznaczony] == 1:
                self.checkbox_info.setText('Wykonane: Tak')
            else:
                self.checkbox_info.setText('Wykonane: Nie')
            date = QDate.currentDate()
            item = date.toString('dd-MM-yyyy')
            if item > self.lista_deadline[zaznaczony]:
                self.info_deadline.setStyleSheet("color: red;")
            else:
                self.info_deadline.setStyleSheet("color: black;")

    def Dodawanie(self):
        if self.Task_input.text() == '':
            print("brak")
        else:
            item1 = self.Task_input.text()
            self.Main_listWidget.addItem(item1)
            self.Task_input.setText("")
            date = QDate.currentDate()
            item = date.toString('dd-MM-yyyy')
            self.lista.append(item1)
            self.lista_dat_dodania.append(item)
            self.Info_listWidget.setText(f"Data Dodania:")
            self.info_deadline.setText(f"DeadLine:")
            self.Deadline_input.setText("")
            self.lista_wykonane.append(0)

    def usuwanie(self):
        zaznaczony = self.Main_listWidget.currentRow()
        self.Main_listWidget.takeItem(zaznaczony)
        self.lista_wykonane.pop(zaznaczony)
        self.lista_deadline.pop(zaznaczony)

    def Deadline(self):
        if self.Deadline_input.text() == '':
            print("brak")
        else:
            self.lista_deadline.append((self.Deadline_input.text()))
            self.Deadline_input.setText("")

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.Dodaj.setText(_translate("MainWindow", "Dodaj"))
        self.usun.setText(_translate("MainWindow", "Usun"))
        self.Dodaj_deadline.setText(_translate("MainWindow", "Dodaj Deadline"))
        self.Zapisz.setText(_translate("MainWindow", "Info"))
        self.checkbox_button.setText(_translate("MainWindow", "Zatwierdz"))
        self.checkbox_button2.setText(_translate("MainWindow", "Zatwierdz"))
        self.save_button.setText(_translate("MainWindow", 'Zapisz'))


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())