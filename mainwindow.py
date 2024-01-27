from PyQt6.QtWidgets import QMainWindow, QPushButton, QInputDialog
from PyQt6.QtGui import QFont, QPalette, QPainter, QPen, QColor
from PyQt6.QtMultimedia import QMediaPlayer, QAudioOutput
                                from PyQt6.QtCore import Qt, QPoint, QRect, QUrl
from PyQt6.QtWidgets import QLabel
from picture import Picture
from annotation import Annotation
from dataset import ImageDataset

class Mainwindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.indeksi = 0
        self.init_ui()
        self.init_buttons()
        self.annotation_rect = None #Tästä tulee suorakaide, joka luodaan kun hiirtä painetaan ja vedetään. Lopuksi tästä tulee annotaatio
        self.is_drawing = False #Jotta mouseMoveEvent aktivoituu vain kun halutaan
        self.dataset = None
        self.kuvat = []
        self.toinenflagi = True
        self.first_image = False #Tämän avulla aloituskuvaa (tyhjä kuva) ei voi tallentaa, eikä siihen voi tehdä annotaatioita
        self.show()

    def init_ui(self):
        self.setWindowTitle("Picture Annotator")
        self.setGeometry(100, 50, 900, 650)

        palette = self.palette()
        palette.setColor(QPalette.ColorRole.Window, QColor(255, 255, 255))
        self.setPalette(palette)

        self.picture_label = QLabel(self)
        self.picture_label.setPalette(palette) #taustaväri valkoiseksi esteettisistä syistä
        self.wholeimage = Picture("self.imagename") #kuva ja annotaatiot
        self.picture_label.setPixmap(self.wholeimage.get_picture())  # avataan olematon kuva, jolloin saadaan ensinäkymä tyhjäksi

        self.setCentralWidget(self.picture_label)

    def init_buttons(self):
        self.virhenappula = QPushButton("hups", self) #nappi, josta voi poistaa viimeisimmän annotaation
        self.virhenappula.setFixedSize(150, 50)
        self.virhenappula.setFont(QFont("Comic sans", 16))
        self.virhenappula.move(705, 385)

        self.donenappula = QPushButton("Tallenna", self) #nappi, jolla kuva ja annotaatiot tallennetaan ja luodaan torchvisionin avulla dataset
        self.donenappula.setFixedSize(150, 50)
        self.donenappula.setFont(QFont("Comic sans", 16))
        self.donenappula.move(705, 285)

        self.next = QPushButton("Seuraava", self) #nappi, jolla voi selata kuvia ja niiden annotaatioita
        self.next.setFont(QFont("Comic sans", 12))
        self.next.move(110, 0)

        self.previous = QPushButton("Edellinen", self) #nappi, jolla voi selata kuvia ja niiden annotaatioita
        self.previous.setFont(QFont("Comic sans", 12))

        self.tuo = QPushButton("Tuo kuva", self) #nappi, jolla valitaan kuva, joka halutaan avata
        self.tuo.setFont(QFont("Comic sans", 12))
        self.tuo.move(300, 0)

        # Musiikkia viihdykkeeksi
        self.mysteeri = QPushButton("Musiikkia", self)
        self.mysteeri.setFont(QFont("Comic sans", 12))
        self.mysteeri.move(500, 0)

        self.player = QMediaPlayer()
        self.audio_output = QAudioOutput()
        self.player.setAudioOutput(self.audio_output)
        self.player.setSource(QUrl.fromLocalFile("hehe.MP3"))

        # Lopettaa ohjelman
        self.OKnappula = QPushButton("Poistu", self)
        self.OKnappula.setFixedSize(150, 50)
        self.OKnappula.setFont(QFont("Comic sans", 16))
        self.OKnappula.move(705, 485)
        self.OKnappula.clicked.connect(self.lopeta)

        # Luo tallennetuista kuvista PyTorch datasetin
        self.datasettinappi = QPushButton("Dataset", self)
        self.datasettinappi.setFixedSize(150, 50)
        self.datasettinappi.setFont(QFont("Comic sans", 16))
        self.datasettinappi.move(705, 0)

        self.mysteeri.clicked.connect(self.playsound)
        self.donenappula.clicked.connect(self.save_image)
        self.virhenappula.clicked.connect(self.removeannotation)
        self.next.clicked.connect(self.next_picture)
        self.previous.clicked.connect(self.previous_picture)
        self.tuo.clicked.connect(self.load_image)
        self.datasettinappi.clicked.connect(self.create_dataset)


    def removeannotation(self):
        self.wholeimage.removeannotation()
        self.update()


    def paintEvent(self, event):
        self.kuvankopio = self.wholeimage.get_picture().copy()
        painter = QPainter(self.kuvankopio)
        if self.annotation_rect is not None or len(self.wholeimage.get_annotations()) > 0:
            pen = QPen(QColor(255, 0, 0), 2, Qt.PenStyle.SolidLine)
            painter.setPen(pen)
            if self.annotation_rect is not None:#Piirretään suorakaidetta, josta tulee annotaatio
                painter.drawRect(self.annotation_rect)
            for annotaatio in self.wholeimage.get_annotations(): #Piirretään annotaatiot
                painter.drawRect(annotaatio.get_rectangle())
                painter.drawText(annotaatio.get_rectangle().bottomLeft() + QPoint(5, -5), annotaatio.get_name())
            self.picture_label.setPixmap(self.kuvankopio)
        else:
            self.picture_label.setPixmap(self.wholeimage.get_picture())

    def mousePressEvent(self, event):
        if self.first_image:
            self.is_drawing = True
            self.start_pos = event.pos()
    def mouseMoveEvent(self, event):
        if self.first_image:
            if self.is_drawing:
                self.annotation_rect = QRect(self.start_pos, event.pos()).normalized()

    def mouseReleaseEvent(self, event):
        if self.first_image:
            self.is_drawing = False
            text, ok = QInputDialog.getText(self, 'Text input dialog', 'Syötä nimi annotaatiolle')
            if ok:
                self.wholeimage.get_annotations().append(Annotation(self.annotation_rect, text))
            self.annotation_rect = None

    def load_image(self):
        text, ok = QInputDialog.getText(self, 'Kuva?', 'Syötä kuva')
        if ok:
            self.imagename = text
            self.update_image()
            self.first_image = True


    def update_image(self):
        self.wholeimage = Picture(self.imagename)
        self.picture_label.setPixmap(self.wholeimage.get_picture())
        self.annotation_rect = None
        self.update()


    def save_image(self):
        if self.first_image:
            flag = True
            for kuva in self.kuvat:
                if kuva == self.wholeimage:
                    kuva.set_annotations(self.wholeimage.get_annotations())
                    flag = False
            if flag:
                if len(self.kuvat) > 0:
                    self.indeksi += 1
                self.kuvat.append(self.wholeimage)


    def next_picture(self):
        if len(self.kuvat) > 1:
            if self.indeksi < (len(self.kuvat) - 1):
                self.indeksi += 1
                self.wholeimage = self.kuvat[self.indeksi]
                self.wholeimage.set_annotations(self.kuvat[self.indeksi].get_annotations())
                self.picture_label.setPixmap(self.wholeimage.get_picture())
                self.annotation_rect = None

    def previous_picture(self):
        if len(self.kuvat) > 1:
            if self.indeksi > 0:
                self.indeksi -= 1
                self.wholeimage = self.kuvat[self.indeksi]
                self.wholeimage.set_annotations(self.kuvat[self.indeksi].get_annotations())
                self.picture_label.setPixmap(self.wholeimage.get_picture())
                self.annotation_rect = None
        elif len(self.kuvat) == 1:
            self.wholeimage = self.kuvat[self.indeksi]
            self.picture_label.setPixmap(self.wholeimage.get_picture())


    def set_image(self, image_path): #testausta varten
        self.wholeimage = Picture(image_path)
        self.picture_label.setPixmap(self.wholeimage.get_picture())
        self.annotation_rect = None
        self.update()

    def create_dataset(self):
        self.dataset = ImageDataset(self.kuvat)

    def playsound(self):
        if self.toinenflagi:
            self.player.play()
            self.toinenflagi = False
        else:
            self.player.stop()
            self.toinenflagi = True

    def lopeta(self):
        self.close()
