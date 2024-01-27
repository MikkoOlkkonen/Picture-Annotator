from PyQt6.QtWidgets import QWidget


class Annotation(QWidget):
    def __init__(self, rectangle, name):
        super().__init__()
        self.name = name
        self.rectangle = rectangle

    def get_name(self):
        return self.name

    def get_rectangle(self):
        return self.rectangle


