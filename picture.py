from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QWidget

class Picture(QWidget):
    def __init__(self, image_path):
        super().__init__()
        self.annotations = []
        self.picture = QPixmap(image_path)

    def get_annotations(self):
        return self.annotations

    def get_picture(self):
        return self.picture

    def set_annotations(self, annotations):
        self.annotations = annotations

    def removeannotation(self):
        if len(self.annotations) > 0:
            del self.annotations[-1]