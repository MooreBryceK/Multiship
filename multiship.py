from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt
import csv
import os


class MultiShip:
    def __init__(self):
        self.org_csv_file = ''
        self.new_csv_file = ''
        self.new_csv_file_content = ''
        self.remove_chrs = '@#:;()[],./\\\'"'
        self.errors = []

    def save_file(self):
        self.remove_chrs = self.remove_chrs.strip()

        # Read original csv file and store formatted content in a string.
        with open(self.org_csv_file, "r") as infile:
            reader = csv.reader(infile, delimiter=',')
            header = next(reader)

            self.new_csv_file_content += ','.join(header) + ',\n'

            for row in reader:
                line = ''
                for col in row:
                    cell = col.strip()
                    for c in self.remove_chrs:
                        cell = cell.replace(c, '')
                    line += f"{cell},"
                line += '\n'
                self.new_csv_file_content += line

        # Write formatted content to new csv file
        with open(self.new_csv_file, "w") as outfile:
            outfile.write(self.new_csv_file_content)


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(416, 203)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.btn_open_csv = QtWidgets.QPushButton(self.centralwidget)
        self.btn_open_csv.setGeometry(QtCore.QRect(10, 30, 71, 23))
        self.btn_open_csv.setObjectName("btn_open_csv")
        self.lbl_open_csv = QtWidgets.QLabel(self.centralwidget)
        self.lbl_open_csv.setGeometry(QtCore.QRect(10, 10, 81, 16))
        self.lbl_open_csv.setObjectName("lbl_open_csv")
        self.lne_open_csv = QtWidgets.QLineEdit(self.centralwidget)
        self.lne_open_csv.setGeometry(QtCore.QRect(90, 30, 311, 20))
        self.lne_open_csv.setObjectName("lne_open_csv")
        self.lne_remove_chrs = QtWidgets.QLineEdit(self.centralwidget)
        self.lne_remove_chrs.setGeometry(QtCore.QRect(10, 80, 391, 20))
        self.lne_remove_chrs.setObjectName("lne_remove_chrs")
        self.lbl_remove_chrs = QtWidgets.QLabel(self.centralwidget)
        self.lbl_remove_chrs.setGeometry(QtCore.QRect(10, 60, 141, 16))
        self.lbl_remove_chrs.setObjectName("lbl_remove_chrs")
        self.btn_save_csv = QtWidgets.QPushButton(self.centralwidget)
        self.btn_save_csv.setGeometry(QtCore.QRect(10, 120, 391, 61))
        self.btn_save_csv.setObjectName("btn_save_csv")
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.logic = MultiShip()
        self.lne_remove_chrs.setText(self.logic.remove_chrs)
        self.btn_open_csv.clicked.connect(self.evt_btn_open_csv_clicked)
        self.btn_save_csv.clicked.connect(self.evt_btn_save_csv_clicked)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def evt_btn_open_csv_clicked(self):
        try:
            path, _ = QtWidgets.QFileDialog.getOpenFileName(MainWindow, "Open csv file", "", "CSV Files (*.csv)")
            self.lne_open_csv.setText(str(path))
        except Exception as e:
            QtWidgets.QMessageBox.about(MainWindow, 'Error', str(e))

    def evt_btn_save_csv_clicked(self):
        self.logic.remove_chrs = self.lne_remove_chrs.text().strip()

        if os.path.isfile(self.lne_open_csv.text().strip()):
            try:
                self.logic.org_csv_file = self.lne_open_csv.text().strip()
                option = QtWidgets.QFileDialog.Options()
                path, _ = QtWidgets.QFileDialog.getSaveFileName(
                    MainWindow, "Save CSV File", "", "CSV Files (*.csv)", options=option)
                self.logic.new_csv_file = str(path)
                self.logic.save_file()
                QtWidgets.QMessageBox.about(MainWindow, 'File created', f"Created file '{path}'")
            except Exception as e:
                QtWidgets.QMessageBox.about(MainWindow, 'Error', str(e))
        else:
            QtWidgets.QMessageBox.about(MainWindow, 'Error', "Open a csv file to continue.")

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Multiship"))
        self.btn_open_csv.setText(_translate("MainWindow", "Open"))
        self.lbl_open_csv.setText(_translate("MainWindow", "Open CSV File:"))
        self.lbl_remove_chrs.setText(_translate("MainWindow", "Remove Characters:"))
        self.btn_save_csv.setText(_translate("MainWindow", "Save"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
