from mainwindow import Mainwindow
from PyQt6.QtWidgets import QApplication
import sys

def main():
    app = QApplication(sys.argv)
    example_window = Mainwindow()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()