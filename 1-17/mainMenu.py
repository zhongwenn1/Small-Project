# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\wzhong\Documents\mainMenu.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!

import sys
import os
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import Qt, QAbstractTableModel
from preProc import PreProc
from dataProc import DataProc

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.getLinkedBtn = QtWidgets.QPushButton(self.centralwidget)
        self.getLinkedBtn.setGeometry(QtCore.QRect(40, 170, 131, 31))
        self.getLinkedBtn.setObjectName("getLinkedBtn")
        self.getUnlinkedBtn = QtWidgets.QPushButton(self.centralwidget)
        self.getUnlinkedBtn.setGeometry(QtCore.QRect(40, 220, 131, 31))
        self.getUnlinkedBtn.setObjectName("getUnlinkedBtn")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(216, 42, 620, 520))
        self.label.setObjectName("label")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 21))
        self.menubar.setObjectName("menubar")
        self.menu_File = QtWidgets.QMenu(self.menubar)
        self.menu_File.setObjectName("menu_File")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.action_Exit = QtWidgets.QAction(MainWindow)
        self.action_Exit.setObjectName("action_Exit")
        self.actionOpenFile = QtWidgets.QAction(MainWindow)
        self.actionOpenFile.setObjectName("actionOpenFile")
        self.actionOpenDir = QtWidgets.QAction(MainWindow)
        self.actionOpenDir.setObjectName("actionOpenDir")
        self.menu_File.addAction(self.actionOpenFile)
        self.menu_File.addAction(self.actionOpenDir)
        self.menu_File.addSeparator()
        self.menu_File.addAction(self.action_Exit)
        self.menubar.addAction(self.menu_File.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        self.getLinkedBtn.clicked.connect(self.setLinkedHistogram)
        self.getUnlinkedBtn.clicked.connect(self.setUnlinkedHistogram)

        self.actionOpenFile.triggered.connect(self.openFile)
        self.actionOpenDir.triggered.connect(self.openDir)
        self.action_Exit.triggered.connect(self.exit)


    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.getLinkedBtn.setText(_translate("MainWindow", "Push for Linked Bag"))
        self.getUnlinkedBtn.setText(_translate("MainWindow", "Push for Unlinked Bag"))
        # self.label.setText(_translate("MainWindow", "TextLabel"))
        self.menu_File.setTitle(_translate("MainWindow", "&File"))
        self.action_Exit.setText(_translate("MainWindow", "&Exit"))
        self.actionOpenFile.setText(_translate("MainWindow", "&Open File/Files"))
        self.actionOpenDir.setText(_translate("MainWindow", "&Open Folder"))

    def setLinkedHistogram(self):
        pixmap = QtGui.QPixmap('his.png')
        pixmap = pixmap.scaled(self.label.width(), self.label.height(), QtCore.Qt.KeepAspectRatio)
        self.label.setPixmap(pixmap)
        self.label.setAlignment(QtCore.Qt.AlignCenter)

    def setUnlinkedHistogram(self):
        pixmap = QtGui.QPixmap('her.png')
        pixmap = pixmap.scaled(self.label.width(), self.label.height(), QtCore.Qt.KeepAspectRatio)
        self.label.setPixmap(pixmap)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
     
    def processFile(self, fileNames):
        # pass
        has_log = False
        illegal_file = False
        if len(fileNames) != 0:
            for file in fileNames:
                suffix = f[f.rfind('.')+1:]
                if suffix == 'log':
                    has_log = True
                else:
                    illegal_file = True
            print("illegal_file:", illegal_file, "has_log:", has_log)
            self.showdialog(illegal_file, has_log)

    def openFile(self):
        filenames, _ = QtWidgets.QFileDialog.getOpenFileNames(None,"QFileDialog.getOpenFileNames()", "","All Files (*);;Log Files (*.log);;")
        if filenames:
            print("inside:",filenames)
        print("fdsfs", filenames)

        # self.processFile(filenames)
        # illegal_file = False
        # has_log = False
        # suf = 'log' # test for single .txt first, need to modify for final version
        # if len(filenames) != 0:
        #     for f in filenames: # check all files are illegal in here
        #         print("fff")
        #         suffix = f[f.rfind('.')+1:]
        #         if suffix != suf:
        #             print("Illegal selection")
        #             illegal = True
        #         elif suffix == suf:
        #             has_log = True
        #     self.showdialog(illegal_file, has_log);
        pp = PreProc(filenames)     # pass files into PreProc class
        dp = DataProc('in_window_logfile.csv', 'machine_decision_logfile.csv')     # pass the prepared data into DataProc class

    def openDir(self):
        dialog = QtWidgets.QFileDialog()
        dialog.setFileMode(QFileDialog.DirectoryOnly)

        dic_file = []
        if dialog.exec_(): # == QtGui.QDialog.Accepted:
            dic_file = dialog.selectedFiles()
        print(dic_file)

        filenames = []
        if len(dic_file) != 0:
            for f in os.listdir(dic_file[0]):
                print(f)
                filenames += dic_file[0]+"/"+f,
            print(filenames)

        # has_log = False
        # suf = 'log'
        # if dic_file:
        #     for f in os.listdir(dic_file[0]):
        #         print(f)
        #         suffix = f[f.rfind('.')+1:]
        #         if suffix == suf:
        #             has_log = True     
        #     if not has_log:              
        #         self.showdialog(False, has_log);
        # # self.processFile(filenames)
        #     else:
        #         pp = PreProc(filenames)     # pass files into PreProc class
        #         dp = DataProc('in_window_logfile.csv', 'machine_decision_logfile.csv')     # pass the prepared data into DataProc class
        pp = PreProc(filenames)     # pass files into PreProc class
        dp = DataProc('in_window_logfile.csv', 'machine_decision_logfile.csv')     # pass the prepared data into DataProc class

    # pop up warning window
    def showdialog(self, illegal_file, has_log):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        if not has_log:
            msg.setText("No log files found.")
        if illegal_file and (has_log and illegal_file):
            msg.setText("Invalid log files detected.")


        msg.setWindowTitle("Something's wrong")

        # msg.setGeometry(200, 200, 300, 400) # need to change if need this line
        msg.setStandardButtons(QMessageBox.Ok)

        retval = msg.exec_()


    def exit(self):
        sys.exit(app.exec_())

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

        # options = QFileDialog.Options()
        # options |= QFileDialog.DontUseNativeDialog
        # files, _ = QFileDialog.getOpenFileNames(self,"QFileDialog.getOpenFileNames()", "","All Files (*);;Python Files (*.py)", options=options)
        # if files:
        #     print(files)
        # dialog = QtWidgets.QFileDialog()
        # # f = QFileDialog.getOpenFileName(dialog,)
        # dialog.setFileMode(QFileDialog.ExistingFiles)
        # filenames = []
        # if dialog.exec_():
        #     filenames = dialog.selectedFiles()
        # print(filenames)