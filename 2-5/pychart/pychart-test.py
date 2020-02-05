import sys, random
from PyQt5.QtWidgets import (QApplication, QMainWindow)
from PyQt5.QtChart import QChart, QChartView, QValueAxis, QBarCategoryAxis, QBarSet, QBarSeries
from PyQt5.Qt import Qt
from PyQt5.QtGui import QPainter

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.resize(800, 600)

        set0 = QBarSet('X0')
        set1 = QBarSet('X1')
        set2 = QBarSet('X2')
        set3 = QBarSet('X3')
        set4 = QBarSet('X4')

        set0.append([random.randint(0, 10) for i in range(6)])
        set1.append([random.randint(0, 10) for i in range(6)])
        set2.append([random.randint(0, 10) for i in range(6)])
        set3.append([random.randint(0, 10) for i in range(6)])
        set4.append([random.randint(0, 10) for i in range(6)])

        series = QBarSeries()
        series.append(set0)
        series.append(set1)
        series.append(set2)
        series.append(set3)
        series.append(set4)

        chart = QChart()
        chart.addSeries(series)
        chart.setTitle('Bar Chart Demo')
        chart.setAnimationOptions(QChart.SeriesAnimations)

        months = ('Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun')

        axisX = QBarCategoryAxis()
        axisX.append(months)

        axisY = QValueAxis()
        axisY.setRange(0, 15)

        chart.addAxis(axisX, Qt.AlignBottom)
        chart.addAxis(axisY, Qt.AlignLeft)

        chart.legend().setVisible(True)
        chart.legend().setAlignment(Qt.AlignBottom)

        chartView = QChartView(chart)
        self.setCentralWidget(chartView)

if __name__ == '__main__':
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec_())