import unittest
from mainMenu import Ui_MainWindow
from PyQt5 import QtWidgets
import sys

class MainMenuTest(unittest.TestCase):
    def test_defaults(self):
        app = QtWidgets.QApplication(sys.argv)
        MainWindow = QtWidgets.QMainWindow()
        ui = Ui_MainWindow()
        ui.setupUi(MainWindow,app)

        self.assertEqual(ui.total_bins_text.text(), "0")
        self.assertEqual(ui.atten_events_text.text(), "0")

if __name__ == '__main__':
    unittest.main(verbosity=2)
