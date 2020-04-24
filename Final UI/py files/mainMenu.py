import sys
import os
from PyQt5 import QtCore,  QtWidgets
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QGridLayout, QComboBox, QLabel, QFileDialog, QGroupBox, QMessageBox, QTextEdit
from PyQt5.QtGui import QBrush, QPen, QColor, QFont, QPainter
from PyQt5.QtChart import QChart, QChartView, QValueAxis, QBarSet, QBarSeries, QPieSeries
from preProc import PreProc
from dataProc import DataProc
import timeit


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1000, 680)
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

        self.grid = QGridLayout()
        self.centralwidget.setLayout(self.grid)
        self.grid.addWidget(self.createSummary(), 0, 0)
        self.grid.addWidget(self.createBar(), 0, 1)

        self.grid.addWidget(self.createUnlinkedSummary(), 1, 0)
        self.grid.addWidget(self.createFileList(), 1, 1)
        self.grid.setColumnStretch(0, 1)
        self.grid.setColumnStretch(1, 3)
        self.grid.setRowStretch(0, 3)
        self.grid.setRowStretch(1, 1)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        
        self.actionOpenFile.triggered.connect(self.openFile)
        self.actionOpenDir.triggered.connect(self.openDir)
        self.action_Exit.triggered.connect(self.exit)


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

        unlinked_bin_percentage_layout = QHBoxLayout()
        vlayout.addLayout(unlinked_bin_percentage_layout)
        unlinked_bin_percentage_label = QLabel('\n-----------------------------------------\n\nPercent of Unlinked Bins: ')
        self.unlinked_bin_percentage_text = QLabel('\n\n\n0 %')
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
            scanner_linked_rfid = self.scanner_linked_rfid
            unlinked_bins = total_bins - scanner_linked_rfid
            percentage_unlinked_bin = unlinked_bins / total_bins * 100           

            total = len(self.dfinal.index)      # total number of scanned bags
            linked = len(self.linked.index)     # total number of linked bags
            unlinked = total - linked          # total number of unlinked bags
            percentage_unlinked_bags = (unlinked/(total)) * 100       # percentage for unlinked bags

            loose_bags = self.exit_misreads - self.lost_track_crusty_bag + self.already_sent_moveback_bag

            # print(self.dfinal.loc[self.dfinal['Machine Decision'] == 'ALARM'])
            self.entrance_events_text.setText('\n'+(str(self.entrance_events)))
            self.entrance_misreads_text.setText(str(self.entrance_misreads))
            self.found_previous_bag_text.setText(str(self.found_prev_bag))
            self.total_bins_text.setText(str(total_bins))
            self.atten_events_text.setText(str(total))
            self.atten_linked_text.setText(str(scanner_linked_rfid))
            self.unlinked_text.setText(str(unlinked_bins))
            self.linked_internal_bag_text.setText(str(linked))
            self.unlinked_internal_bag_text.setText(str(unlinked))
            self.exit_events_text.setText(str(self.exit_events))
            self.exit_misreads_text.setText(str(self.exit_misreads))
            self.lost_track_crusty_bag_text.setText(str(self.lost_track_crusty_bag))
            self.already_sent_moveback_bag_text.setText(str(self.already_sent_moveback_bag))
            self.loose_bags_text.setText(str(loose_bags))
            self.exit_total_bins_text.setText(str(self.exit_events-loose_bags))
            self.unlinked_bin_percentage_text.setText('\n\n\n{0:.2f} %'.format(percentage_unlinked_bin))
            self.unlinked_internal_bag_percentage_text.setText('{0:.2f} %'.format(percentage_unlinked_bags))

        except (AttributeError, ZeroDivisionError):
            self.statusbar.showMessage("Data not processed")        # not shown due to covered by top message

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
        
        slipping_layout = QHBoxLayout()
        hlayout.addLayout(slipping_layout)
        slipping_label = QLabel('Slipping Bins: ')
        self.slipping_text = QLabel('0')
        slipping_layout.addWidget(slipping_label)
        slipping_layout.addWidget(self.slipping_text)

        slipping_percentage_label = QLabel('Percentage: ')
        self.slipping_percentage_text = QLabel('0 %')
        slipping_layout.addWidget(slipping_percentage_label)
        slipping_layout.addWidget(self.slipping_percentage_text)
        spacerItem = QtWidgets.QSpacerItem(10, 10, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        slipping_layout.addItem(spacerItem)

        pushed_layout = QHBoxLayout()
        hlayout.addLayout(pushed_layout)
        pushed_label = QLabel('Pushed Bins: ')
        self.pushed_text = QLabel('0')
        pushed_layout.addWidget(pushed_label)
        pushed_layout.addWidget(self.pushed_text)

        pushed_percentage_label = QLabel('Percentage: ')
        self.pushed_percentage_text = QLabel('0 %')
        pushed_layout.addWidget(pushed_percentage_label)
        pushed_layout.addWidget(self.pushed_percentage_text)
        spacerItem = QtWidgets.QSpacerItem(10, 10, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        pushed_layout.addItem(spacerItem)

        exit_read_unlinked_layout = QHBoxLayout()
        hlayout.addLayout(exit_read_unlinked_layout)
        exit_read_unlinked_label = QLabel('Unlinked Bin Read at Exit: ')
        self.exit_read_unlinked_text = QLabel('0')
        exit_read_unlinked_layout.addWidget(exit_read_unlinked_label)
        exit_read_unlinked_layout.addWidget(self.exit_read_unlinked_text)
        spacerItem = QtWidgets.QSpacerItem(10, 10, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        exit_read_unlinked_layout.addItem(spacerItem)

        unlinked_lost_track_layout = QHBoxLayout()
        hlayout.addLayout(unlinked_lost_track_layout)
        unlinked_lost_track_label = QLabel("Unlinked Bin Lost Track before Exit: ")
        self.unlinked_lost_track_text = QLabel('0')
        unlinked_lost_track_layout.addWidget(unlinked_lost_track_label)
        unlinked_lost_track_layout.addWidget(self.unlinked_lost_track_text)
        spacerItem = QtWidgets.QSpacerItem(10, 10, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        unlinked_lost_track_layout.addItem(spacerItem)        

        return groupbox

    def setUnlinkedLabel(self):
        try:
            total_bins = self.total_bins  

            co_count = len(self.cut_oversized.index)   # cut or oversized bags.
            slipping = len(self.slipping.index)
            pushed = len(self.pushed.index)

            scanner_linked_rfid = self.scanner_linked_rfid
            unlinked_bins = total_bins - scanner_linked_rfid

            exit_read_unlinked = self.exit_read_unlinked

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
            min_num = int(min(linked_bag_list))
            if min_num > 0:                 # check if greater than 0, set to 0
                min_num = 0
            max_num = int(max(linked_bag_list))

        except AttributeError:
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
        chart.setTheme(QChart.ChartThemeBlueIcy)
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
        pushed_bin = 0
        slipping_bin = 0
        others = 0
        try:
            total_bins = self.total_bins
            scanner_linked_rfid = self.scanner_linked_rfid
            unlinked_bins = total_bins - scanner_linked_rfid
            slipping_bin = len(self.slipping.index)
            pushed_bin = len(self.pushed.index)
            others = unlinked_bins-pushed_bin-slipping_bin

        except AttributeError:
            self.statusbar.showMessage('Data not ready')

        series = QPieSeries()
        series.setHoleSize(0.35)
        series.append("Pushed", pushed_bin)
        series.append("Slipping", slipping_bin)
        series.append("Others", others)
        slices = series.slices()[0]
        slices.setLabelVisible()
        slices.setLabel("{0} {1:.2f}".format("Pushed", 100*slices.percentage()))

        slices1 = series.slices()[1]
        slices1.setLabelVisible()
        slices1.setLabel("{0} {1:.2f}".format("Slipping", 100*slices1.percentage()))

        # set exploded slice
        if pushed_bin > slipping_bin:
            slices.setExploded()
        else:
            slices1.setExploded()

        slices2 = series.slices()[2]
        slices2.setLabelVisible()
        slices2.setLabel("{0} {1:.2f}".format("Others", 100*slices2.percentage()))

        chart = QChart()
        chart.setTheme(QChart.ChartThemeBlueCerulean)
        chart.legend().hide()
        font = QFont()
        font.setPixelSize(16)

        chart.setTitleFont(font)
        chart.setTitle("Unlinked Details")        
        chart.addSeries(series)
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
            linked_bag = self.scanner_linked_rfid
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
        chart.setTheme(QChart.ChartThemeHighContrast)
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


    # mainMenu components
    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.menu_File.setTitle(_translate("MainWindow", "&File"))
        self.action_Exit.setText(_translate("MainWindow", "&Exit"))
        self.actionOpenFile.setText(_translate("MainWindow", "&Open File/Files"))
        self.actionOpenDir.setText(_translate("MainWindow", "&Open Folder"))

                   

    # open file dialog
    def openFile(self):
        filenames, _ = QtWidgets.QFileDialog.getOpenFileNames(None,"QFileDialog.getOpenFileNames()", "","All Files (*);;Log Files (*.log);;")

        illegal = False
        suf = 'log' # test for single .txt first, need to modify for final version
        if len(filenames) != 0:
            for f in filenames: # check all files are illegal in here
                suffix = f[f.rfind('.')+1:]
                if suffix != suf:
                    illegal = True
            if illegal:
                self.showdialog(illegal, True);
            else:
                start_time = timeit.default_timer()
                pp = PreProc(filenames)     # pass files into PreProc class
                elapsed = timeit.default_timer() - start_time
                print("time cost on processing data:", elapsed)
                start_time1 = timeit.default_timer()
                dp = DataProc()     # pass the prepared data into DataProc class
                elapsed1 = timeit.default_timer() - start_time1
                print("time cost on load data:", elapsed1)
                self.linked = dp.linked
                self.unlinked = dp.unlinked
                self.dfinal = dp.dfinal
                self.cut_oversized = dp.cut_oversized
                self.slipping = dp.slipping
                self.pushed = dp.pushed
                self.entrance_events = pp.entrance_events
                self.entrance_misreads = pp.misread_entrance
                self.found_prev_bag = pp.found_prev_bag
                self.total_bins = pp.total_bins
                self.scanner_linked_rfid = pp.scanner_linked_rfid   
                self.already_sent_moveback_bag = pp.bag_already_sent
                self.lost_track_crusty_bag = pp.lost_track_crusty_bag
                self.exit_events = pp.exit_events
                self.exit_misreads = pp.misread_exit  
                self.exit_read_unlinked = pp.exit_read_unlinked
                self.statusbar.showMessage('Done')
                self.setSummaryLabel()
                self.setUnlinkedLabel()
                self.setFileLists(filenames)
                self.onActivated(self.currText)         # to display chart corresponding to dropdown selections



    # open directory dialog
    def openDir(self):
        dialog = QtWidgets.QFileDialog()
        dialog.setFileMode(QFileDialog.DirectoryOnly)

        dic_file = []
        if dialog.exec_(): # == QtGui.QDialog.Accepted:
            dic_file = dialog.selectedFiles()

        log_file = []
        has_log = False
        suf = 'log'
        if dic_file:
            for f in os.listdir(dic_file[0]):
                suffix = f[f.rfind('.')+1:]
                name = f[:f.rfind('.')]
                if suffix == suf:
                    has_log = True
                    if "AnalogicStandaloneType" in name:# if match AnalogicStandaloneType*.log, append to log_file
                        log_file += dic_file[0]+"/"+f,
            if not has_log:            
                self.showdialog(False, has_log)
            if len(log_file) == 0 and has_log:
                self.showdialog(False, False)
            if len(log_file) != 0:
                start_time = timeit.default_timer()
                pp = PreProc(log_file)     # pass files into PreProc class
                elapsed = timeit.default_timer() - start_time
                print("time cost on processing data:", elapsed)
                start_time1 = timeit.default_timer()
                dp = DataProc()     # pass the prepared data into DataProc class
                elapsed1 = timeit.default_timer() - start_time1
                print("time cost on load data:", elapsed1)
                self.linked = dp.linked
                self.unlinked = dp.unlinked
                self.dfinal = dp.dfinal
                self.cut_oversized = dp.cut_oversized
                self.slipping = dp.slipping
                self.pushed = dp.pushed
                self.entrance_events = pp.entrance_events
                self.entrance_misreads = pp.misread_entrance
                self.found_prev_bag = pp.found_prev_bag
                self.total_bins = pp.total_bins
                self.scanner_linked_rfid = pp.scanner_linked_rfid
                self.already_sent_moveback_bag = pp.bag_already_sent
                self.lost_track_crusty_bag = pp.lost_track_crusty_bag
                self.exit_events = pp.exit_events
                self.exit_misreads = pp.misread_exit 
                self.exit_read_unlinked = pp.exit_read_unlinked
                self.statusbar.showMessage('Done')
                self.setSummaryLabel()
                self.setUnlinkedLabel()
                self.setFileLists(log_file)
                self.onActivated(self.currText)         # to display chart corresponding to dropdown selections


    # pop up warning window
    def showdialog(self, illegal_file, has_log):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        if not has_log:
            msg.setText("No log files found.")
        if illegal_file:
            msg.setText("Invalid log files detected.")

        msg.setWindowTitle("Something's wrong")
        msg.setStandardButtons(QMessageBox.Ok)

    def exit(self):
        sys.exit(app.exec_())

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
