import sys
from PyQt6.QtWidgets import QApplication, QMainWindow
from PyQt6.QtCore import QLocale
from ui_design import Ui_MainWindow


class MyPlanner(QMainWindow):
    def __init__(self):
        super().__init__()
        QLocale.setDefault(QLocale(QLocale.Language.Russian, QLocale.Country.Russia))
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MyPlanner()
    window.show()
    sys.exit(app.exec())
