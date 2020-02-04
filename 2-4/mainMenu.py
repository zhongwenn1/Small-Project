import sys
import os
import re
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import Qt, QAbstractTableModel
from preProc import PreProc
from dataProc import DataProc
from simulationTool import TimeMeasure

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        # self.grid = QtWidgets.QGridLayout()
        # self.grid.setSpacing(10)    # hou jia de
        # self.grid.addWidget(self.createGroup(), 0, 0)       # combobox and buttons
        # self.grid.addWidget(self.createGroup2(), 0, 1, 1, 4.5)  # label
        # self.grid.addWidget(self.createGroup2(), 0, 1)  # row span and column span

        # self.centralwidget.setLayout(self.grid)

        self.contentsWidget = QListWidget()
        self.contentsWidget.insertItem(0, 'Linked/Unlinked Bags')
        self.contentsWidget.insertItem(1, 'Simulation Tools')

        self.stack1 = QWidget()
        self.stack2 = QWidget()

        self.stack1UI()
        self.stack2UI()

        self.st = QStackedWidget(self.centralwidget)
        self.st.addWidget(self.stack1)
        self.st.addWidget(self.stack2)

        hbox = QHBoxLayout(self.centralwidget)
        hbox.addWidget(self.contentsWidget)
        hbox.addWidget(self.st)
        hbox.setStretch(1, 100)

        self.centralwidget.setLayout(hbox)
        self.contentsWidget.currentRowChanged.connect(self.display)

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


        # self.getSummaryBtn.clicked.connect(self.setSummary)
        # self.getLinkedBtn.clicked.connect(self.setLinkedHistogram)
        # self.getUnlinkedBtn.clicked.connect(self.setUnlinkedHistogram)
        # self.getTimeStoppedBtn.clicked.connect(self.setTimeStoppedHistogram)
        # self.getTimeRunningBtn.clicked.connect(self.setTimeRunningHistogram)

        self.actionOpenFile.triggered.connect(self.openFile)
        self.actionOpenDir.triggered.connect(self.openDir)
        self.action_Exit.triggered.connect(self.exit)

    def stack1UI(self):
        layout = QVBoxLayout()
        combo = QComboBox(self.centralwidget)
        combo.addItem("Linked Bags")
        combo.addItem("Unlinked Bags")
        combo.addItem("Summary")

        self.image = QtWidgets.QLabel(self.centralwidget)
        self.image.setObjectName("imageLabel")
        self.image.setText("image")

        layout.addWidget(combo)
        layout.addWidget(self.image)
        self.stack1.setLayout(layout)

        combo.activated[str].connect(self.onActivated)

    def stack2UI(self):
        vlayout = QVBoxLayout()
        hlayout = QHBoxLayout()

        label = QLabel()
        label.setText("Delay: ")
        self.text = QLineEdit()
        button = QPushButton("Go")

        hlayout.addWidget(label)
        hlayout.addWidget(self.text)
        hlayout.addWidget(button)

        self.labelDelay = QtWidgets.QLabel(self.centralwidget)
        self.labelDelay.setObjectName("delayResult")
        self.labelDelay.setText("fdsfsdfsd")

        vlayout.addLayout(hlayout)
        vlayout.addWidget(self.labelDelay)
        self.stack2.setLayout(vlayout)

        button.clicked.connect(self.simulate)

    def display(self, i):
        self.st.setCurrentIndex(i)


    # mainMenu components
    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        # self.getSummaryBtn.setText(_translate("MainWindow", "Push for Summary"))
        # self.getLinkedBtn.setText(_translate("MainWindow", "Push for Linked Bag"))
        # self.getUnlinkedBtn.setText(_translate("MainWindow", "Push for Unlinked Bag"))
        # self.getTimeStoppedBtn.setText(_translate("MainWindow", "Push for Time Stopped"))
        # self.getTimeRunningBtn.setText(_translate("MainWindow", "Push for Time Running"))
        # self.image.setText(_translate("MainWindow", "ImageLabel"))
        self.labelDelay.setText(_translate("MainWindow", "DelayLabel"))
        self.menu_File.setTitle(_translate("MainWindow", "&File"))
        self.action_Exit.setText(_translate("MainWindow", "&Exit"))
        self.actionOpenFile.setText(_translate("MainWindow", "&Open File/Files"))
        self.actionOpenDir.setText(_translate("MainWindow", "&Open Folder"))

    # combo box items
    def onActivated(self, text):
        print(text)
        if text == 'Linked Bags':
            self.image.setPixmap(QtGui.QPixmap('link.png'))
        elif text == 'Unlinked Bags':
            self.image.setPixmap(QtGui.QPixmap('unlink.png'))
        elif text == 'Summary':
            self.image.setPixmap(QtGui.QPixmap('his.png'))

    def simulate(self):
        print(self.text.text())
        if bool(re.match('^[0-9]+$',self.text.text())):
            tm = TimeMeasure('runtime_.txt', int(self.text.text()))
            tm.getDuration()
            tm.runList("")
            tm.stopList("")
            total_time = tm.org_finish_time - tm.org_start_time

            self.labelDelay.setText("Run Time total: {0:d} Sum: {1:f} seconds Percentage: {2:.2f}%\n".format(len(tm.total_running_time), sum(tm.total_running_time), sum(tm.total_running_time)/total_time * 100))
            self.labelDelay.setText(self.labelDelay.text() + "Stop Time total: {0:d} Sum: {1:f} seconds Percentage: {2:.2f}%\n".format(len(tm.total_stopped_time), sum(tm.total_stopped_time), sum(tm.total_stopped_time)/total_time * 100))
            self.labelDelay.setText(self.labelDelay.text() + "Total: {0:f} seconds Percentage: {1:.2f}%\n".format(total_time, sum(tm.total_running_time)/total_time * 100 + sum(tm.total_stopped_time)/total_time * 100))
            # print("run:",len(tm.total_running_time), "sum:", sum(tm.total_running_time),"percentage:",sum(tm.total_running_time)/total_time * 100)
            # print("stop:",len(tm.total_stopped_time), "sum:", sum(tm.total_stopped_time),"percentage:",sum(tm.total_stopped_time)/total_time * 100)
            # print("total:",total_time, sum(tm.total_running_time)/total_time * 100 + sum(tm.total_stopped_time)/total_time * 100)
            # print("\n---------------Add delay 2 seconds---------------\n")
            self.labelDelay.setText(self.labelDelay.text() + "\n---------------Add delay 2 seconds---------------\n\n")
            tm.runListDelay("")
            tm.stopListDelay("")
            total_time_after_delay = tm.delay_finish_time - tm.delay_start_time
            self.labelDelay.setText(self.labelDelay.text() + "Run time after delay: {0:d} Sum: {1:f} seconds Percentage: {2:.2f}%\n".format(len(tm.total_running_after_delay), sum(tm.total_running_after_delay), sum(tm.total_running_after_delay) / total_time_after_delay * 100))
            self.labelDelay.setText(self.labelDelay.text() + "Stop time after delay: {0:d} Sum: {1:f} seconds Percentage: {2:.2f}%\n".format(len(tm.total_stopped_after_delay), sum(tm.total_stopped_after_delay), sum(tm.total_stopped_after_delay) / total_time_after_delay * 100))
            self.labelDelay.setText(self.labelDelay.text() + "Total: {0:f} seconds Percentage: {1:.2f}%\n".format(total_time_after_delay, sum(tm.total_running_after_delay) / total_time_after_delay * 100 + sum(tm.total_stopped_after_delay) / total_time_after_delay * 100))
            # print("run after delay:", len(tm.total_running_after_delay), "sum:", sum(tm.total_running_after_delay), "percentage:",sum(tm.total_running_after_delay) / total_time_after_delay * 100)
            # print("stop after delay:",len(tm.total_stopped_after_delay), "sum:", sum(tm.total_stopped_after_delay), "percentage:",sum(tm.total_stopped_after_delay) / total_time_after_delay * 100)
            # print("total:",total_time_after_delay, sum(tm.total_running_after_delay) / total_time_after_delay * 100 + sum(tm.total_stopped_after_delay) / total_time_after_delay * 100)

            tm.fakestopList()
            delaylist = tm.getCertainRangeList(tm.fake_total_stopped_time)
            # print("\nSummary:")
            # print("Before delay XRAY_MIN / total: 100% ----> After delay XRAY_MIN / total: {0:.2f}%".format((len(tm.fake_total_stopped_time)-len(delaylist))/len(tm.fake_total_stopped_time)*100))
            # print("Before delay total time: 100% ----> After delay total time: {0:.2f}%".format(total_time_after_delay/total_time*100))
            self.labelDelay.setText(self.labelDelay.text() + "\nSummary:")
            self.labelDelay.setText(self.labelDelay.text() + "Before delay total time: 100% ----> After delay total time: {0:.2f}%\n".format(total_time_after_delay/total_time*100))
            self.labelDelay.setText(self.labelDelay.text() + "Before delay XRAY_MIN / total: 100% ----> After delay XRAY_MIN / total: {0:.2f}%".format((len(tm.fake_total_stopped_time)-len(delaylist))/len(tm.fake_total_stopped_time)*100))


    # display summary label
    def setSummary(self):
    	self.image.setPixmap(QtGui.QPixmap('his.png'))

    # display linked bags histogram
    def setLinkedHistogram(self):
        # pixmap = pixmap.tmaled(self.label.width(), self.label.height(), QtCore.Qt.KeepAspectRatio, QtCore.Qt.FastTransformation)	# make image unclear
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
                dp = DataProc()     # pass the prepared data into DataProc class
                # dp.getDiffHistogram(dp.linked)
                # self.image.setPixmap(QtGui.QPixmap('his.png'))

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
                dp = DataProc()     # pass the prepared data into DataProc class
                # dp.getDiffHistogram(dp.linked)
                # self.image.setPixmap(QtGui.QPixmap('his.png'))

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