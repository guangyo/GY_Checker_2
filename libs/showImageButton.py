# -*- coding:utf8 -*-
from PySide2.QtWidgets import QPushButton
from PySide2.QtCore import *
from PySide2.QtGui import *


class ImageButton(QPushButton):
    '''
        用于展示反馈图片的button类
        '''
    # 自定义按钮的右键单击信号
    mouseRightClicked = Signal()

    def __init__(self,parent = None,pic = None,item = None):
        super(ImageButton, self).__init__(parent)
        self.pic = pic
        # 记录是第几个按钮的计数item
        self.item = item
        self.setFixedSize(80, 80)
        self.setIcon(QIcon(self.pic))
        self.setStyleSheet('''QPushButton{background-color:rgb(25,25,25);}''')
        self.setIconSize(QSize(80, 80))
        self.setCursor(Qt.PointingHandCursor)

    # 重写鼠标的按键事件，用于相应右键点击
    def mouseReleaseEvent(self, event):
        if event.button() == Qt.RightButton:
            self.mouseRightClicked.emit()

        elif event.button() == Qt.LeftButton:
            self.clicked.emit()