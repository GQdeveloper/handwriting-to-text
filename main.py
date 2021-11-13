from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QVBoxLayout, QWidget, QTextBrowser, \
    QLineEdit
from PyQt5.QtGui import QIcon, QImage, QPainter, QPen
from PyQt5.QtCore import Qt, QPoint
import sys


class AnotherWindow(QWidget):
    """
    This "window" is a QWidget. If it has no parent, it
    will appear as a free-floating window as we want.
    """

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
        self.setWindowTitle("MAIN WINDOWWWWW")
        self.setFixedSize(300, 300)
        self.image = QImage(self.size(), QImage.Format_RGB32)
        self.image.fill(Qt.white)
        self.window = AnotherWindow()
        self.window.show()

        self.drawing = False
        self.brushSize = 4
        self.brushColor = Qt.black
        self.lastPoint = QPoint()

    def filled(self):
        self.window.lineEdit.setText(self.window.lineEdit.text() + "1")

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
            self.drawing = False
            self.filled()
            self.image.fill(Qt.white)
            self.update()


app = QApplication(sys.argv)
w = MainWindow()
w.show()
app.exec()

