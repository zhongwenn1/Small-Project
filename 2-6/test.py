import sys
import os
import re
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import Qt, QAbstractTableModel
from PyQt5.QtChart import QChart, QChartView, QValueAxis, QBarCategoryAxis, QBarSet, QBarSeries
from preProc import PreProc
from dataProc import DataProc
from simulationTool import TimeMeasure
import random

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

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
        self.action_Exit.setStatusTip('Exit')
        self.actionOpenFile = QtWidgets.QAction(MainWindow)
        self.actionOpenFile.setObjectName("actionOpenFile")
        self.actionOpenFile.setStatusTip('Open new File')
        self.actionOpenDir = QtWidgets.QAction(MainWindow)
        self.actionOpenDir.setObjectName("actionOpenDir")
        self.actionOpenDir.setStatusTip('Open Directory')
        self.menu_File.addAction(self.actionOpenFile)
        self.menu_File.addAction(self.actionOpenDir)
        self.menu_File.addSeparator()
        self.menu_File.addAction(self.action_Exit)
        self.menubar.addAction(self.menu_File.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        self.createBar(MainWindow)

    def createBar(self, MainWindow):
        dp = DataProc()
        # print(dp.linked)
        linked_list = dp.linked['Beam Diff'].values.tolist()
        # print(linked_list)

        count = [0] * 200
        # print(count)

        for item in linked_list:
            if item <= 160:
                count[int(item)] += 1

        set0 = QBarSet('Beam Difference')
        # set0.setColor(QColor("blue"))
        # add pen width to bar
        pen = QPen(QColor(0xfdb157))
        pen.setWidth(5)
        set0.setPen(pen)        
        # set1 = QBarSet('X1')
       
        set0.append(count)
        # set0.append([random.randint(0, 10) for i in range(6)])
      
        series = QBarSeries()
        series.append(set0)
        # series.barWidth()

        # series.append(set1)

        # Getting the Chart
        chart = QChart()                            # Getting the Chart

        # add font to title
        font = QFont()
        font.setPixelSize(18)
        chart.setTitleFont(font)        


        chart.addSeries(series)                     # Add data
        chart.setTitle('Linked Bags Histogram')            # Set title
        chart.setAnimationOptions(QChart.SeriesAnimations)  # Set animation

        # months = ('Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun') # Set custom axis
        times = ['0-20','20-40','40-60','60-80','80-100','100-120','120-140','140-160']

        # Set x-axis
        axisX = QBarCategoryAxis()
        # axisX.append(months)
        axisX.append(times)

        # Set y-axis
        # axisY = QValueAxis()
        # axisY.setRange(0, 200)

        # Alignment for x,y axis
        chart.addAxis(axisX, Qt.AlignBottom)
        # chart.addAxis(axisY, Qt.AlignLeft)

        # Enable legend and set custom axis alignment to bottom
        chart.legend().setVisible(True)
        chart.legend().setAlignment(Qt.AlignBottom)

        # Create ChartView
        chartView = QChartView(chart)
        # add rendering
        # chartView.setRenderHint(QPainter.Antialiasing)
        # Set view at the center of MainWindw (show view)
        MainWindow.setCentralWidget(chartView)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        # self.getSummaryBtn.setText(_translate("MainWindow", "Push for Summary"))
        # self.image.setText(_translate("MainWindow", "ImageLabel"))
        # self.labelDelay.setText(_translate("MainWindow", "DelayLabel"))
        self.menu_File.setTitle(_translate("MainWindow", "&File"))
        self.action_Exit.setText(_translate("MainWindow", "&Exit"))
        self.actionOpenFile.setText(_translate("MainWindow", "&Open File/Files"))
        self.actionOpenDir.setText(_translate("MainWindow", "&Open Folder"))

    def exit(self):
        sys.exit(app.exec_())

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())