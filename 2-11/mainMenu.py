import sys
import os
import re
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import (QListWidget, QListWidgetItem, QStackedWidget, QListView, QWidget, QVBoxLayout, QHBoxLayout, QComboBox, 
			QLabel, QLineEdit, QPushButton, QRadioButton, QFileDialog)
from PyQt5.QtGui import QIcon, QBrush, QPen, QColor, QFont, QPainter
from PyQt5.QtCore import Qt, QAbstractTableModel, QSize
from PyQt5.QtChart import QChart, QChartView, QValueAxis, QBarCategoryAxis, QBarSet, QBarSeries, QPieSeries, QPieSlice
from preProc import PreProc
from dataProc import DataProc
from simulationTool import TimeMeasure
import random

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1280, 600)
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


        self.contentsWidget = QListWidget()
        self.contentsWidget.setViewMode(QListView.ViewMode.IconMode)
        self.contentsWidget.setIconSize(QSize(140,140))					# add icon 2/6
        self.contentsWidget.setMovement(QListView.Movement.Static)		# add icon
        # self.contentsWidget.insertItem(0, 'Linked/Unlinked Bags')		# add icon
        # self.contentsWidget.insertItem(1, 'Simulation Tools')			# add icon
        self.contentsWidget.setMinimumWidth(160)
        self.contentsWidget.setMaximumWidth(160)
        self.contentsWidget.setSpacing(6)								# add icon
        # self.contentsWidget.setMaximumWidth(480)

        self.createIcons()				# add icon

        self.stack1 = QWidget()
        self.stack2 = QWidget()

        self.stack1UI()
        self.stack2UI()

        self.st = QStackedWidget(self.centralwidget)
        self.st.addWidget(self.stack1)
        self.st.addWidget(self.stack2)
        self.st.setMinimumWidth(640)
        self.st.setMinimumHeight(480)

        # print(self.size().width())  # tried to get mainwindow size

        hbox = QHBoxLayout(self.centralwidget)
        hbox.addWidget(self.contentsWidget)
        hbox.addWidget(self.st)
        hbox.setStretch(1, 100)

        self.centralwidget.setLayout(hbox)
        # self.statusbar = QMainWindow.statusBar(MainWindow)


        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        
        self.contentsWidget.currentRowChanged.connect(self.display)
        self.actionOpenFile.triggered.connect(self.openFile)
        self.actionOpenDir.triggered.connect(self.openDir)
        self.action_Exit.triggered.connect(self.exit)

        # self.createBar()


    def createIcons(self):			# add icon
    	histIcon = QListWidgetItem(self.contentsWidget)
    	histIcon.setIcon(QIcon("icon/hist-icon.jpg"))
    	histIcon.setText("Histogram")
    	histIcon.setTextAlignment(Qt.AlignHCenter)
    	histIcon.setFlags(Qt.ItemIsSelectable|Qt.ItemIsEnabled)

    	simuIcon = QListWidgetItem(self.contentsWidget)
    	simuIcon.setIcon(QIcon("icon/simul-icon.png"))
    	simuIcon.setText("Simulation")
    	simuIcon.setTextAlignment(Qt.AlignHCenter)
    	simuIcon.setFlags(Qt.ItemIsSelectable|Qt.ItemIsEnabled)
    
    def createUnlinkedBar(self):
        max_count = 0
        unlinked_bag_list = []
        try:
            df = self.unlinked['Beam Diff'].dropna()
        # unlinked_bag_list = [-144, -12, 179, 322, 312]
            unlinked_bag_list = df.values.tolist()
        except AttributeError:
            self.statusbar.showMessage('Data not ready')

        count = [0] * 4
        for num in unlinked_bag_list:
            if -1000 <= num and num <= -51:
                count[0] += 1
            elif -50 <= num and num <= -1:
                count[1] += 1
            elif 151 <= num and num <= 200:
                count[2] += 1
            elif 201 <= num:
                count[3] += 1

        # print(count)
        max_count = max(count)

        setBar = QBarSet('Beam Difference')
        setBar.append(count)

        series = QBarSeries()
        series.append(setBar)
        
        brush = QBrush(QColor(0xfdb157))
        pen = QPen(QColor(0xfdb157))
        pen.setWidth(2)
        setBar.setPen(pen)  
        setBar.setBrush(brush)

        chart = QChart()
        font = QFont()
        font.setPixelSize(18)
        chart.setTitleFont(font)

        chart.setTitle('Unlinked Bags Histogram')
        chart.addSeries(series)
        chart.setAnimationOptions(QChart.SeriesAnimations)

        labels = ['Not useful(-50 ~ -1000)', 'Pushed by operator', 'Slipping on belt', 'Not useful >201']
        axisX = QBarCategoryAxis()
        axisX.append(labels)
        # chart.setAxisX(axisX, series)
        chart.addAxis(axisX, Qt.AlignBottom)
        # chart.ChartAreas[0].AxisX.LabelAutoFitStyle = LabelAutoFitStyle.WrodWrap
        series.attachAxis(axisX)

        axisY = QValueAxis()
        axisY.setRange(0, max_count+1)
        # chart.setAxisY(axisY, series)
        chart.addAxis(axisY, Qt.AlignLeft)
        series.attachAxis(axisY)

        chart.legend().setVisible(True)
        chart.legend().setAlignment(Qt.AlignBottom)

        chartView = QChartView(chart)
        chartView.setRenderHint(QPainter.Antialiasing)

        # MainWindow.setCentralWidget(chartView)
        return chartView


    def createBar(self):
        print("in create bar")
        min_num, max_num = 0, 100
        max_count = 0
        linked_bag_list = []
        try:
            df = self.linked['Beam Diff'].dropna()
            # df = self.dp.linked['Beam Diff'].dropna()
            # print(df)
            linked_bag_list = df.values.tolist()
            min_num = int(min(linked_bag_list))
            # print(min_num)
            if min_num > 0:                 # check if greater than 0, set to 0
                min_num = 0
            max_num = int(max(linked_bag_list))

            # print(max_count)        
        except AttributeError:
            self.statusbar.showMessage('Data not ready')


        count = linked_bag_list
        count = [0] * (max_num + 1)        # choose the largest num as length of count
        
        for num in linked_bag_list:
            count[int(num)] += 1            # update every number's count

        max_count = max(count)

        setBar = QBarSet('Beam Difference')
        setBar.append(count)
        brush = QBrush(QColor(0x57B1FD))
        pen = QPen(QColor(0x57B1FD))
        pen.setWidth(2)
        setBar.setPen(pen)  
        setBar.setBrush(brush)

        series = QBarSeries()
        series.append(setBar)

        chart = QChart()
        font = QFont()
        font.setPixelSize(18)
        chart.setTitleFont(font)

        chart.setTitle('Linked Bags Histogram')
        chart.addSeries(series)
        chart.setAnimationOptions(QChart.SeriesAnimations)

        axisX = QValueAxis()
        axisX.setRange(min_num, max_num+20)
        chart.setAxisX(axisX, series)

        axisY = QValueAxis()
        axisY.setRange(0, max_count+20)
        chart.setAxisY(axisY, series)

        chart.legend().setVisible(True)
        chart.legend().setAlignment(Qt.AlignBottom)

        chartView = QChartView(chart)
        chartView.setRenderHint(QPainter.Antialiasing)

        # MainWindow.setCentralWidget(chartView)
        return chartView

    def createSummaryBar(self):
        # self.dp.dfinal

        series = QPieSeries()
        labelfont = QFont()
        labelfont.setPixelSize(11)
        try:
            series.append("Linked", len(self.linked.index))
            series.append("Unlinked", len(self.unlinked.index))
            # slices = QPieSlice()
            slices1 = series.slices()[1]
            slices1.setExploded()
            slices1.setLabelVisible()
            slices1.setPen(QPen(QColor(0x57B1FD), 2))
            slices1.setBrush(QBrush(QColor(0xfdb157)))
            slices1.setLabelPosition(QPieSlice.LabelOutside)
            slices1.setLabel(("{0} {1:.2f}%").format("Unlinked", 100*slices1.percentage()))
            slices1.setLabelFont(labelfont)

            # slices.setPen(QPen(Qt.darkGreen, 2))
            # slices.setBrush(QBrush(QColor(0xfdb157)))            
        except AttributeError:
            self.statusbar.showMessage('Data not ready')
            series.append("Total", 1)

        slices = series.slices()[0]
        
        slices.setBrush(QBrush(QColor(0x57B1FD)))
        # slices.setLabel(("%1%").format(100*slices.percentage(), 0, 'f', 1))
        # slices.setLabelPosition(QPieSlice.LabelInsideHorizontal)
        if len(series.slices()) == 2:       # display "linked" label only at data was processed
            slices.setLabelVisible()
            slices.setLabel(("{0} {1:.2f}%").format("Linked", 100*slices.percentage()))
            slices.setLabelFont(labelfont)


        chart = QChart()
        font = QFont()
        font.setPixelSize(18)
        chart.setTitleFont(font)

        chart.addSeries(series)
        chart.setAnimationOptions(QChart.SeriesAnimations)
        chart.setTitle("Total")
        chart.legend().hide()

        chartView = QChartView(chart)
        chartView.setRenderHint(QPainter.Antialiasing)

        return chartView


    def getCertainRangeList(self, total_time_lst):
        self.ready_to_plot_lst = []
        self.range0To2 = []
        self.range2To3 = []
        self.range3To6 = []
        self.range6To9 = []
        self.range9To20 = []
        for item in total_time_lst:
          if 0 < item and item <= 2:
            # print("in 0-3: ", item)
            self.ready_to_plot_lst.append(int(item))
            self.range0To2.append(item)
          elif 2 < item and item <= 3:
            self.ready_to_plot_lst.append(int(item))
            self.range2To3.append(item)
          elif 3 < item and item <= 6:
            # print("in 3-6: ", item)
            self.ready_to_plot_lst.append(int(item))
            self.range3To6.append(item)
          elif 6 < item and item <= 9:
            # print("in 6-9: ", item)       
            self.range6To9.append(item)
            self.ready_to_plot_lst.append(int(item))
          elif 9 < item and item <= 20:
            self.range9To20.append(item)    


    def onClicked(self, b):						# try to add histogram radio button 2/11 12:02
        # self.removeWidgets()
        # self.layout.addWidget(self.createBar())
        if b.text() == "Histogram":
            print("histogram checkd!")
        elif b.text() == "RangeHist":
            print("range histogram")
        elif b.text() == "Pie Chart":
            print("pie chart")

    def stack1UI(self):
        self.layout = QVBoxLayout()
        combo = QComboBox(self.stack1)
        combo.addItem("Linked Bags")
        combo.addItem("Unlinked Bags")
        combo.addItem("Summary")

        radio = QRadioButton("Histogram")		# try to add histogram radio button 2/11 12:02
        radio.setChecked(True)					# try to add histogram radio button 2/11 12:02
        radio.toggled.connect(lambda:self.onClicked(radio))	# try to add histogram radio button 2/11 12:02


        self.image = QtWidgets.QLabel(self.stack1)				# try to do stackwidget here 2/10 10:52
        self.image.setObjectName("imageLabel")						# try to do stackwidget here 2/10 10:52
        # self.displaywidget = QtWidgets.QWidget(self.stack1)			# try to do stackwidget here 2/10 10:52
        # self.displaywidget.setObjectName("displaywidget")				# try to do stackwidget here 2/10 10:52

        # self.image.setText("image")
        # self.st1 = QStackedWidget(self.stack1)							# add stackwidget 2/10 10:52
        # self.st1.addWidget(self.createBar())
        # self.st1.addWidget(self.createUnlinkedBar())
        # self.st1.addWidget(self.createSummaryBar())

        self.layout.addWidget(combo)
        self.layout.addWidget(radio)                # add radio button to choose various charts 2/11 12:02
        self.layout.addWidget(self.image)								# add stackwidget 2/10 10:52
        # self.layout.addWidget(self.st1)									# add stackwidget 2/10 10:52
        # self.layout.addWidget(self.displaywidget)
        # self.layout.addWidget(self.createBar())

        self.stack1.setLayout(self.layout)

        combo.activated[str].connect(self.onActivated)


    def stack2UI(self):
        self.vlayout = QVBoxLayout()
        hlayout = QHBoxLayout()

        combo1 = QComboBox(self.stack2)
        combo1.addItem("Distribution")
        combo1.addItem("Occurrence")
        combo1.addItem("Summary")

        label = QLabel()
        label.setText("Delay: ")
        self.text = QLineEdit()
        button = QPushButton("Go")

        hlayout.addWidget(combo1)        
        hlayout.addWidget(label)
        hlayout.addWidget(self.text)
        hlayout.addWidget(button)

        self.slayout = QHBoxLayout()

        self.labelDelay = QtWidgets.QWidget(self.stack2)
        self.labelafterDelay = QtWidgets.QWidget(self.stack2)		# try to add a paralel widget (before / after)
        self.labelDelay.setObjectName("result")

        self.labelafterDelay.setObjectName("delayResult")			# try to add a paralel widget (before / after)
        # self.labelDelay.setText("before")
        # self.labelafterDelay.setText("after")						# try to add a paralel widget (before / after)

        self.slayout.addWidget(self.labelDelay)
        self.slayout.addWidget(self.labelafterDelay)

        self.vlayout.addLayout(hlayout)
        # self.vlayout.addWidget(self.labelDelay)
        # self.vlayout.addWidget(self.labelafterDelay)
        self.vlayout.addLayout(self.slayout)
        # vlayout.addWidget(self.beforeDelay())
        self.stack2.setLayout(self.vlayout)

        button.clicked.connect(self.simulate)
        combo1.activated[str].connect(self.onActivated1)

    def afterDelayPieChart(self):
        series = QPieSeries()
        labelfont = QFont()
        labelfont.setPixelSize(11)
        try:
            series.append("Run", sum(self.tm.total_running_after_delay))
            series.append("Stop", sum(self.tm.total_stopped_after_delay))
            # slices = QPieSlice()
            slices1 = series.slices()[1]
            slices1.setExploded()
            slices1.setLabelVisible()
            slices1.setPen(QPen(QColor(0x57B1FD), 2))
            slices1.setBrush(QBrush(QColor(0xfdb157)))
            slices1.setLabelPosition(QPieSlice.LabelOutside)
            slices1.setLabel(("{0} {1:.2f}%").format("Stop", 100*slices1.percentage()))
            slices1.setLabelFont(labelfont)

            # slices.setPen(QPen(Qt.darkGreen, 2))
            # slices.setBrush(QBrush(QColor(0xfdb157)))            
        except AttributeError:
            self.statusbar.showMessage('Data not ready')
            series.append("Total", 1)

        slices = series.slices()[0]
        
        slices.setBrush(QBrush(QColor(0x57B1FD)))
        # slices.setLabel(("%1%").format(100*slices.percentage(), 0, 'f', 1))
        # slices.setLabelPosition(QPieSlice.LabelInsideHorizontal)
        if len(series.slices()) == 2:       # display "linked" label only at data was processed
            slices.setLabelVisible()
            slices.setLabel(("{0} {1:.2f}%").format("Run", 100*slices.percentage()))
            slices.setLabelFont(labelfont)


        chart = QChart()
        font = QFont()
        font.setPixelSize(18)
        chart.setTitleFont(font)

        chart.addSeries(series)
        chart.setAnimationOptions(QChart.SeriesAnimations)
        chart.setTitle("Total")
        chart.legend().hide()

        chartView = QChartView(chart)
        chartView.setRenderHint(QPainter.Antialiasing)

        return chartView

    def afterDelay(self):
        print("in after delay bar")
        min_num, max_num = 0, 100
        max_count = 0
        total_stopped_after_delay = []
        try:
            total_stopped_after_delay = self.tm.total_stopped_after_delay
            max_num = max(total_stopped_after_delay)
        except AttributeError:
            self.statusbar.showMessage('Data not ready')

        count = total_stopped_after_delay
        count = [0] * (int(max_num) + 1)        # choose the largest num as length of count
        
        for num in total_stopped_after_delay:
            count[int(num)] += 1            # update every number's count

        max_count = max(count)
        print(len(total_stopped_after_delay), max_count)
        setBar = QBarSet('stop time')
        setBar.append(count)
        brush = QBrush(QColor(0x57B1FD))
        pen = QPen(QColor(0x57B1FD))
        pen.setWidth(2)
        setBar.setPen(pen)  
        setBar.setBrush(brush)

        series = QBarSeries()
        series.append(setBar)

        chart = QChart()
        font = QFont()
        font.setPixelSize(18)
        chart.setTitleFont(font)

        chart.setTitle('Stop time Histogram (after)')
        chart.addSeries(series)
        chart.setAnimationOptions(QChart.SeriesAnimations)

        axisX = QValueAxis()
        axisX.setRange(min_num, max_num+20)
        chart.setAxisX(axisX, series)

        axisY = QValueAxis()
        axisY.setRange(0, max_count+20)
        chart.setAxisY(axisY, series)

        chart.legend().setVisible(True)
        chart.legend().setAlignment(Qt.AlignBottom)

        chartView = QChartView(chart)
        chartView.setRenderHint(QPainter.Antialiasing)

        # MainWindow.setCentralWidget(chartView)
        return chartView   

    def afterDelayDistribution(self):
        min_num, max_num = 0, 100
        max_count = 0
        total_stopped_after_delay = []
        try:
            total_stopped_after_delay = self.tm.total_stopped_after_delay
            max_num = max(total_stopped_after_delay)
        except AttributeError:
            self.statusbar.showMessage('Data not ready')

        count = total_stopped_after_delay
        # count = [0] * (int(max_num) + 1)        # choose the largest num as length of count
        
        # for num in total_stopped_after_delay:
        #     count[int(num)] += 1            # update every number's count

        max_count = max(count)
        # print(len(total_stopped_after_delay), max_count)
        setBar = QBarSet('stop time')
        setBar.append(count)
        brush = QBrush(QColor(0x57B1FD))
        pen = QPen(QColor(0x57B1FD))
        pen.setWidth(2)
        setBar.setPen(pen)  
        setBar.setBrush(brush)

        series = QBarSeries()
        series.append(setBar)

        chart = QChart()
        font = QFont()
        font.setPixelSize(18)
        chart.setTitleFont(font)

        chart.setTitle('Stop time Distribution (after)')
        chart.addSeries(series)
        chart.setAnimationOptions(QChart.SeriesAnimations)

        axisX = QValueAxis()
        axisX.setRange(min_num, max_num+20)
        chart.setAxisX(axisX, series)

        axisY = QValueAxis()
        axisY.setRange(0, max_count+20)
        chart.setAxisY(axisY, series)

        chart.legend().setVisible(True)
        chart.legend().setAlignment(Qt.AlignBottom)

        chartView = QChartView(chart)
        chartView.setRenderHint(QPainter.Antialiasing)

        # MainWindow.setCentralWidget(chartView)
        return chartView   

    def beforeDelayPieChart(self):
        series = QPieSeries()
        labelfont = QFont()
        labelfont.setPixelSize(11)
        try:
            series.append("Run", sum(self.tm.total_running_time))
            series.append("Stop", sum(self.tm.total_stopped_time))
            # slices = QPieSlice()
            slices1 = series.slices()[1]
            slices1.setExploded()
            slices1.setLabelVisible()
            slices1.setPen(QPen(QColor(0x57B1FD), 2))
            slices1.setBrush(QBrush(QColor(0xfdb157)))
            slices1.setLabelPosition(QPieSlice.LabelOutside)
            slices1.setLabel(("{0} {1:.2f}%").format("Stop", 100*slices1.percentage()))
            slices1.setLabelFont(labelfont)

            # slices.setPen(QPen(Qt.darkGreen, 2))
            # slices.setBrush(QBrush(QColor(0xfdb157)))            
        except AttributeError:
            self.statusbar.showMessage('Data not ready')
            series.append("Total", 1)

        slices = series.slices()[0]
        
        slices.setBrush(QBrush(QColor(0x57B1FD)))
        # slices.setLabel(("%1%").format(100*slices.percentage(), 0, 'f', 1))
        # slices.setLabelPosition(QPieSlice.LabelInsideHorizontal)
        if len(series.slices()) == 2:       # display "linked" label only at data was processed
            slices.setLabelVisible()
            slices.setLabel(("{0} {1:.2f}%").format("Run", 100*slices.percentage()))
            slices.setLabelFont(labelfont)


        chart = QChart()
        font = QFont()
        font.setPixelSize(18)
        chart.setTitleFont(font)

        chart.addSeries(series)
        chart.setAnimationOptions(QChart.SeriesAnimations)
        chart.setTitle("Total")
        chart.legend().hide()

        chartView = QChartView(chart)
        chartView.setRenderHint(QPainter.Antialiasing)

        return chartView

    def beforeDelay(self):
        print("in before delay bar")
        min_num, max_num = 0, 100
        max_count = 0
        total_stopped_time = []
        try:
            total_stopped_time = self.tm.total_stopped_time
            max_num = max(total_stopped_time)
        except AttributeError:
            self.statusbar.showMessage('Data not ready')

        count = total_stopped_time
        count = [0] * (int(max_num) + 1)        # choose the largest num as length of count
        
        for num in total_stopped_time:
            count[int(num)] += 1            # update every number's count

        max_count = max(count)
        print(len(total_stopped_time), max_count)
        setBar = QBarSet('stop time')
        setBar.append(count)
        brush = QBrush(QColor(0x57B1FD))
        pen = QPen(QColor(0x57B1FD))
        pen.setWidth(2)
        setBar.setPen(pen)  
        setBar.setBrush(brush)

        series = QBarSeries()
        series.append(setBar)

        chart = QChart()
        font = QFont()
        font.setPixelSize(18)
        chart.setTitleFont(font)

        chart.setTitle('Stop time Histogram (before)')
        chart.addSeries(series)
        chart.setAnimationOptions(QChart.SeriesAnimations)

        axisX = QValueAxis()
        axisX.setRange(min_num, max_num+20)
        chart.setAxisX(axisX, series)

        axisY = QValueAxis()
        axisY.setRange(0, max_count+20)
        chart.setAxisY(axisY, series)

        chart.legend().setVisible(True)
        chart.legend().setAlignment(Qt.AlignBottom)

        chartView = QChartView(chart)
        chartView.setRenderHint(QPainter.Antialiasing)

        # MainWindow.setCentralWidget(chartView)
        return chartView    	

    def beforeDelayDistribution(self):
        min_num, max_num = 0, 100
        max_count = 0
        total_stopped_time = []
        try:
            total_stopped_time = self.tm.total_stopped_time
            max_num = max(total_stopped_time)
        except AttributeError:
            self.statusbar.showMessage('Data not ready')

        count = total_stopped_time
        # count = [0] * (int(max_num) + 1)        # choose the largest num as length of count
        
        # for num in total_stopped_time:
        #     count[int(num)] += 1            # update every number's count

        max_count = max(count)
        setBar = QBarSet('stop time')
        setBar.append(count)
        brush = QBrush(QColor(0x57B1FD))
        pen = QPen(QColor(0x57B1FD))
        pen.setWidth(2)
        setBar.setPen(pen)  
        setBar.setBrush(brush)

        series = QBarSeries()
        series.append(setBar)

        chart = QChart()
        font = QFont()
        font.setPixelSize(18)
        chart.setTitleFont(font)

        chart.setTitle('Stop time Distribution (before)')
        chart.addSeries(series)
        chart.setAnimationOptions(QChart.SeriesAnimations)

        axisX = QValueAxis()
        axisX.setRange(min_num, max_num+20)
        chart.setAxisX(axisX, series)

        axisY = QValueAxis()
        axisY.setRange(0, max_count+20)
        chart.setAxisY(axisY, series)

        chart.legend().setVisible(True)
        chart.legend().setAlignment(Qt.AlignBottom)

        chartView = QChartView(chart)
        chartView.setRenderHint(QPainter.Antialiasing)

        # MainWindow.setCentralWidget(chartView)
        return chartView  

    def display(self, i):
        self.st.setCurrentIndex(i)


    # mainMenu components
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

    def removeWidgets(self):
        for i in reversed(range(3,self.layout.count())):                # change 2 to 3 if add another widget(radio)
            self.layout.itemAt(i).widget().setParent(None)


    def onActivated1(self, text):
    	if text == 'Distribution':
    		self.removeWidgets1()
    		self.slayout.addWidget(self.beforeDelayDistribution(), QtCore.Qt.AlignLeft)
    		self.slayout.addWidget(self.afterDelayDistribution(), QtCore.Qt.AlignLeft)
    	elif text == 'Occurrence':
    		self.removeWidgets1()
    		self.slayout.addWidget(self.beforeDelay(), QtCore.Qt.AlignLeft)
    		self.slayout.addWidget(self.afterDelay(), QtCore.Qt.AlignLeft)
    	elif text == 'Summary':
    		self.removeWidgets1()
    		self.slayout.addWidget(self.beforeDelayPieChart(), QtCore.Qt.AlignLeft)
    		self.slayout.addWidget(self.afterDelayPieChart(), QtCore.Qt.AlignLeft)


    # combo box items
    def onActivated(self, text):
        print(text)
        if text == 'Linked Bags':
            # self.image.setPixmap(QtGui.QPixmap('link.png'))
            # self.createBar()
            # self.st1.setCurrentIndex(0)
            # self.st1.removeWidget(self.createBar())
            # self.st1.insertWidget(0, self.createBar())
            self.removeWidgets()
            self.layout.addWidget(self.createBar())
        elif text == 'Unlinked Bags':
            # self.image.setPixmap(QtGui.QPixmap('unlink.png'))
            # self.st1.setCurrentIndex(1)
            self.removeWidgets()
            self.layout.addWidget(self.createUnlinkedBar())
        elif text == 'Summary':
            # self.image.setPixmap(QtGui.QPixmap('his.png'))
            # self.st1.setCurrentIndex(2)
            self.removeWidgets()            
            self.layout.addWidget(self.createSummaryBar())

    def simulate(self):
        print(self.text.text())
        if bool(re.match('^[0-9]+$',self.text.text())):
            self.tm = TimeMeasure('runtime_.txt', int(self.text.text()))		# change variables to global value 2/11 2:06
            self.tm.getDuration()
            self.tm.runList("")
            self.tm.stopList("")
            self.total_time = self.tm.org_finish_time - self.tm.org_start_time

            # self.labelDelay.setText("Simulation Result:\n")
            # self.labelDelay.setText(self.labelDelay.text() + "\n---------------Before delay---------------\n\n")
            # self.labelDelay.setText(self.labelDelay.text() + "Run Time total: {0:d} Sum: {1:f} seconds Percentage: {2:.2f}%\n".format(len(self.tm.total_running_time), sum(self.tm.total_running_time), sum(self.tm.total_running_time)/self.total_time * 100))
            # self.labelDelay.setText(self.labelDelay.text() + "Stop Time total: {0:d} Sum: {1:f} seconds Percentage: {2:.2f}%\n".format(len(self.tm.total_stopped_time), sum(self.tm.total_stopped_time), sum(self.tm.total_stopped_time)/self.total_time * 100))
            # self.labelDelay.setText(self.labelDelay.text() + "Total: {0:f} seconds Percentage: {1:.2f}%\n".format(self.total_time, sum(self.tm.total_running_time)/self.total_time * 100 + sum(self.tm.total_stopped_time)/self.total_time * 100))
            # # print("run:",len(tm.total_running_time), "sum:", sum(tm.total_running_time),"percentage:",sum(tm.total_running_time)/total_time * 100)
            # # print("stop:",len(tm.total_stopped_time), "sum:", sum(tm.total_stopped_time),"percentage:",sum(tm.total_stopped_time)/total_time * 100)
            # # print("total:",total_time, sum(tm.total_running_time)/total_time * 100 + sum(tm.total_stopped_time)/total_time * 100)
            # # print("\n---------------Add delay 2 seconds---------------\n")
            # self.labelDelay.setText(self.labelDelay.text() + "\n---------------Add delay 2 seconds---------------\n\n")
            self.tm.runListDelay("")
            self.tm.stopListDelay("")
            # self.total_time_after_delay = self.tm.delay_finish_time - self.tm.delay_start_time
            # self.labelDelay.setText(self.labelDelay.text() + "Run time after delay: {0:d} Sum: {1:f} seconds Percentage: {2:.2f}%\n".format(len(self.tm.total_running_after_delay), sum(self.tm.total_running_after_delay), sum(self.tm.total_running_after_delay) / self.total_time_after_delay * 100))
            # self.labelDelay.setText(self.labelDelay.text() + "Stop time after delay: {0:d} Sum: {1:f} seconds Percentage: {2:.2f}%\n".format(len(self.tm.total_stopped_after_delay), sum(self.tm.total_stopped_after_delay), sum(self.tm.total_stopped_after_delay) / self.total_time_after_delay * 100))
            # self.labelDelay.setText(self.labelDelay.text() + "Total: {0:f} seconds Percentage: {1:.2f}%\n".format(self.total_time_after_delay, sum(self.tm.total_running_after_delay) / self.total_time_after_delay * 100 + sum(self.tm.total_stopped_after_delay) / self.total_time_after_delay * 100))
            # # print("run after delay:", len(tm.total_running_after_delay), "sum:", sum(tm.total_running_after_delay), "percentage:",sum(tm.total_running_after_delay) / total_time_after_delay * 100)
            # # print("stop after delay:",len(tm.total_stopped_after_delay), "sum:", sum(tm.total_stopped_after_delay), "percentage:",sum(tm.total_stopped_after_delay) / total_time_after_delay * 100)
            # # print("total:",total_time_after_delay, sum(tm.total_running_after_delay) / total_time_after_delay * 100 + sum(tm.total_stopped_after_delay) / total_time_after_delay * 100)

            # self.tm.fakestopList()
            # self.delaylist = self.tm.getCertainRangeList(self.tm.fake_total_stopped_time)
            # # print("\nSummary:")
            # # print("Before delay XRAY_MIN / total: 100% ----> After delay XRAY_MIN / total: {0:.2f}%".format((len(tm.fake_total_stopped_time)-len(delaylist))/len(tm.fake_total_stopped_time)*100))
            # # print("Before delay total time: 100% ----> After delay total time: {0:.2f}%".format(total_time_after_delay/total_time*100))
            # self.labelDelay.setText(self.labelDelay.text() + "\nSummary:")
            # self.labelDelay.setText(self.labelDelay.text() + "Before delay total time: 100% ----> After delay total time: {0:.2f}%\n".format(self.total_time_after_delay/self.total_time*100))
            # self.labelDelay.setText(self.labelDelay.text() + "Before delay XRAY_MIN / total: 100% ----> After delay XRAY_MIN / total: {0:.2f}%".format((len(self.tm.fake_total_stopped_time)-len(self.delaylist))/len(self.tm.fake_total_stopped_time)*100))
            # self.labelDelay.setFont(QtGui.QFont("Times", 12, QtGui.QFont.Bold))
            # self.labelDelay.setAlignment(Qt.AlignTop)#HCenter)

            self.removeWidgets1()
            # self.vlayout.addWidget(self.beforeDelay())
            self.slayout.addWidget(self.beforeDelay(), QtCore.Qt.AlignLeft)
            # self.vlayout.addWidget(self.afterDelayPieChart())
            # self.vlayout.addWidget(self.afterDelay())
            self.slayout.addWidget(self.afterDelay(), QtCore.Qt.AlignLeft)

    def removeWidgets1(self):
        for i in reversed(range(2,self.slayout.count())):                # change 2 to 3 if add another widget(radio)
            self.slayout.itemAt(i).widget().setParent(None)

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
                # self.statusbar.showMessage('Processing Files...')
                pp = PreProc(filenames)     # pass files into PreProc class
                # self.statusbar.showMessage('Analyzing datas...')
                dp = DataProc()     # pass the prepared data into DataProc class
                self.linked = dp.linked
                self.unlinked = dp.unlinked
                self.statusbar.showMessage('Done')
                self.removeWidgets()
                self.layout.addWidget(self.createBar())
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
                self.dp = DataProc()     # pass the prepared data into DataProc class
                self.statusbar.showMessage('Done')
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