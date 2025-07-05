import sys
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter, QPen, QColor

class Overlay(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # Устанавливаем размер окна равным разрешению экрана
        self.setGeometry(0, 0, 1920, 1080)  # Замените на ваше разрешение экрана
        self.setWindowTitle('Overlay')
        
        # Делаем окно прозрачным и поверх всех окон
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool)
        self.setAttribute(Qt.WA_TranslucentBackground)

        # Центр экрана для квадрата
        self.square_size = 50  # Размер квадрата
        self.square_x = (1920 - self.square_size) // 2  # Центр по X
        self.square_y = (1080 - self.square_size) // 2  # Центр по Y

        self.show()

    def paintEvent(self, event):
        painter = QPainter(self)
        pen = QPen(QColor(255, 0, 0), 2)  # Красный цвет, толщина линии 2
        painter.setPen(pen)
        
        # Рисуем квадрат в центре
        painter.drawRect(self.square_x, self.square_y, self.square_size, self.square_size)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    overlay = Overlay()
    sys.exit(app.exec_())
