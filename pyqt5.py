# -*- coding: utf-8 -*-
"""
Created on Wed Jan  8 16:53:58 2020

@author: wzhong
"""

import sys
from fileProc import FileProc
from dataProc import DataProc
from PyQt5 import QtWidgets
from PyQt5 import QtGui
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QFileDialog, QTextEdit, QHBoxLayout, 
    QMessageBox, QLineEdit)
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import Qt

class App(QWidget):

    def __init__(self):
        super().__init__()
        self.title = 'Bin Tracking - Select files'
        self.left = 200
        self.top = 300
        self.width = 500  
        self.height = 200
        self.initUI()
   

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        hlayout = QHBoxLayout()

        self.textBox = QLineEdit(self)
        hlayout.addWidget(self.textBox)

        self.openButton = QtWidgets.QPushButton(self)
        self.openButton.setText("Open")
        # self.openButton.clicked.connect(self.openClicked) # open image directly for now
        self.openButton.clicked.connect(self.choosePath)
        hlayout.addWidget(self.openButton)

        self.setLayout(hlayout)

        self.show()
    
    def choosePath(self):
        # pop out the file dialog

        dialog = QFileDialog()
        dialog.setFileMode(QFileDialog.ExistingFiles)

        filenames = []
        if dialog.exec_():
            filenames = dialog.selectedFiles()  
        # print(filenames)
        illegal = False
        suf = 'log' # test for single .txt first, need to modify for final version
        if len(filenames) != 0:
            for f in filenames: # check all files are illegal in here
                print(f, f.rfind('.'), f[f.rfind('.')+1:])
                suffix = f[f.rfind('.')+1:]
                if suffix != suf:
                    print("Illegal selection")
                    illegal = True
            if illegal:
                print("Should pop up message box")
                self.showdialog();
                # then go back to selection 
                    
            # we made here because all files are log file
            # go to File process procedure, I might prababely create a calss for process log files
            else:
                self.textBox.setText(('').join(filenames))
                # fp = DataProc(filenames[0]) # for process data and show diagram, single file
                fp = FileProc(filenames)
                # print(fp.getLinkedBags(), fp.getLinkedBagsNum())
                linked_bags = fp.getLinkedBags()
                dp = DataProc(linked_bags)

                # uncomment below when fileProc connect to dataProc
                self.h = HisView('his.png')
                self.h.show()
                # to here

        # process data by fname, save chart to img
        # image single file open in new window successfully
        # print(fname[0])
        # self.h = HisView(fname[0])
        # self.h.show()
        # self.label.setText("Displaying the histogram")  

        # self.update()

    def showdialog(self):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setText("It must be *.log files")
        # msg.setInformativeText("Your selection contains non *log files")
        msg.setWindowTitle("Something's wrong")
        # msg.setGeometry(200, 200, 300, 400) # need to change if need this line
        msg.setStandardButtons(QMessageBox.Ok)

        retval = msg.exec_()
        # print ("value of pressed message box button:", retval)

    def update(self):
        self.label.adjustSize()


class HisView(QWidget):
    def __init__(self, filename):
        super(HisView, self).__init__()
        # self.theHist = QLabel('text', self)

        # Create widget
        self.labelHis = QLabel(self)
        self.pixmap = QPixmap(filename)
        self.labelHis.setPixmap(self.pixmap)
        self.resize(self.pixmap.width(), self.pixmap.height())

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())


   #      fname = QFileDialog.getOpenFileName(self, 'Open file', 
   # 'c:\\',"Log files (*.log *.txt *.png)")
   
        # self.pixmap = QPixmap('C:/Users/wzhong/Documents/ff.png')

        # show histogram in label widget
        # f = open(fname[0], 'r')
        # with f:
        #     data = f.read()
        #     self.contents.setText(data)

        # dialog = QFileDialog()
        # dialog.setFileMode(QFileDialog.AnyFile)
        # dialog.setFilter("Text files (*.txt)")
        # filenames = QStringList()

        # if dlg.exec_():
        #     filenames = dlg.selectedFiles()    