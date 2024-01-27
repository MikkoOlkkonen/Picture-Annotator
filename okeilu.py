from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout
from PyQt5.QtGui import QPainter, QColor, QPen, QPixmap
from PyQt5.QtCore import Qt, QRect

class MyWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.rect = QRect(0, 0, 100, 100)
        self.label_imageDisplay = QLabel(self)
        # convert image file into pixmap
        self.pixmap_image = QPixmap("jonikopio.png")


        # create painter instance with pixmap
        self.painterInstance = QPainter(self.pixmap_image)

        # set rectangle color and thickness
        self.penRectangle = QPen(Qt.red)
        self.penRectangle.setWidth(3)

        # draw rectangle on painter
        self.painterInstance.setPen(self.penRectangle)
        self.painterInstance.drawRect(self.rect)

        # set pixmap onto the label widget
        self.label_imageDisplay.setPixmap(self.pixmap_image)
        self.label_imageDisplay.show()

if __name__ == '__main__':
    app = QApplication([])
    widget = MyWidget()
    widget.show()
    app.exec_()