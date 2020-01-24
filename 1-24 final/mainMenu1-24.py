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

        self.grid = QtWidgets.QGridLayout()
        self.grid.addWidget(self.createGroup(), 0, 0)
        self.grid.addWidget(self.createGroup2(), 0, 1, 1, 4.5)
        self.centralwidget.setLayout(self.grid)

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

        self.getSummaryBtn.clicked.connect(self.setSummary)
        self.getLinkedBtn.clicked.connect(self.setLinkedHistogram)
        self.getUnlinkedBtn.clicked.connect(self.setUnlinkedHistogram)
        self.getTimeStoppedBtn.clicked.connect(self.setTimeStoppedHistogram)
        self.getTimeRunningBtn.clicked.connect(self.setTimeRunningHistogram)

        self.actionOpenFile.triggered.connect(self.openFile)
        self.actionOpenDir.triggered.connect(self.openDir)
        self.action_Exit.triggered.connect(self.exit)

    # add buttons to left side
    def createGroup(self):
        groupBox = QGroupBox("Selection")

        self.getSummaryBtn = QtWidgets.QPushButton(self.centralwidget)
        self.getSummaryBtn.setObjectName("getSummaryBtn")
        self.getLinkedBtn = QtWidgets.QPushButton(self.centralwidget)
        self.getLinkedBtn.setObjectName("getLinkedBtn")
        self.getUnlinkedBtn = QtWidgets.QPushButton(self.centralwidget)
        self.getUnlinkedBtn.setObjectName("getUnlinkedBtn")
        self.getTimeStoppedBtn = QtWidgets.QPushButton(self.centralwidget)
        self.getTimeStoppedBtn.setObjectName("getTimeStoppedBtn")
        self.getTimeRunningBtn = QtWidgets.QPushButton(self.centralwidget)
        self.getTimeRunningBtn.setObjectName("getTimeRunningBtn")

        self.getSummaryBtn.setStyleSheet("QPushButton {\n"
        "color: #333;\n"
        "background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 rgba(0, 0, 0, 255), stop:1 rgba(255, 255, 255, 255));\n"
        "border: 2px outset #555;\n"
        "border-radius: 11px;\n"
        "padding: 5px;\n"
        "background: qradialgradient(cx: 0.3, cy: -0.4,\n"
        "fx: 0.3, fy: -0.4,\n"
        "radius: 1.35, stop: 0 #fff, stop: 1 #888);\n"
        "min-width: 10em;\n"
        "padding: 6px;\n"
        "}\n"
        "QPushButton:hover {\n"
        "background: qradialgradient(cx: 0.3, cy: -0.4,\n"
        "fx: 0.3, fy: -0.4,\n"
        "radius: 1.35, stop: 0 #fff, stop: 1 #bbb);\n"
        "}\n"
        "QPushButton:pressed {\n"
        "background: qradialgradient(cx: 0.4, cy: -0.1,\n"
        "fx: 0.4, fy: -0.1,\n"
        "radius: 1.35, stop: 0 #fff, stop: 1 #ddd);\n"
        "}")

        self.getLinkedBtn.setStyleSheet("QPushButton {\n"
        "color: #333;\n"
        "background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 rgba(0, 0, 0, 255), stop:1 rgba(255, 255, 255, 255));\n"
        "border: 2px outset #555;\n"
        "border-radius: 11px;\n"
        "padding: 5px;\n"
        "background: qradialgradient(cx: 0.3, cy: -0.4,\n"
        "fx: 0.3, fy: -0.4,\n"
        "radius: 1.35, stop: 0 #fff, stop: 1 #888);\n"
        "min-width: 10em;\n"
        "padding: 6px;\n"
        "}\n"
        "QPushButton:hover {\n"
        "background: qradialgradient(cx: 0.3, cy: -0.4,\n"
        "fx: 0.3, fy: -0.4,\n"
        "radius: 1.35, stop: 0 #fff, stop: 1 #bbb);\n"
        "}\n"
        "QPushButton:pressed {\n"
        "background: qradialgradient(cx: 0.4, cy: -0.1,\n"
        "fx: 0.4, fy: -0.1,\n"
        "radius: 1.35, stop: 0 #fff, stop: 1 #ddd);\n"
        "}")

        self.getUnlinkedBtn.setStyleSheet("QPushButton {\n"
        "color: #333;\n"
        "background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 rgba(0, 0, 0, 255), stop:1 rgba(255, 255, 255, 255));\n"
        "border: 2px outset #555;\n"
        "border-radius: 11px;\n"
        "padding: 5px;\n"
        "background: qradialgradient(cx: 0.3, cy: -0.4,\n"
        "fx: 0.3, fy: -0.4,\n"
        "radius: 1.35, stop: 0 #fff, stop: 1 #888);\n"
        "min-width: 10em;\n"
        "padding: 6px;\n"
        "}\n"
        "QPushButton:hover {\n"
        "background: qradialgradient(cx: 0.3, cy: -0.4,\n"
        "fx: 0.3, fy: -0.4,\n"
        "radius: 1.35, stop: 0 #fff, stop: 1 #bbb);\n"
        "}\n"
        "QPushButton:pressed {\n"
        "background: qradialgradient(cx: 0.4, cy: -0.1,\n"
        "fx: 0.4, fy: -0.1,\n"
        "radius: 1.35, stop: 0 #fff, stop: 1 #ddd);\n"
        "}")

        self.getTimeStoppedBtn.setStyleSheet("QPushButton {\n"
        "color: #333;\n"
        "background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 rgba(0, 0, 0, 255), stop:1 rgba(255, 255, 255, 255));\n"
        "border: 2px outset #555;\n"
        "border-radius: 11px;\n"
        "padding: 5px;\n"
        "background: qradialgradient(cx: 0.3, cy: -0.4,\n"
        "fx: 0.3, fy: -0.4,\n"
        "radius: 1.35, stop: 0 #fff, stop: 1 #888);\n"
        "min-width: 10em;\n"
        "padding: 6px;\n"
        "}\n"
        "QPushButton:hover {\n"
        "background: qradialgradient(cx: 0.3, cy: -0.4,\n"
        "fx: 0.3, fy: -0.4,\n"
        "radius: 1.35, stop: 0 #fff, stop: 1 #bbb);\n"
        "}\n"
        "QPushButton:pressed {\n"
        "background: qradialgradient(cx: 0.4, cy: -0.1,\n"
        "fx: 0.4, fy: -0.1,\n"
        "radius: 1.35, stop: 0 #fff, stop: 1 #ddd);\n"
        "}")

        self.getTimeRunningBtn.setStyleSheet("QPushButton {\n"
        "color: #333;\n"
        "background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 rgba(0, 0, 0, 255), stop:1 rgba(255, 255, 255, 255));\n"
        "border: 2px outset #555;\n"
        "border-radius: 11px;\n"
        "padding: 5px;\n"
        "background: qradialgradient(cx: 0.3, cy: -0.4,\n"
        "fx: 0.3, fy: -0.4,\n"
        "radius: 1.35, stop: 0 #fff, stop: 1 #888);\n"
        "min-width: 10em;\n"
        "padding: 6px;\n"
        "}\n"
        "QPushButton:hover {\n"
        "background: qradialgradient(cx: 0.3, cy: -0.4,\n"
        "fx: 0.3, fy: -0.4,\n"
        "radius: 1.35, stop: 0 #fff, stop: 1 #bbb);\n"
        "}\n"
        "QPushButton:pressed {\n"
        "background: qradialgradient(cx: 0.4, cy: -0.1,\n"
        "fx: 0.4, fy: -0.1,\n"
        "radius: 1.35, stop: 0 #fff, stop: 1 #ddd);\n"
        "}")

        vbox = QVBoxLayout()
        vbox.addWidget(self.getSummaryBtn)
        vbox.addWidget(self.getLinkedBtn)
        vbox.addWidget(self.getUnlinkedBtn)
        vbox.addWidget(self.getTimeStoppedBtn)
        vbox.addWidget(self.getTimeRunningBtn)
        vbox.addStretch(1)
        groupBox.setLayout(vbox)

        return groupBox

    # create label on right side
    def createGroup2(self):
        groupBox = QGroupBox("Histogram")

        self.image = QtWidgets.QLabel(self.centralwidget)
        self.image.setObjectName("imageLabel")

        vbox2 = QVBoxLayout()
        vbox2.addWidget(self.image)
        groupBox.setLayout(vbox2)

        return groupBox

    # mainMenu components
    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.getSummaryBtn.setText(_translate("MainWindow", "Push for Summary"))
        self.getLinkedBtn.setText(_translate("MainWindow", "Push for Linked Bag"))
        self.getUnlinkedBtn.setText(_translate("MainWindow", "Push for Unlinked Bag"))
        self.getTimeStoppedBtn.setText(_translate("MainWindow", "Push for Time Stopped"))
        self.getTimeRunningBtn.setText(_translate("MainWindow", "Push for Time Running"))
        self.image.setText(_translate("MainWindow", "ImageLabel"))
        # self.sumlabel.setText(_translate("MainWindow", "Summary"))
        self.menu_File.setTitle(_translate("MainWindow", "&File"))
        self.action_Exit.setText(_translate("MainWindow", "&Exit"))
        self.actionOpenFile.setText(_translate("MainWindow", "&Open File/Files"))
        self.actionOpenDir.setText(_translate("MainWindow", "&Open Folder"))

    # display summary label
    def setSummary(self):
    	self.image.setPixmap(QtGui.QPixmap('his.png'))

    # display linked bags histogram
    def setLinkedHistogram(self):
        # pixmap = pixmap.scaled(self.label.width(), self.label.height(), QtCore.Qt.KeepAspectRatio, QtCore.Qt.FastTransformation)	# make image unclear
        self.image.setPixmap(QtGui.QPixmap('link.png'))

    # display unlinked bags histogram
    def setUnlinkedHistogram(self):
        self.image.setPixmap(QtGui.QPixmap('unlink.png'))

    # display time stopped histogram
    def setTimeStoppedHistogram(self):
        self.image.setPixmap(QtGui.QPixmap('stop_time_distribution.png'))

    # display time running histogram
    def setTimeRunningHistogram(self):
        self.image.setPixmap(QtGui.QPixmap('running_time_distribution'))

    # open file dialog
    def openFile(self):
        filenames, _ = QtWidgets.QFileDialog.getOpenFileNames(None,"QFileDialog.getOpenFileNames()", "","All Files (*);;Log Files (*.log);;")
        if filenames:
            print("inside:",filenames)
        print("fdsfs", filenames)

        illegal = False
        suf = 'log' # test for single .txt first, need to modify for final version
        if len(filenames) != 0:
            for f in filenames: # check all files are illegal in here
                suffix = f[f.rfind('.')+1:]
                if suffix != suf:
                    print("Illegal selection")
                    illegal = True
            print(illegal)
            if illegal:
                self.showdialog(illegal, True);
            else:
                pp = PreProc(filenames)     # pass files into PreProc class
                dp = DataProc('in_window_logfile.csv', 'machine_decision_logfile.csv')     # pass the prepared data into DataProc class
                dp.getDiffHistogram(dp.linked)
                self.image.setPixmap(QtGui.QPixmap('his.png'))

    # open directory dialog
    def openDir(self):
        dialog = QtWidgets.QFileDialog()
        dialog.setFileMode(QFileDialog.DirectoryOnly)

        dic_file = []
        if dialog.exec_(): # == QtGui.QDialog.Accepted:
            dic_file = dialog.selectedFiles()
        print("openDir: (dic_file) ", dic_file)

        log_file = []
        has_log = False
        suf = 'log'
        if dic_file:
            for f in os.listdir(dic_file[0]):
        #         print(f)
                suffix = f[f.rfind('.')+1:]
                name = f[:f.rfind('.')]
                print(name)
                if suffix == suf:
                    has_log = True
                    if "AnalogicStandaloneType" in name:# if match AnalogicStandaloneType*.log, append to log_file     
                        log_file += dic_file[0]+"/"+f,
            print(has_log, log_file)
            if not has_log:            
                self.showdialog(False, has_log)
            if len(log_file) == 0 and has_log:
            	self.showdialog(False, False)
            if len(log_file) != 0:
                pp = PreProc(log_file)     # pass files into PreProc class
                dp = DataProc('in_window_logfile.csv', 'machine_decision_logfile.csv')     # pass the prepared data into DataProc class
                dp.getDiffHistogram(dp.linked)
                self.image.setPixmap(QtGui.QPixmap('his.png'))

    # pop up warning window
    def showdialog(self, illegal_file, has_log):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        if not has_log:
            msg.setText("No log files found.")
        if illegal_file:
            print("in illegal")
            msg.setText("Invalid log files detected.")


        msg.setWindowTitle("Something's wrong")

        # msg.setGeometry(200, 200, 300, 400) # need to change if need this line
        msg.setStandardButtons(QMessageBox.Ok)

        retval = msg.exec_()


    def exit(self):
        sys.exit(app.exec_())

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())