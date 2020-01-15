# -*- coding: utf-8 -*-
"""
Created on Wed Jan  8 16:53:58 2020

@author: wzhong
"""

import sys
from preProc import PreProc
from fileProc import FileProc
from dataProc import DataProc
from PyQt5 import QtWidgets
from PyQt5 import QtGui
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import Qt, QAbstractTableModel

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
                print(f)    #, f.rfind('.'), f[f.rfind('.')+1:])
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
                self.textBox.setText((',').join(filenames))
                print("show loding dialog")
                # self.l = LoadView()
                # self.l
                # fp = FileProc(filenames)
                pp = PreProc(filenames)
                dp = DataProc('in_window_logfile.csv', 'machine_decision_logfile.csv')
                # linked_bags = fp.getLinkedBags()
                # unlinked_bags = fp.getUnlinkedBags()
                # print(len(linked_bags), len(unlinked_bags))
                # dp = DataProc(linked_bags, unlinked_bags)

                # # self.l.setParent(None)
                # # uncomment below when fileProc connect to dataProc
                # self.m = MainMenu('his.png')      # this line is to show histogram

                # self.h = HisView('his.png')
                # self.h.show()
                # to here
                print(dp.dfinal)
                model = pandasModel(dp.dfinal)
                self.view = QTableView()
                self.view.setModel(model)
                self.view.resize(800, 600)
                self.view.show()


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

class pandasModel(QAbstractTableModel):

    def __init__(self, data):
        QAbstractTableModel.__init__(self)
        self._data = data

    def rowCount(self, parent=None):
        return self._data.shape[0]

    def columnCount(self, parnet=None):
        return self._data.shape[1]

    def data(self, index, role=Qt.DisplayRole):
        if index.isValid():
            if role == Qt.DisplayRole:
                return str(self._data.iloc[index.row(), index.column()])
        return None

    def headerData(self, col, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self._data.columns[col]
        return None

class MainMenu(QMainWindow):
    def __init__(self, image):
        super().__init__()
        self.imageName = image
        self.initUI()

    def initUI(self):
        bar = self.menuBar()    # menu bar
        file_menu = bar.addMenu('File') # File menu
        open_action = QtWidgets.QAction('Open', self)
        close_action = QtWidgets.QAction('Close', self)
        file_menu.addAction(open_action)
        file_menu.addAction(close_action)       

        # hisWidget = HisView('his.png')
        hisWidget = QWidget()
        self.setCentralWidget(hisWidget)
        lay = QVBoxLayout(hisWidget)

        self.labelHis = QLabel(self)
        # vlayout.addWidget(self.labelHis)       
        self.pixmap = QPixmap(self.imageName)
        self.labelHis.setPixmap(self.pixmap)
        self.labelHis.adjustSize()
        self.resize(self.pixmap.width(), self.pixmap.height())
        lay.addWidget(self.labelHis)


        self.setGeometry(100, 100, 640, 480)
        # self.setFixedSize(self.size())    # add this line will crop image
        self.setWindowTitle('Histogram') 

        self.show()


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