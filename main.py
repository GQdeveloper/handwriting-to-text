import tensorflow as tf
import numpy as np
from PIL import Image, ImageOps
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QVBoxLayout, QWidget, QTextBrowser, \
    QLineEdit
from PyQt5.QtGui import QImage, QPainter, QPen
from PyQt5.QtCore import Qt, QPoint
import sys


# creating a floating window with an internal layout
class AnotherWindow(QWidget):

    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        self.setLayout(layout)

        # self.painter = Canvas()
        self.browser = QTextBrowser()
        self.browser.resize(100, 100)

        self.lineEdit = QLineEdit(self)
        self.lineEdit.resize(380, 30)

        self.labelOne = QLabel("Text", self)
        self.labelOne.setStyleSheet("background-color: white")
        self.labelOne.resize(380, 30)

        self.labelTwo = QLabel("hand input", self)
        self.labelTwo.setStyleSheet("background-color: white")
        self.labelTwo.resize(380, 30)

        self.sendButton = QPushButton("Send", self)
        self.sendButton.clicked.connect(self.on_send)

        layout.addWidget(self.browser)
        layout.addWidget(self.labelOne)
        layout.addWidget(self.lineEdit)
        layout.addWidget(self.sendButton)
        layout.addWidget(self.labelTwo)

    def on_send(self):
        textInput = self.lineEdit.text()
        self.browser.append(textInput)
        self.lineEdit.clear()


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        #loading tensorflow model
        self.model = tf.keras.models.load_model('predic_dig.model')
        self.setWindowTitle("MAIN WINDOWWWWW")
        self.setFixedSize(300, 300)
        self.image = QImage(self.size(), QImage.Format_RGB32)
        self.image.fill(Qt.white)
        self.window = AnotherWindow()
        self.window.show()

        self.drawing = False
        self.brushSize = 15
        self.brushColor = Qt.black
        self.lastPoint = QPoint()

    def paintEvent(self, event):
        canvasPainter = QPainter(self)
        canvasPainter.begin(self)
        canvasPainter.drawImage(self.rect(), self.image)
        canvasPainter.end()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drawing = True
            self.lastPoint = event.pos()

    def mouseMoveEvent(self, event):
        if (event.buttons() & Qt.LeftButton) & self.drawing:
            painter = QPainter(self.image)
            painter.setPen(QPen(self.brushColor, self.brushSize))
            painter.drawLine(self.lastPoint, event.pos())
            self.lastPoint = event.pos()
            self.update()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.update()
            img = self.image

            data = img.constBits().asstring(img.byteCount())
            pilimg = Image.frombuffer('RGBA', (img.width(), img.height()), data, 'raw', 'RGBA', 0, 1)

            img = ImageOps.grayscale(pilimg)

            img = img.resize((28, 28))

            img = tf.keras.utils.normalize(img, axis=1)

            img = np.array(img).reshape(-1, 28, 28, 1)

            # img = img / 255.0
            print(img.shape)
            # predicting the class
            res = self.model.predict([img])[0]
            answer = np.argmax(res)
            print(res)

            self.drawing = False
            self.window.lineEdit.setText(self.window.lineEdit.text() + str(answer))

            self.image.fill(Qt.white)
            self.update()


app = QApplication(sys.argv)
w = MainWindow()
w.show()
app.exec()
