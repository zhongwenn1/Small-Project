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
        self.title = 'Bin Tracking - Select files'  # app title
        self.left = 200
        self.top = 300
        self.width = 500  
        self.height = 200
        self.initUI()
   

    def initUI(self):
        self.setWindowTitle(self.title)             # set window title
        self.setGeometry(self.left, self.top, self.width, self.height)

        hlayout = QHBoxLayout()                     # set a horizontal layout

        self.textBox = QLineEdit(self)              # place to input file path
        hlayout.addWidget(self.textBox)             # add textbox to layout

        self.openButton = QtWidgets.QPushButton(self)   # open to show folder browser
        self.openButton.setText("Open")             # set button name

        self.openButton.clicked.connect(self.choosePath)    # connect button with function
        hlayout.addWidget(self.openButton)          # add button to layout

        self.setLayout(hlayout)         # set layout to active

        self.show()         # show the UI
    
    def choosePath(self):   # pop out the file browser, triggered by "open" button

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
                # print(f)    #, f.rfind('.'), f[f.rfind('.')+1:])
                suffix = f[f.rfind('.')+1:]
                if suffix != suf:
                    print("Illegal selection")
                    illegal = True

            # if selected file contains illegal extension, show warning
            if illegal:
                print("Should pop up message box")
                self.showdialog();
                # then go back to selection 
                    
            # we made here because all files are log file, go to File process procedure,seperate calss for process log files
            else:
                self.textBox.setText((',').join(filenames))     # display selected files inside the textedit box

                pp = PreProc(filenames)     # pass files into PreProc class
                dp = DataProc('in_window_logfile.csv', 'machine_decision_logfile.csv')     # pass the prepared data into DataProc class

                self.m = MainMenu('his.png')      # this line is to show histogram

                print(dp.dfinal)    # print the final dataframe, show on console

                # diaplay the dataframe on seperate widget
                model = pandasModel(dp.dfinal)  
                self.view = QTableView()
                self.view.setModel(model)
                self.view.resize(800, 600)
                self.view.show()

    # pop up warning window
    def showdialog(self):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setText("It must be *.log files")
        # msg.setInformativeText("Your selection contains non *log files")  # small font, need to change if need this line

        msg.setWindowTitle("Something's wrong")

        # msg.setGeometry(200, 200, 300, 400) # need to change if need this line
        msg.setStandardButtons(QMessageBox.Ok)

        retval = msg.exec_()
        # print ("value of pressed message box button:", retval)

# display pandas dataframe on seperate window
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

# main menu for histogram window, should be able to choose item from menu bar
class MainMenu(QMainWindow):
    def __init__(self, image):
        super().__init__()
        self.imageName = image
        self.initUI()

    def initUI(self):
        bar = self.menuBar()        # Add menu bar
        file_menu = bar.addMenu('File')     # Add file menu to menu abr
        open_action = QtWidgets.QAction('Open', self)   # drop down select to different pages
        close_action = QtWidgets.QAction('Close', self) # drop down select to different pages
        file_menu.addAction(open_action)    # add action
        file_menu.addAction(close_action)       

        hisWidget = QWidget()       # new widget where to display image
        self.setCentralWidget(hisWidget)    # place this widget in center
        lay = QVBoxLayout(hisWidget)    # layout the widget

        self.labelHis = QLabel(self)    # create new label to show image

        self.pixmap = QPixmap(self.imageName)   # method to show image attach to the label
        self.labelHis.setPixmap(self.pixmap)
        self.labelHis.adjustSize()      # adjust the label
        self.resize(self.pixmap.width(), self.pixmap.height())  # adjust the size to fit the screen
        lay.addWidget(self.labelHis)    # add this image label to layout


        self.setGeometry(100, 100, 640, 480)
        # self.setFixedSize(self.size())    # add this line will crop image
        self.setWindowTitle('Histogram') 

        self.show()     # make it display


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
