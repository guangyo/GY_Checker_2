# -*- coding:utf-8 -*-
import sys
from PySide2.QtWidgets import *
from PySide2.QtCore import *
from PySide2.QtGui import *


class SubmitDialog(QDialog):
    def __init__(self):
        super(SubmitDialog, self).__init__()
        self.label = QLabel('INPUTING...')
        self.label.setFont(QFont('Microsoft YaHei', 18))
        self.label.setStyleSheet('''QLabel{color:rgb(155,155,155)}''')
        self.label.setFixedSize(220,30)
        # 设置背景色
        self.setStyleSheet('''QDialog{background-color:black}''')
        # 创建进度条控件
        self.pbar = QProgressBar()

        # 创建时间对象（测试用）
        self.timer = QBasicTimer()
        self.step = 0

        self.resize(350,220)
        self.setWindowTitle('INPUTING:')

        layout = QVBoxLayout()
        layout.addWidget(self.label,0,Qt.AlignHCenter)
        layout.addWidget(self.pbar)
        layout.setSpacing(0)
        self.setLayout(layout)

        layout.setContentsMargins(20,0,20,0)
        self.pbar.resize(200, 55)

        self.pbar.setStyleSheet('''
                                QProgressBar{
                                border:1px solid rgb(188,188,188);
                                border-radius:10px;
                                text-align:center;
                                color:rgb(74,0,5);
                                background:grey;}
                                QProgressBar::chunk{
                                border-radius:10px;
                                background:qlineargradient(spread:pad,x1:0,y1:0,x2:1,y2:0,stop:0 rgb(158,98,0),stop:1 rgb(255,0,9));
                                }
                                ''')
        self.initUI()

    def timerEvent(self, e):
        if self.step >= 100:
            self.timer.stop()
            self.setWindowTitle('完成')
            # 进度条走完关闭窗口~，关联的事件应用中需要替换
            self.accept()
            return
        self.step += 5
        self.label.setText('INPUTING:%d' % self.step + '%')
        self.pbar.setValue(self.step)

    def initUI(self):
        self.timer.start(100,self)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    demo = SubmitDialog()
    demo.show()
    sys.exit(app.exec_())
