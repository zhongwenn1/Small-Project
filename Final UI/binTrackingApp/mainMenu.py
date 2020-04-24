import sys
import os
import re
from PyQt5 import QtCore,  QtWidgets
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QGridLayout, QComboBox, QLabel, QFileDialog, QGroupBox, \
    QMessageBox, QTextEdit, QTabWidget, QLineEdit, QPushButton, QProgressDialog, QWidget, QProgressBar
from PyQt5.QtGui import QBrush, QPen, QColor, QFont, QPainter
from PyQt5.QtChart import QChart, QChartView, QValueAxis, QBarSet, QBarSeries, QPieSeries, QLineSeries, QBarCategoryAxis, QPercentBarSeries, QPieSlice
from preProc import PreProc
from dataProc import DataProc
from simulationTool import TimeMeasure
import config as cfg
import timeit


class Ui_MainWindow(object):
    def setupUi(self, MainWindow, app):
        self.app = app
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1000, 680)

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

        self.tabwidget = QTabWidget()
        self.tabwidget.setObjectName("tabWidget")

        self.binTrackingTab = QtWidgets.QWidget()
        self.binTrackingTab.setObjectName("binTracking")
        self.grid = QGridLayout()
        self.binTrackingTab.setLayout(self.grid)
        self.grid.addWidget(self.createSummary(), 0, 0)
        self.grid.addWidget(self.createBar(), 0, 1)
        self.grid.addWidget(self.createUnlinkedSummary(), 1, 0)
        self.grid.addWidget(self.createFileList(), 1, 1)
        self.grid.setColumnStretch(0, 1)
        self.grid.setColumnStretch(1, 3)
        self.grid.setRowStretch(0, 3)
        self.grid.setRowStretch(1, 1)

        self.simulationTab = QtWidgets.QWidget()
        self.simulationTab.setObjectName("simulation")
        self.slayout = QGridLayout()
        self.simulationTab.setLayout(self.slayout)
        self.slayout.addWidget(self.createInfo(), 0, 0, 0, 1)
        self.slayout.addWidget(self.beforeDelayDistribution(), 0, 1)
        self.slayout.addWidget(self.afterDelayDistribution(), 1, 1)
        self.slayout.setColumnStretch(0, 1)
        self.slayout.setColumnStretch(1, 3)

        self.tabwidget.addTab(self.binTrackingTab, "Bin Tracking")
        self.tabwidget.addTab(self.simulationTab, "Simulation")
        MainWindow.setCentralWidget(self.tabwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        
        self.actionOpenFile.triggered.connect(self.openFile)
        self.actionOpenDir.triggered.connect(self.openDir)
        self.action_Exit.triggered.connect(self.exit)

    def createInfo(self):
        groupbox = QGroupBox("Summary")
        vlayout = QVBoxLayout()
        groupbox.setLayout(vlayout)

        hlayout = QHBoxLayout()
        combo = QComboBox()
        combo.addItem("Distribution")
        combo.addItem("Occurrence")
        combo.addItem("Summary")

        label = QLabel()
        label.setText("Delay: ")
        self.text = QLineEdit()
        button = QPushButton("Go")

        hlayout.addWidget(label)
        hlayout.addWidget(self.text)
        hlayout.addWidget(button)

        vlayout.addWidget(combo)
        vlayout.addLayout(hlayout)

        total_time_layout = QHBoxLayout()
        vlayout.addLayout(total_time_layout)
        total_time_label = QLabel("Total Time (before)")
        total_time_layout.addWidget(total_time_label)

        total_time_seconds_layout = QHBoxLayout()
        vlayout.addLayout(total_time_seconds_layout)
        total_time_seconds_label = QLabel("Seconds:")
        self.total_time_seconds_text = QLabel('0')
        self.total_time_seconds_text.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignCenter)
        total_time_seconds_layout.addWidget(total_time_seconds_label)
        total_time_seconds_layout.addWidget(self.total_time_seconds_text)

        total_time_minutes_layout = QHBoxLayout()
        vlayout.addLayout(total_time_minutes_layout)
        total_time_minutes_label = QLabel("Minutes:")
        self.total_time_minutes_text = QLabel('0')
        self.total_time_minutes_text.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignCenter)
        total_time_minutes_layout.addWidget(total_time_minutes_label)
        total_time_minutes_layout.addWidget(self.total_time_minutes_text)

        total_time_hours_layout = QHBoxLayout()
        vlayout.addLayout(total_time_hours_layout)
        total_time_hours_label = QLabel("Hours:")
        self.total_time_hours_text = QLabel('0')
        self.total_time_hours_text.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignCenter)
        total_time_hours_layout.addWidget(total_time_hours_label)
        total_time_hours_layout.addWidget(self.total_time_hours_text)


        total_stop_time_layout = QHBoxLayout()
        vlayout.addLayout(total_stop_time_layout)
        total_stop_time_label = QLabel("Total Stop Time (before)")
        total_stop_time_layout.addWidget(total_stop_time_label)

        total_stop_time_seconds_layout = QHBoxLayout()
        vlayout.addLayout(total_stop_time_seconds_layout)
        total_stop_time_seconds_label = QLabel("Seconds:")
        self.total_stop_time_seconds_text = QLabel('0')
        self.total_stop_time_seconds_text.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignCenter)
        total_stop_time_seconds_layout.addWidget(total_stop_time_seconds_label)
        total_stop_time_seconds_layout.addWidget(self.total_stop_time_seconds_text)

        total_stop_time_minutes_layout = QHBoxLayout()
        vlayout.addLayout(total_stop_time_minutes_layout)
        total_stop_time_minutes_label = QLabel("Minutes:")
        self.total_stop_time_minutes_text = QLabel('0')
        self.total_stop_time_minutes_text.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignCenter)
        total_stop_time_minutes_layout.addWidget(total_stop_time_minutes_label)
        total_stop_time_minutes_layout.addWidget(self.total_stop_time_minutes_text)

        total_stop_time_hours_layout = QHBoxLayout()
        vlayout.addLayout(total_stop_time_hours_layout)
        total_stop_time_hours_label = QLabel("Hours:")
        self.total_stop_time_hours_text = QLabel('0')
        self.total_stop_time_hours_text.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignCenter)
        total_stop_time_hours_layout.addWidget(total_stop_time_hours_label)
        total_stop_time_hours_layout.addWidget(self.total_stop_time_hours_text)

        divider_label = QLabel("----------------------------------------------------------")
        vlayout.addWidget(divider_label)

        total_duration_layout = QHBoxLayout()
        vlayout.addLayout(total_duration_layout)
        total_duration_label = QLabel("Total Stop Duration: ")
        self.total_duration_text = QLabel('0')
        self.total_duration_text.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignCenter)
        total_duration_layout.addWidget(total_duration_label)
        total_duration_layout.addWidget(self.total_duration_text)

        total_duration_in_range_layout = QHBoxLayout()
        vlayout.addLayout(total_duration_in_range_layout)
        total_duration_in_range_label = QLabel("Total Duration to Save: ")
        self.total_duration_in_range_text = QLabel('0')
        self.total_duration_in_range_text.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignCenter)
        total_duration_in_range_layout.addWidget(total_duration_in_range_label)
        total_duration_in_range_layout.addWidget(self.total_duration_in_range_text)

        time_save_layout = QHBoxLayout()
        vlayout.addLayout(time_save_layout)
        time_save_label = QLabel("Time Save")
        time_save_layout.addWidget(time_save_label)

        time_save_seconds_layout = QHBoxLayout()
        vlayout.addLayout(time_save_seconds_layout)
        time_save_seconds_label = QLabel("Seconds:")
        self.time_save_seconds_text = QLabel('0')
        self.time_save_seconds_text.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignCenter)
        time_save_seconds_layout.addWidget(time_save_seconds_label)
        time_save_seconds_layout.addWidget(self.time_save_seconds_text)

        time_save_minutes_layout = QHBoxLayout()
        vlayout.addLayout(time_save_minutes_layout)
        time_save_minutes_label = QLabel("Minutes:")
        self.time_save_minutes_text = QLabel('0')
        self.time_save_minutes_text.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignCenter)
        time_save_minutes_layout.addWidget(time_save_minutes_label)
        time_save_minutes_layout.addWidget(self.time_save_minutes_text)

        time_save_hours_layout = QHBoxLayout()
        vlayout.addLayout(time_save_hours_layout)
        time_save_hours_label = QLabel("Hours:")
        self.time_save_hours_text = QLabel('0')
        self.time_save_hours_text.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignCenter)
        time_save_hours_layout.addWidget(time_save_hours_label)
        time_save_hours_layout.addWidget(self.time_save_hours_text)

        time_add_layout = QHBoxLayout()
        vlayout.addLayout(time_add_layout)
        time_add_label = QLabel("Time Add")
        time_add_layout.addWidget(time_add_label)

        time_add_seconds_layout = QHBoxLayout()
        vlayout.addLayout(time_add_seconds_layout)
        time_add_seconds_label = QLabel("Seconds:")
        self.time_add_seconds_text = QLabel('0')
        self.time_add_seconds_text.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignCenter)
        time_add_seconds_layout.addWidget(time_add_seconds_label)
        time_add_seconds_layout.addWidget(self.time_add_seconds_text)

        time_add_minutes_layout = QHBoxLayout()
        vlayout.addLayout(time_add_minutes_layout)
        time_add_minutes_label = QLabel("Minutes:")
        self.time_add_minutes_text = QLabel('0')
        self.time_add_minutes_text.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignCenter)
        time_add_minutes_layout.addWidget(time_add_minutes_label)
        time_add_minutes_layout.addWidget(self.time_add_minutes_text)

        time_add_hours_layout = QHBoxLayout()
        vlayout.addLayout(time_add_hours_layout)
        time_add_hours_label = QLabel("Hours:")
        self.time_add_hours_text = QLabel('0')
        self.time_add_hours_text.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignCenter)
        time_add_hours_layout.addWidget(time_add_hours_label)
        time_add_hours_layout.addWidget(self.time_add_hours_text)

        divider_label = QLabel("----------------------------------------------------------")
        vlayout.addWidget(divider_label)

        total_time_after_delay_layout = QHBoxLayout()
        vlayout.addLayout(total_time_after_delay_layout)
        total_time_after_delay_label = QLabel("Total Time (after)")
        total_time_after_delay_layout.addWidget(total_time_after_delay_label)

        total_time_after_delay_seconds_layout = QHBoxLayout()
        vlayout.addLayout(total_time_after_delay_seconds_layout)
        total_time_after_delay_seconds_label = QLabel("Seconds:")
        self.total_time_after_delay_seconds_text = QLabel('0')
        self.total_time_after_delay_seconds_text.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignCenter)
        total_time_after_delay_seconds_layout.addWidget(total_time_after_delay_seconds_label)
        total_time_after_delay_seconds_layout.addWidget(self.total_time_after_delay_seconds_text)

        total_time_after_delay_minutes_layout = QHBoxLayout()
        vlayout.addLayout(total_time_after_delay_minutes_layout)
        total_time_after_delay_minutes_label = QLabel("Minutes:")
        self.total_time_after_delay_minutes_text = QLabel('0')
        self.total_time_after_delay_minutes_text.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignCenter)
        total_time_after_delay_minutes_layout.addWidget(total_time_after_delay_minutes_label)
        total_time_after_delay_minutes_layout.addWidget(self.total_time_after_delay_minutes_text)

        total_time_after_delay_hours_layout = QHBoxLayout()
        vlayout.addLayout(total_time_after_delay_hours_layout)
        total_time_after_delay_hours_label = QLabel("Hours:")
        self.total_time_after_delay_hours_text = QLabel('0')
        self.total_time_after_delay_hours_text.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignCenter)
        total_time_after_delay_hours_layout.addWidget(total_time_after_delay_hours_label)
        total_time_after_delay_hours_layout.addWidget(self.total_time_after_delay_hours_text)

        total_stop_time_delay_layout = QHBoxLayout()
        vlayout.addLayout(total_stop_time_delay_layout)
        total_stop_time_delay_label = QLabel("Total Stop Time (after)")
        total_stop_time_delay_layout.addWidget(total_stop_time_delay_label)

        total_stop_time_delay_seconds_layout = QHBoxLayout()
        vlayout.addLayout(total_stop_time_delay_seconds_layout)
        total_stop_time_delay_seconds_label = QLabel("Seconds:")
        self.total_stop_time_delay_seconds_text = QLabel('0')
        self.total_stop_time_delay_seconds_text.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignCenter)
        total_stop_time_delay_seconds_layout.addWidget(total_stop_time_delay_seconds_label)
        total_stop_time_delay_seconds_layout.addWidget(self.total_stop_time_delay_seconds_text)

        total_stop_time_delay_minutes_layout = QHBoxLayout()
        vlayout.addLayout(total_stop_time_delay_minutes_layout)
        total_stop_time_delay_minutes_label = QLabel("Minutes:")
        self.total_stop_time_delay_minutes_text = QLabel('0')
        self.total_stop_time_delay_minutes_text.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignCenter)
        total_stop_time_delay_minutes_layout.addWidget(total_stop_time_delay_minutes_label)
        total_stop_time_delay_minutes_layout.addWidget(self.total_stop_time_delay_minutes_text)

        total_stop_time_delay_hours_layout = QHBoxLayout()
        vlayout.addLayout(total_stop_time_delay_hours_layout)
        total_stop_time_delay_hours_label = QLabel("Hours:")
        self.total_stop_time_delay_hours_text = QLabel('0')
        self.total_stop_time_delay_hours_text.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignCenter)
        total_stop_time_delay_hours_layout.addWidget(total_stop_time_delay_hours_label)
        total_stop_time_delay_hours_layout.addWidget(self.total_stop_time_delay_hours_text)

        self.currSimText = "Distribution"
        button.clicked.connect(self.simulate)
        combo.activated[str].connect(self.onActivated1)
        return groupbox

    def onActivated1(self, text):
        self.currSimText = text
        if text == 'Distribution':
            self.slayout.addWidget(self.beforeDelayDistribution(), 0, 1)
            self.slayout.addWidget(self.afterDelayDistribution(), 1, 1)
        elif text == 'Occurrence':
            self.slayout.addWidget(self.beforeDelay(), 0, 1)
            self.slayout.addWidget(self.afterDelay(), 1, 1)
        elif text == 'Summary':
            self.slayout.addWidget(self.beforeDelayPieChart(), 0, 1)
            self.slayout.addWidget(self.afterDelayPieChart(), 1, 1)

    def beforeDelayDistribution(self):
        min_num, max_num = 0, 100
        max_count = 0
        count = [0]
        try:
            total_stopped_time = self.tm.total_stopped_time
            max_num = len(total_stopped_time)
            count = total_stopped_time
            max_count = max(count)
        except (AttributeError, ValueError):
            self.statusbar.showMessage('Data not ready')

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
        axisX.setRange(min_num, max_num)
        chart.setAxisX(axisX, series)

        axisY = QValueAxis()
        axisY.setRange(0, max_count + 20)
        chart.setAxisY(axisY, series)

        chart.legend().setVisible(True)
        chart.legend().setAlignment(QtCore.Qt.AlignBottom)

        chartView = QChartView(chart)
        chartView.setRenderHint(QPainter.Antialiasing)

        return chartView

    def afterDelayDistribution(self):
        min_num, max_num = 0, 100
        max_count = 0
        count = [0]
        try:
            total_stopped_after_delay = self.tm.total_stopped_after_delay
            max_num = len(total_stopped_after_delay)
            count = total_stopped_after_delay
            max_count = max(count)
        except (AttributeError, ValueError):
            self.statusbar.showMessage('Data not ready')

        setBar = QBarSet('stop time')
        setBar.append(count)
        brush = QBrush(QColor(0xA6E22E))		# Green
        pen = QPen(QColor(0xA6E22E))			# Green
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
        axisX.setRange(min_num, max_num)
        chart.setAxisX(axisX, series)

        axisY = QValueAxis()
        axisY.setRange(0, max_count+20)
        chart.setAxisY(axisY, series)

        chart.legend().setVisible(True)
        chart.legend().setAlignment(QtCore.Qt.AlignBottom)

        chartView = QChartView(chart)
        chartView.setRenderHint(QPainter.Antialiasing)

        return chartView

    def beforeDelay(self):
        min_num, max_num = 0, 100
        max_count = 0
        count = []
        try:
            total_stopped_time = self.tm.total_stopped_time
            max_num = max(total_stopped_time)
            count = [0] * (int(max_num) + 1)  # choose the largest num as length of count

            for num in total_stopped_time:
                count[int(num)] += 1  # update every number's count

            max_count = max(count)
        except (AttributeError, ValueError):
            self.statusbar.showMessage('Data not ready')

        series = QLineSeries()
        for i in range(len(count)):
            series.append(i, count[i])
        series.setName('Stop Time Occurrence')
        
        brush = QBrush(QColor(0x57B1FD))
        pen = QPen(QColor(0x57B1FD))
        pen.setWidth(3)
        series.setPen(pen)
        series.setBrush(brush)

        chart = QChart()
        font = QFont()
        font.setPixelSize(18)
        chart.setTitleFont(font)

        chart.setTitle('Stop time Occurrence (before)')
        chart.addSeries(series)
        chart.setAnimationOptions(QChart.SeriesAnimations)

        axisX = QValueAxis()
        axisX.setRange(min_num, max_num + 20)
        chart.setAxisX(axisX, series)

        axisY = QValueAxis()
        axisY.setRange(0, max_count + 20)
        chart.setAxisY(axisY, series)

        chart.legend().setVisible(True)
        chart.legend().setAlignment(QtCore.Qt.AlignBottom)

        chartView = QChartView(chart)
        chartView.setRenderHint(QPainter.Antialiasing)

        return chartView

    def afterDelay(self):
        min_num, max_num = 0, 100
        max_count = 0
        count = []
        try:
            total_stopped_after_delay = self.tm.total_stopped_after_delay
            max_num = max(total_stopped_after_delay)
            count = [0] * (int(max_num) + 1)  # choose the largest num as length of count

            for num in total_stopped_after_delay:
                count[int(num)] += 1  # update every number's count

            max_count = max(count)

        except (AttributeError, ValueError):
            self.statusbar.showMessage('Data not ready')

        series = QLineSeries()
        for i in range(len(count)):
            series.append(i, count[i])
        series.setName('Stop Time Occurrence')

        brush = QBrush(QColor(0xA6E22E))  # Green
        pen = QPen(QColor(0xA6E22E))
        pen.setWidth(3)
        series.setPen(pen)
        series.setBrush(brush)

        chart = QChart()
        font = QFont()
        font.setPixelSize(18)
        chart.setTitleFont(font)

        chart.setTitle('Stop time Occurrence (after)')
        chart.addSeries(series)
        chart.setAnimationOptions(QChart.SeriesAnimations)

        axisX = QValueAxis()
        axisX.setRange(min_num, max_num + 20)
        chart.setAxisX(axisX, series)

        axisY = QValueAxis()
        axisY.setRange(0, max_count + 20)
        chart.setAxisY(axisY, series)

        chart.legend().setVisible(True)
        chart.legend().setAlignment(QtCore.Qt.AlignBottom)

        chartView = QChartView(chart)
        chartView.setRenderHint(QPainter.Antialiasing)

        return chartView

    def beforeDelayPieChart(self):
        series = QPieSeries()
        labelfont = QFont()
        labelfont.setPixelSize(11)
        total_running_time, total_stopped_time = 0, 0
        try:
            total_stopped_time = sum(self.tm.total_stopped_time)
            total_running_time = self.tm.total_time_before_delay - total_stopped_time

        except AttributeError:
            self.statusbar.showMessage('Data not ready')

        series.append("Run", total_running_time)
        series.append("Stop", total_stopped_time)

        slices = series.slices()[0]
        slices.setBrush(QBrush(QColor(0x57B1FD)))
        slices.setLabel(("{0} {1:.2f}%").format("Run Time", 100*slices.percentage()))
        slices.setLabelFont(labelfont)

        slices1 = series.slices()[1]
        slices1.setExploded()
        slices1.setPen(QPen(QColor(0x57B1FD), 2))
        slices1.setBrush(QBrush(QColor(0xfdb157)))
        slices1.setLabel(("{0} {1:.2f}%").format("Stop Time", 100*slices1.percentage()))
        slices1.setLabelFont(labelfont)

        chart = QChart()
        font = QFont()
        font.setPixelSize(18)
        chart.setTitleFont(font)

        chart.addSeries(series)
        chart.setAnimationOptions(QChart.SeriesAnimations)
        chart.setTitle("Total Time (before)")

        chartView = QChartView(chart)
        chartView.setRenderHint(QPainter.Antialiasing)

        return chartView

    def afterDelayPieChart(self):
        series = QPieSeries()
        labelfont = QFont()
        labelfont.setPixelSize(11)
        total_running_after_delay, total_stopped_after_delay = 0, 0
        try:
            total_stopped_after_delay = sum(self.tm.total_stopped_after_delay)
            total_running_after_delay = self.tm.total_time_after_delay - total_stopped_after_delay

        except AttributeError:
            self.statusbar.showMessage('Data not ready')

        series.append("Run", total_running_after_delay)
        series.append("Stop", total_stopped_after_delay)

        slices = series.slices()[0]   					# Run time slice
        slices.setBrush(QBrush(QColor(0x57B1FD)))		# Blue
        slices.setLabel(("{0} {1:.2f}%").format("Run time", 100*slices.percentage()))	# Set percentage
        slices.setLabelFont(labelfont)        			# Set label font

        slices1 = series.slices()[1]					# Stop time slice
        slices1.setExploded()							# Set stop slice exploded
        slices1.setPen(QPen(QColor(0x57B1FD), 2))		# Blue
        slices1.setBrush(QBrush(QColor(0xA6E22E)))		# Orange
        slices1.setLabel(("{0} {1:.2f}%").format("Stop time", 100*slices1.percentage()))	# Set percentage
        slices1.setLabelFont(labelfont)        			# Set label font

        chart = QChart()
        font = QFont()
        font.setPixelSize(18)
        chart.setTitleFont(font)

        chart.addSeries(series)
        chart.setAnimationOptions(QChart.SeriesAnimations)
        chart.setTitle("Total Time (after)")

        chartView = QChartView(chart)
        chartView.setRenderHint(QPainter.Antialiasing)

        return chartView

    def simulate(self):
        if bool(re.match('^[0-9]+$', self.text.text())):
            try:
                self.tm = TimeMeasure(int(self.text.text()))
                self.tm.get_duration()
                self.tm.get_summary()
                total_time_before_delay = self.tm.total_time_before_delay
                total_stop_time_before_delay = sum(self.tm.total_stopped_time)
                total_stop_duration = len(self.tm.total_stopped_time)
                total_in_range = self.tm.count
                time_save = self.tm.time_save
                time_add = self.tm.time_add
                total_stop_time_after_delay = sum(self.tm.total_stopped_after_delay)
                total_time_after_delay = self.tm.total_time_after_delay

                self.total_time_seconds_text.setText("{0:.2f}".format(total_time_before_delay))
                self.total_time_minutes_text.setText("{0:.2f}".format(total_time_before_delay/60))
                self.total_time_hours_text.setText("{0:.2f}".format(total_time_before_delay/3600))
                self.total_stop_time_seconds_text.setText("{0:.2f}".format(total_stop_time_before_delay))
                self.total_stop_time_minutes_text.setText("{0:.2f}".format(total_stop_time_before_delay/60))
                self.total_stop_time_hours_text.setText("{0:.2f}".format(total_stop_time_before_delay/3600))
                self.total_duration_text.setText("{0}".format(total_stop_duration))
                self.total_duration_in_range_text.setText("{0}".format(total_in_range))
                self.time_save_seconds_text.setText("{0:.2f}".format(time_save))
                self.time_save_minutes_text.setText("{0:.2f}".format(time_save/60))
                self.time_save_hours_text.setText("{0:.2f}".format(time_save/3600))
                self.time_add_seconds_text.setText("{0:.2f}".format(time_add))
                self.time_add_minutes_text.setText("{0:.2f}".format(time_add/60))
                self.time_add_hours_text.setText("{0:.2f}".format(time_add/3600))
                self.total_stop_time_delay_seconds_text.setText("{0:.2f}".format(total_stop_time_after_delay))
                self.total_stop_time_delay_minutes_text.setText("{0:.2f}".format(total_stop_time_after_delay/60))
                self.total_stop_time_delay_hours_text.setText("{0:.2f}".format(total_stop_time_after_delay/3600))
                self.total_time_after_delay_seconds_text.setText("{0:.2f}".format(total_time_after_delay))
                self.total_time_after_delay_minutes_text.setText("{0:.2f}".format(total_time_after_delay/60))
                self.total_time_after_delay_hours_text.setText("{0:.2f}".format(total_time_after_delay/3600))

                self.statusbar.showMessage("Done")
                self.onActivated1(self.currSimText)
            except FileNotFoundError:
                self.statusbar.showMessage("Data not ready")

    def createSummary(self):
        groupbox = QGroupBox("Summary")
        vlayout = QVBoxLayout()
        groupbox.setLayout(vlayout)

        combo = QComboBox()
        combo.addItem("Linked Histogram")
        combo.addItem("Unlinked Donut Chart")
        combo.addItem("Summary Pie Chart")
        vlayout.addWidget(combo)

        entrance_events_layout = QHBoxLayout()
        vlayout.addLayout(entrance_events_layout)
        entrance_events_label = QLabel('\nEntrance events: ')
        self.entrance_events_text = QLabel('\n0')
        self.entrance_events_text.setAlignment(QtCore.Qt.AlignRight)
        entrance_events_layout.addWidget(entrance_events_label)
        entrance_events_layout.addWidget(self.entrance_events_text)

        entrance_misreads_layout = QHBoxLayout()
        vlayout.addLayout(entrance_misreads_layout)
        entrance_misreads_label = QLabel('Entrance misreads: ')
        self.entrance_misreads_text = QLabel('0')
        self.entrance_misreads_text.setAlignment(QtCore.Qt.AlignRight)
        entrance_misreads_layout.addWidget(entrance_misreads_label)
        entrance_misreads_layout.addWidget(self.entrance_misreads_text)

        found_previous_bag_layout = QHBoxLayout()
        vlayout.addLayout(found_previous_bag_layout)
        found_previous_bag_label = QLabel('Read last RFID (found previous bag): ')
        self.found_previous_bag_text = QLabel('0')
        self.found_previous_bag_text.setAlignment(QtCore.Qt.AlignRight)
        found_previous_bag_layout.addWidget(found_previous_bag_label)
        found_previous_bag_layout.addWidget(self.found_previous_bag_text)

        total_bins_layout = QHBoxLayout()
        vlayout.addLayout(total_bins_layout)
        total_bins_label = QLabel('Total Bins: ')
        self.total_bins_text = QLabel('0')
        self.total_bins_text.setAlignment(QtCore.Qt.AlignRight)
        total_bins_layout.addWidget(total_bins_label)
        total_bins_layout.addWidget(self.total_bins_text)

        atten_linked_layout = QHBoxLayout()
        vlayout.addLayout(atten_linked_layout)
        atten_linked_label = QLabel('Total Linked Bins: ')
        self.atten_linked_text = QLabel('0')
        self.atten_linked_text.setAlignment(QtCore.Qt.AlignRight)
        atten_linked_layout.addWidget(atten_linked_label)
        atten_linked_layout.addWidget(self.atten_linked_text)

        unlinked_layout = QHBoxLayout()
        vlayout.addLayout(unlinked_layout)
        unlinked_label = QLabel('Total Unlinked Bins: ')
        self.unlinked_text = QLabel('0')
        self.unlinked_text.setAlignment(QtCore.Qt.AlignRight)
        unlinked_layout.addWidget(unlinked_label)
        unlinked_layout.addWidget(self.unlinked_text)

        atten_events_layout = QHBoxLayout()
        vlayout.addLayout(atten_events_layout)
        atten_events_label = QLabel('Attenuation events: ')
        self.atten_events_text = QLabel('0')
        self.atten_events_text.setAlignment(QtCore.Qt.AlignRight)
        atten_events_layout.addWidget(atten_events_label)
        atten_events_layout.addWidget(self.atten_events_text)

        linked_internal_bag_layout = QHBoxLayout()
        vlayout.addLayout(linked_internal_bag_layout)
        linked_internal_bag_label = QLabel('Total Linked Internal Bags: ')
        self.linked_internal_bag_text = QLabel('0')
        self.linked_internal_bag_text.setAlignment(QtCore.Qt.AlignRight)
        linked_internal_bag_layout.addWidget(linked_internal_bag_label)
        linked_internal_bag_layout.addWidget(self.linked_internal_bag_text)

        unlinked_internal_bag_layout = QHBoxLayout()
        vlayout.addLayout(unlinked_internal_bag_layout)
        unlinked_internal_bag_label = QLabel('Total Unlinked Internal Bags: ')
        self.unlinked_internal_bag_text = QLabel('0')
        self.unlinked_internal_bag_text.setAlignment(QtCore.Qt.AlignRight)
        unlinked_internal_bag_layout.addWidget(unlinked_internal_bag_label)
        unlinked_internal_bag_layout.addWidget(self.unlinked_internal_bag_text)

        exit_events_layout = QHBoxLayout()
        vlayout.addLayout(exit_events_layout)
        exit_events_label = QLabel('Exit events: ')
        self.exit_events_text = QLabel('0')
        self.exit_events_text.setAlignment(QtCore.Qt.AlignRight)
        exit_events_layout.addWidget(exit_events_label)
        exit_events_layout.addWidget(self.exit_events_text)

        exit_misreads_layout = QHBoxLayout()
        vlayout.addLayout(exit_misreads_layout)
        exit_misreads_label = QLabel('Exit misreads: ')
        self.exit_misreads_text = QLabel('0')
        self.exit_misreads_text.setAlignment(QtCore.Qt.AlignRight)
        exit_misreads_layout.addWidget(exit_misreads_label)
        exit_misreads_layout.addWidget(self.exit_misreads_text)

        lost_track_crusty_bag_layout = QHBoxLayout()
        vlayout.addLayout(lost_track_crusty_bag_layout)
        lost_track_crusty_bag_label = QLabel('Lost Tracking Crusty Bags: ')
        self.lost_track_crusty_bag_text = QLabel('0')
        self.lost_track_crusty_bag_text.setAlignment(QtCore.Qt.AlignRight)
        lost_track_crusty_bag_layout.addWidget(lost_track_crusty_bag_label)
        lost_track_crusty_bag_layout.addWidget(self.lost_track_crusty_bag_text)

        already_sent_moveback_bag_layout = QHBoxLayout()
        vlayout.addLayout(already_sent_moveback_bag_layout)
        already_sent_moveback_bag_label = QLabel('Bag already sent to next zone: ')
        self.already_sent_moveback_bag_text = QLabel('0')
        self.already_sent_moveback_bag_text.setAlignment(QtCore.Qt.AlignRight)
        already_sent_moveback_bag_layout.addWidget(already_sent_moveback_bag_label)
        already_sent_moveback_bag_layout.addWidget(self.already_sent_moveback_bag_text)

        loose_bags_layout = QHBoxLayout()
        vlayout.addLayout(loose_bags_layout)
        loose_bags_label = QLabel('Loose Bags: \n(Exit misreads - Lost Track + Bag already sent)')
        self.loose_bags_text = QLabel('0')
        self.loose_bags_text.setAlignment(QtCore.Qt.AlignRight)
        loose_bags_layout.addWidget(loose_bags_label)
        loose_bags_layout.addWidget(self.loose_bags_text)

        exit_total_bins_layout = QHBoxLayout()
        vlayout.addLayout(exit_total_bins_layout)
        exit_total_bins_label = QLabel('Total Exit Bins: \n(Exit events - Loose bags)')
        self.exit_total_bins_text = QLabel('0')
        self.exit_total_bins_text.setAlignment(QtCore.Qt.AlignRight)
        exit_total_bins_layout.addWidget(exit_total_bins_label)
        exit_total_bins_layout.addWidget(self.exit_total_bins_text)

        cut_oversized_bags_layout = QHBoxLayout()
        vlayout.addLayout(cut_oversized_bags_layout)
        cut_oversized_bags_label = QLabel('Cut/Overesized Bags: ')
        self.cut_oversized_bags_text = QLabel('0')
        self.cut_oversized_bags_text.setAlignment(QtCore.Qt.AlignRight)
        cut_oversized_bags_layout.addWidget(cut_oversized_bags_label)
        cut_oversized_bags_layout.addWidget(self.cut_oversized_bags_text)

        divider_label = QLabel("\n-----------------------------------------------------------\n")
        vlayout.addWidget(divider_label)

        unlinked_bin_percentage_layout = QHBoxLayout()
        vlayout.addLayout(unlinked_bin_percentage_layout)
        unlinked_bin_percentage_label = QLabel('Percent of Unlinked Bins: ')
        self.unlinked_bin_percentage_text = QLabel('0 %')
        self.unlinked_bin_percentage_text.setAlignment(QtCore.Qt.AlignRight)
        unlinked_bin_percentage_layout.addWidget(unlinked_bin_percentage_label)
        unlinked_bin_percentage_layout.addWidget(self.unlinked_bin_percentage_text)

        unlinked_internal_bag_percentage_layout = QHBoxLayout()
        vlayout.addLayout(unlinked_internal_bag_percentage_layout)
        unlinked_internal_bag_percentage_label = QLabel('Percent of Unlinked Internal Bags: ')
        self.unlinked_internal_bag_percentage_text = QLabel('0 %')
        self.unlinked_internal_bag_percentage_text.setAlignment(QtCore.Qt.AlignRight)
        unlinked_internal_bag_percentage_layout.addWidget(unlinked_internal_bag_percentage_label)
        unlinked_internal_bag_percentage_layout.addWidget(self.unlinked_internal_bag_percentage_text)

        self.currText = "Linked Histogram"
        combo.activated[str].connect(self.onActivated)
        return groupbox

    def setSummaryLabel(self):
        try:           
            total_bins = self.total_bins
            scanner_linked_RFID = self.scanner_linked_RFID
            unlinked_bins = total_bins - scanner_linked_RFID
            percentage_unlinked_bin = unlinked_bins / total_bins * 100           

            total = len(self.dfinal.index)      # total number of scanned bags
            linked = len(self.linked.index)     # total number of linked bags
            unlinked = total - linked           # total number of unlinked bags
            percentage_unlinked_bags = (unlinked/(total)) * 100       # percentage for unlinked bags

            loose_bags = self.exit_misreads - self.lost_track_crusty_bag + self.already_sent_moveback_bag
            cut_oversized = len(self.cut_oversized.index)

            self.entrance_events_text.setText('\n'+str(self.entrance_events))
            self.entrance_misreads_text.setText(str(self.entrance_misreads))
            self.found_previous_bag_text.setText(str(self.found_prev_bag))
            self.total_bins_text.setText(str(total_bins))
            self.atten_events_text.setText(str(total))
            self.atten_linked_text.setText(str(scanner_linked_RFID))
            self.unlinked_text.setText(str(unlinked_bins))
            self.linked_internal_bag_text.setText(str(linked))
            self.unlinked_internal_bag_text.setText(str(unlinked))
            self.exit_events_text.setText(str(self.exit_events))
            self.exit_misreads_text.setText(str(self.exit_misreads))
            self.lost_track_crusty_bag_text.setText(str(self.lost_track_crusty_bag))
            self.already_sent_moveback_bag_text.setText(str(self.already_sent_moveback_bag))
            self.loose_bags_text.setText(str(loose_bags))
            self.cut_oversized_bags_text.setText(str(cut_oversized))
            self.exit_total_bins_text.setText(str(self.exit_events-loose_bags))
            self.unlinked_bin_percentage_text.setText('{0:.2f} %'.format(percentage_unlinked_bin))
            self.unlinked_internal_bag_percentage_text.setText('{0:.2f} %'.format(percentage_unlinked_bags))

        except (AttributeError, ZeroDivisionError):
            self.statusbar.showMessage("Data not processed")

    def onActivated(self, text):
        self.currText = text
        if text == 'Linked Histogram':
            self.grid.addWidget(self.createBar(), 0, 1)
        elif text == 'Unlinked Donut Chart':
            self.grid.addWidget(self.createUnlinkedBar(), 0, 1)
        else:
            self.grid.addWidget(self.createSummaryBar(), 0, 1)

    def createUnlinkedSummary(self):
        groupbox = QGroupBox("Unlinked Details")
        hlayout = QVBoxLayout()
        groupbox.setLayout(hlayout)

        exit_read_unlinked_layout = QHBoxLayout()
        hlayout.addLayout(exit_read_unlinked_layout)
        exit_read_unlinked_label = QLabel('Unlinked Bin Read at Exit: ')
        self.exit_read_unlinked_text = QLabel('0')
        self.exit_read_unlinked_text.setAlignment(QtCore.Qt.AlignRight)
        exit_read_unlinked_layout.addWidget(exit_read_unlinked_label)
        exit_read_unlinked_layout.addWidget(self.exit_read_unlinked_text)

        unlinked_lost_track_layout = QHBoxLayout()
        hlayout.addLayout(unlinked_lost_track_layout)
        unlinked_lost_track_label = QLabel("Unlinked Bin Lost Track before Exit: ")
        self.unlinked_lost_track_text = QLabel('0')
        self.unlinked_lost_track_text.setAlignment(QtCore.Qt.AlignRight)
        unlinked_lost_track_layout.addWidget(unlinked_lost_track_label)
        unlinked_lost_track_layout.addWidget(self.unlinked_lost_track_text)

        total_unlinked_layout = QHBoxLayout()
        hlayout.addLayout(total_unlinked_layout)
        total_unlinked_label = QLabel('Total Unlinked: ')
        self.total_unlinked_text = QLabel('0')
        self.total_unlinked_text.setAlignment(QtCore.Qt.AlignRight)
        total_unlinked_layout.addWidget(total_unlinked_label)
        total_unlinked_layout.addWidget(self.total_unlinked_text)

        upper_count_layout = QHBoxLayout()
        hlayout.addLayout(upper_count_layout)
        upper_count_label = QLabel('Over the Upper Limit: ')
        self.upper_count_text = QLabel('0')
        self.upper_count_text.setAlignment(QtCore.Qt.AlignRight)
        upper_count_layout.addWidget(upper_count_label)
        upper_count_layout.addWidget(self.upper_count_text)

        lower_count_layout = QHBoxLayout()
        hlayout.addLayout(lower_count_layout)
        lower_count_label = QLabel('Below the Lower Limit: ')
        self.lower_count_text = QLabel('0')
        self.lower_count_text.setAlignment(QtCore.Qt.AlignRight)
        lower_count_layout.addWidget(lower_count_label)
        lower_count_layout.addWidget(self.lower_count_text)

        not_scanned_unlinked_layout = QHBoxLayout()
        hlayout.addLayout(not_scanned_unlinked_layout)
        not_scanned_unlinked_label = QLabel('Not Scanned: ')
        self.not_scanned_unlinked_text = QLabel('0')
        self.not_scanned_unlinked_text.setAlignment(QtCore.Qt.AlignRight)
        not_scanned_unlinked_layout.addWidget(not_scanned_unlinked_label)
        not_scanned_unlinked_layout.addWidget(self.not_scanned_unlinked_text)

        slipping_layout = QHBoxLayout()
        hlayout.addLayout(slipping_layout)
        slipping_label = QLabel('Slipping Bins: ')
        self.slipping_text = QLabel('0')
        slipping_layout.addWidget(slipping_label)
        slipping_layout.addWidget(self.slipping_text)

        spacerItem = QtWidgets.QSpacerItem(10, 10, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        slipping_layout.addItem(spacerItem)

        slipping_percentage_label = QLabel('Percentage: ')
        self.slipping_percentage_text = QLabel('0 %')
        slipping_layout.addWidget(slipping_percentage_label)
        slipping_layout.addWidget(self.slipping_percentage_text)

        pushed_layout = QHBoxLayout()
        hlayout.addLayout(pushed_layout)
        pushed_label = QLabel('Pushed Bins: ')
        self.pushed_text = QLabel('0')
        pushed_layout.addWidget(pushed_label)
        pushed_layout.addWidget(self.pushed_text)

        spacerItem = QtWidgets.QSpacerItem(10, 10, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        pushed_layout.addItem(spacerItem)

        pushed_percentage_label = QLabel('Percentage: ')
        self.pushed_percentage_text = QLabel('0 %')
        pushed_layout.addWidget(pushed_percentage_label)
        pushed_layout.addWidget(self.pushed_percentage_text)

        return groupbox

    def setUnlinkedLabel(self):
        try:
            total_bins = self.total_bins
            upper_counts = len(self.upper_counts.index)
            lower_counts = len(self.lower_counts.index)

            not_scanned_unlinked = len(self.not_scanned_unlinked)
            slipping = len(self.slipping.index)
            pushed = len(self.pushed.index)

            scanner_linked_RFID = self.scanner_linked_RFID
            unlinked_bins = total_bins - scanner_linked_RFID

            exit_read_unlinked = self.exit_read_unlinked

            self.total_unlinked_text.setText(str(unlinked_bins))
            self.upper_count_text.setText(str(upper_counts))
            self.lower_count_text.setText(str(lower_counts))
            self.not_scanned_unlinked_text.setText(str(not_scanned_unlinked))
            self.slipping_text.setText(str(slipping))
            self.pushed_text.setText(str(pushed))

            if unlinked_bins == 0:
                self.slipping_percentage_text.setText('0')
                self.pushed_percentage_text.setText('0')      
            else:
                self.slipping_percentage_text.setText('{0:.2f} %'.format(slipping/unlinked_bins*100))
                self.pushed_percentage_text.setText('{0:.2f} %'.format(pushed/unlinked_bins*100))

            self.exit_read_unlinked_text.setText('{0}'.format(exit_read_unlinked))
            self.unlinked_lost_track_text.setText('{0}'.format(unlinked_bins - exit_read_unlinked))

        except AttributeError:
            self.statusbar.showMessage("Data not processed")        # not shown due to covered by top message

    def createFileList(self):
        groupbox = QGroupBox("File List")
        vlayout = QVBoxLayout()
        groupbox.setLayout(vlayout)

        self.file_list_text_edit = QTextEdit()
        vlayout.addWidget(self.file_list_text_edit)

        return groupbox

    def setFileLists(self, files):
        for file in files:
            self.file_list_text_edit.append(file)

    def createBar(self):
        min_num, max_num = 0, 100
        linked_bag_list = []
        try:
            df = self.linked['Beam Diff'].dropna()
            linked_bag_list = df.values.tolist()
            min_num = min(linked_bag_list)
            if min_num > 0:                 # check if greater than 0, set to 0
                min_num = 0
            max_num = int(max(linked_bag_list))

        except (AttributeError, ValueError):
            self.statusbar.showMessage('Data not ready')

        count = [0] * (max_num + 1)        # choose the largest num as length of count
        
        for num in linked_bag_list:
            count[int(num)] += 1            # update every number's count

        max_count = max(count)

        setBar = QBarSet('Beam Difference Occurrence')
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

        chart.setTitle('Linked Bins Histogram')
        chart.addSeries(series)
        chart.setAnimationOptions(QChart.SeriesAnimations)

        axisX = QValueAxis()
        axisX.setTitleText("Attenuation Window")
        axisX.setRange(min_num, max_num+20)
        chart.setAxisX(axisX, series)

        axisY = QValueAxis()
        axisY.setTitleText("Frequency")
        axisY.setRange(0, max_count+20)
        chart.setAxisY(axisY, series)

        chart.legend().hide()

        chartView = QChartView(chart)
        chartView.setRenderHint(QPainter.Antialiasing)

        return chartView


    def createUnlinkedBar(self):
        series = QPieSeries()
        series1 = QPieSeries()

        try:
            upper_bin = len(self.upper_counts.index)
            lower_bin = len(self.lower_counts.index)
            not_scanned_bin = len(self.not_scanned_unlinked)
            slipping_bin = len(self.slipping.index)
            other_than_slipping_bin = upper_bin - slipping_bin
            pushed_bin = len(self.pushed.index)
            other_than_pushed_bin = lower_bin - pushed_bin

            # Inner Donut
            series.setPieSize(0.65)
            series.setHoleSize(0.25)
            series.append("Slipping", slipping_bin)
            series.append("Others", other_than_slipping_bin)
            series.append("Pushed", pushed_bin)
            series.append("Others", other_than_pushed_bin)
            series.append("Not Scanned", not_scanned_bin)

            slices = series.slices()[0]
            slices.setBrush(QBrush(QColor(0xB9DB8A)))
            slices.setLabelVisible()
            slices.setLabelPosition(QPieSlice.LabelInsideNormal)

            slices1 = series.slices()[1]
            slices1.setBrush(QBrush(QColor(0xDCEDC4)))
            slices1.setLabelVisible()
            slices1.setLabelPosition(QPieSlice.LabelInsideNormal)

            slices2 = series.slices()[2]
            slices2.setBrush(QBrush(QColor(0x63BCE9)))
            slices2.setLabelVisible()
            slices2.setLabelPosition(QPieSlice.LabelInsideNormal)

            slices3 = series.slices()[3]
            slices3.setBrush(QBrush(QColor(0xA6D9F2)))
            slices3.setLabelVisible()
            slices3.setLabelPosition(QPieSlice.LabelInsideNormal)

            slices4 = series.slices()[4]
            slices4.setBrush(QBrush(QColor(0xF9C36C)))
            slices4.setLabelVisible()
            slices4.setLabelPosition(QPieSlice.LabelInsideNormal)

            # Outter Donut
            series1.setPieSize(0.8)
            series1.setHoleSize(0.65)
            series1.append("Over Limit", upper_bin)
            series1.append("Below Limit", lower_bin)
            series1.append("Not Scanned", not_scanned_bin)

            slices11 = series1.slices()[0]
            slices11.setBrush(QBrush(QColor(0x99CA53)))
            if upper_bin != 0:
                slices11.setLabelVisible()
            slices11.setLabelPosition(QPieSlice.LabelOutside)

            slices22 = series1.slices()[1]
            slices22.setBrush(QBrush(QColor(0x209FDF)))
            if lower_bin != 0:
                slices22.setLabelVisible()
            slices22.setLabelPosition(QPieSlice.LabelOutside)

            slices33 = series1.slices()[2]
            slices33.setBrush(QBrush(QColor(0xF6A625)))
            if not_scanned_bin != 0:
                slices33.setLabelVisible()
            slices33.setLabelPosition(QPieSlice.LabelOutside)

        except AttributeError:
            self.statusbar.showMessage('Data not ready')

        chart = QChart()
        chart.legend().hide()
        font = QFont()
        font.setPixelSize(16)

        chart.setTitleFont(font)
        chart.setTitle("Unlinked Details")        
        chart.addSeries(series)
        chart.addSeries(series1)
        chart.setAnimationOptions(QChart.SeriesAnimations)

        chartView = QChartView(chart)
        chartView.setRenderHint(QPainter.Antialiasing)

        return chartView

    def createSummaryBar(self):
        series = QPieSeries()
        labelfont = QFont()
        labelfont.setPixelSize(11)
        linked_bag, unlinked_bag = 0, 0
        try:
            linked_bag = self.scanner_linked_RFID
            unlinked_bag = self.total_bins - linked_bag
          
        except AttributeError:
            self.statusbar.showMessage('Data not ready')

        series.append("Linked", linked_bag)
        series.append("Unlinked", unlinked_bag)

        slices = series.slices()[0]
        slices.setBrush(QBrush(QColor(0x57B1FD)))
        slices.setLabelVisible()
        slices.setLabel(("{0} {1:.2f}%").format("Linked", 100*slices.percentage()))
        slices.setLabelFont(labelfont)

        slices1 = series.slices()[1]
        slices1.setExploded()
        slices1.setLabelVisible()
        slices1.setPen(QPen(QColor(0x57B1FD), 2))
        slices1.setBrush(QBrush(QColor(0xfdb157)))
        slices1.setLabel(("{0} {1:.2f}%").format("Unlinked", 100*slices1.percentage()))
        slices1.setLabelFont(labelfont)             

        chart = QChart()
        font = QFont()
        font.setPixelSize(16)
        
        chart.setTitleFont(font)

        chart.addSeries(series)
        chart.setAnimationOptions(QChart.SeriesAnimations)
        chart.setTitle("Total")
        chart.legend().hide()

        chartView = QChartView(chart)
        chartView.setRenderHint(QPainter.Antialiasing)

        return chartView

    # MainMenu Components
    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Bin Tracking App"))
        self.menu_File.setTitle(_translate("MainWindow", "&File"))
        self.action_Exit.setText(_translate("MainWindow", "&Exit"))
        self.actionOpenFile.setText(_translate("MainWindow", "&Open File/Files"))
        self.actionOpenDir.setText(_translate("MainWindow", "&Open Folder"))

    class progressBar(QWidget):

        def __init__(self):
            super().__init__()
            self.initUI()

        def initUI(self):
            self.resize(350, 100)
            vlayout = QVBoxLayout(self)
            self.pbar = QProgressBar(self)
            self.step = 0

            vlayout.addWidget(self.pbar)
            self.setLayout(vlayout)

            self.setWindowTitle('Loading...')
            self.show()

        def exit(self):
            self.close()

    def run_file(self, file_list):
        start_time = timeit.default_timer()
        self.loading_dialog = self.progressBar()
        pp = PreProc(file_list, self)  # pass files into PreProc class
        self.loading_dialog.exit()
        elapsed = timeit.default_timer() - start_time
        print("time cost on processing data:", elapsed)
        start_time1 = timeit.default_timer()
        dp = DataProc(pp)  # pass the prepared data into DataProc class
        elapsed1 = timeit.default_timer() - start_time1
        print("time cost on load data:", elapsed1)
        self.linked = dp.linked
        self.unlinked = dp.unlinked_RFID
        self.dfinal = dp.dfinal
        self.cut_oversized = dp.cut_oversized
        if self.type == '2':
            self.upper_counts = self.unlinked[self.unlinked['Beam Diff'] > cfg.type2['linked'][1]]
            self.lower_counts = self.unlinked[self.unlinked['Beam Diff'] < cfg.type2['linked'][0]]
            self.slipping = dp.get_df(self.upper_counts, cfg.type2['slipping'][0], cfg.type2['slipping'][1])
            self.pushed = dp.get_df(self.lower_counts, cfg.type2['pushed'][0], cfg.type2['pushed'][1])
        elif self.type == '5':
            self.upper_counts = self.unlinked[self.unlinked['Beam Diff'] > cfg.type5['linked'][1]]
            self.lower_counts = self.unlinked[self.unlinked['Beam Diff'] < cfg.type5['linked'][0]]
            self.slipping = dp.get_df(self.unlinked, cfg.type5['slipping'][0], cfg.type5['slipping'][1])
            self.pushed = dp.get_df(self.unlinked, cfg.type5['pushed'][0], cfg.type5['pushed'][1])
        self.not_scanned_unlinked = dp.unlinked_list
        self.entrance_events = pp.entrance_events
        self.entrance_misreads = pp.misread_entrance
        self.found_prev_bag = pp.found_prev_bag
        self.total_bins = pp.total_bins
        self.scanner_linked_RFID = pp.scanner_linked_RFID
        self.already_sent_moveback_bag = pp.bag_already_sent
        self.lost_track_crusty_bag = pp.lost_track_crusty_bag
        self.exit_events = pp.exit_events
        self.exit_misreads = pp.misread_exit
        self.exit_read_unlinked = pp.exit_read_unlinked
        self.statusbar.showMessage('Done')
        self.setSummaryLabel()
        self.setUnlinkedLabel()
        self.setFileLists(file_list)
        self.onActivated(self.currText)  # to display chart corresponding to dropdown selections


    # Open file dialog
    def openFile(self):
        file_list, _ = QtWidgets.QFileDialog.getOpenFileNames(None,"QFileDialog.getOpenFileNames()", "","All Files (*);;Log Files (*.log);;")
        self.type = None
        illegal = False
        file_pattern = cfg.files['pattern']
        suf = 'log'
        if len(file_list) != 0:
            for f in file_list:  # check all selected files are legal
                prefix = f[f.rfind('/')+1:f.find('.')]
                suffix = f[f.rfind('.')+1:]
                if self.type and self.type != prefix[prefix.find('Type')+4:prefix.rfind('_')]:
                    illegal = True
                self.type = prefix[prefix.find('Type')+4:prefix.rfind('_')]
                if suffix != suf and file_pattern not in prefix:
                    illegal = True
            if illegal:
                self.showdialog(illegal, True)
            else:
                self.run_file(file_list)

    # Open directory dialog
    def openDir(self):
        dialog = QtWidgets.QFileDialog()
        dialog.setFileMode(QFileDialog.DirectoryOnly)
        dic_file = []
        if dialog.exec_():
            dic_file = dialog.selectedFiles()

        file_list = []
        has_log = False
        self.type = None
        illegal = False
        file_pattern = cfg.files['pattern']
        suf = 'log'
        if dic_file:
            for f in os.listdir(dic_file[0]):
                prefix = f[f.rfind('/')+1:f.find('.')]
                suffix = f[f.rfind('.')+1:]
                if self.type and self.type != prefix[prefix.find('Type') + 4:prefix.rfind('_')]:
                    illegal = True
                self.type = prefix[prefix.find('Type') + 4:prefix.rfind('_')]
                if suffix == suf:
                    has_log = True
                    if file_pattern in prefix:  # if match AnalogicStandaloneType*.log, append to log_file
                        file_list += dic_file[0]+"/"+f,
            if not has_log:
                self.showdialog(False, has_log)
            elif illegal:
                self.showdialog(illegal, has_log)

            if len(file_list) == 0 and has_log:
                self.showdialog(illegal, False)
            if len(file_list) != 0 and not illegal:
                self.run_file(file_list)


    # Pop up warning window
    def showdialog(self, illegal_file, has_log):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.resize(200, 100)
        if not has_log:
            msg.setText("No log files found.")
        if illegal_file:
            msg.setText("Invalid log files detected.")

        msg.setWindowTitle("Something's wrong")
        msg.setStandardButtons(QMessageBox.Ok)

        x = msg.exec_()

    def exit(self):
        sys.exit(app.exec_())


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow, app)
    MainWindow.show()
    sys.exit(app.exec_())
