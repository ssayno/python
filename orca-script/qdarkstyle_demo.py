#!/usr/bin/env python3
import sys
from PyQt5.QtCore import QPoint
import qdarkstyle
from PyQt5.QtWidgets import QApplication, QMainWindow


class MyWindow(QMainWindow):
    def __init__(self):
        super(MyWindow, self).__init__()
        self.resize(500, 600)

    def mousePressEvent(self, event):
        self.oldPos = event.globalPos()
        return super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if not hasattr(self, 'oldPos'):
            self.oldPos =  event.globalPos()
        else:
            delta = QPoint(event.globalPos() - self.oldPos)
            self.move(self.x() + delta.x(), self.y() + delta.y())
            self.oldPos = event.globalPos()
        return super().mouseMoveEvent(event)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    mywindow = MyWindow()
    mywindow.show()
    sys.exit(app.exec_())
