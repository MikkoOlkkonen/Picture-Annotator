import unittest
from mainwindow import Mainwindow
from dataset import ImageDataset
from annotation import Annotation
from picture import Picture
from PyQt6.QtCore import QRect

class Test(unittest.TestCase):

    def test_removeannotation(self):
        self.picture = Picture("jonikopio.png")
        annotaatio = Annotation(QRect(0, 0, 100, 100), "annotaatio")
        self.picture.set_annotations([annotaatio])
        self.assertEqual(len(self.picture.annotations()), 1)
        self.picture.removeannotation()
        self.assertEqual(len(self.picture.annotations()), 0)

if __name__ == "__main__":
    unittest.main()