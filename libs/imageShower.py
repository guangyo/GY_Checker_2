# -*- coding:utf8 -*-
import sys
from PySide2.QtWidgets import *
from PySide2.QtCore import *
from PySide2.QtGui import *


class ImageShower(QDialog):
    def __init__(self,parent=None,pic=None):
        super(ImageShower, self).__init__(parent)
        self.pic = pic
        self.setWindowTitle('Show Image:')
        # 设置背景图片
        self.setStyleSheet('''QDialog{border-image:url('%s');}''' % self.pic.replace('\\','/'))
        self.imagePic = QImage(self.pic)
        # 获取图像大小信息
        self.imageWidth = self.imagePic.width()
        self.imageHeight = self.imagePic.height()
        self.image_ratio = float(self.imageWidth)/self.imageHeight
        self.resize(self.imageWidth,self.imageHeight)
        # 设置默认拖拽状态
        self.m_drag = False

        # 设置提示信息
        self.setToolTip('Esc或鼠标双击关闭窗口')

        # 设置窗口样式(无标题)
        self.setWindowFlags(Qt.Dialog | Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)

    # 滚轮实现图片缩放
    def wheelEvent(self,event):
        tmp = self.geometry()
        centerPoint = tmp.center()
        adjustSize = 30
        if event.angleDelta().y() > 0:
            tmp.setWidth(tmp.width()+adjustSize)
            tmp.setHeight(tmp.height() + adjustSize/self.image_ratio)
        else:
            tmp.setWidth(tmp.width() - adjustSize)
            tmp.setHeight(tmp.height() - adjustSize/self.image_ratio)

        if tmp.width() > 200:
            tmp.moveCenter(centerPoint)
            self.setGeometry(tmp)

    # 窗口拖动和关闭实现
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.m_drag = True
            self.m_DragPosition = event.globalPos() - self.pos()
            self.setCursor(QCursor(Qt.OpenHandCursor))
        if event.button() == Qt.RightButton:
            self.close()

    def mouseMoveEvent(self, QMouseEvent):
        if Qt.LeftButton and self.m_drag:
            # 当左键移动窗体修改偏移值
            # QPoint
            # 实时计算窗口左上角坐标
            self.move(QMouseEvent.globalPos() - self.m_DragPosition)

    def mouseReleaseEvent(self, QMouseEvent):
        self.m_drag = False
        self.setCursor(QCursor(Qt.ArrowCursor))

    def mouseDoubleClickEvent(self, *args, **kwargs):
        self.close()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    demo = ImageShower(pic=u'../last_fb_img/EPS012\\dza012106\\dza_012_dza012106_1.png'.replace('\\','/'))
    demo.show()
    sys.exit(app.exec_())
