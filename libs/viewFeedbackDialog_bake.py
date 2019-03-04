# -*- coding:utf-8 -*-

import sys
from PySide2.QtWidgets import *
from PySide2.QtCore import *
from PySide2.QtGui import *


class ViewFeedbackDialog(QDialog):
    def __init__(self, fb=None,eps=None,shot=None,artist=None,parent=None,):
        super(ViewFeedbackDialog, self).__init__(parent)
        # 设置窗口显示样式
        self.setWindowFlags(Qt.Dialog | Qt.WindowCloseButtonHint)
        self.setWindowTitle('FeedBack:')
        # 设置默认大小
        self.resize(500,400)
        # 设置背景色
        self.setStyleSheet('''QDialog{background-color:black}''')
        # 获取镜头参数
        self.eps_num = eps
        self.shot_num = shot
        self.artist = artist
        self.feedback = fb
        # 创建所有要使用的控件
        self.eps_label = QLabel('EPS:')
        self.eps_label.setStyleSheet('''QLabel{color:red}''')
        self.eps_label.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.eps_label.setFont(QFont('Microsoft YaHei', 10, QFont.Bold))

        self.eps_value = QLabel(str(self.eps_num))
        self.eps_value.setStyleSheet('''QLabel{color:rgb(255,152,0)}''')
        self.eps_value.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.eps_value.setFont(QFont('Microsoft YaHei', 10, QFont.Bold))

        self.shot_label = QLabel('SHOT:')
        self.shot_label.setStyleSheet('''QLabel{color:red}''')
        self.shot_label.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.shot_label.setFont(QFont('Microsoft YaHei', 10, QFont.Bold))

        self.shot_value = QLabel(str(self.shot_num))
        self.shot_value.setStyleSheet('''QLabel{color:rgb(255,152,0)}''')
        self.shot_value.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.shot_value.setFont(QFont('Microsoft YaHei', 10, QFont.Bold))

        self.artist_label = QLabel('ARTIST:')
        self.artist_label.setStyleSheet('''QLabel{color:red}''')
        self.artist_label.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.artist_label.setFont(QFont('Microsoft YaHei', 10, QFont.Bold))

        self.artist_value = QLabel(str(self.artist))
        self.artist_value.setStyleSheet('''QLabel{color:rgb(255,152,0)}''')
        self.artist_value.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.artist_value.setFont(QFont('Microsoft YaHei', 10, QFont.Bold))

        self.line = QFrame()
        self.line.setFrameShape(QFrame.HLine)
        self.line.setLineWidth(2)
        self.line.setStyleSheet('''QFrame{color:rgb(127,127,127)}''')

        self.editor = QTextEdit()
        self.editor.setStyleSheet('''QTextEdit{
                                     background-color:black;
                                     border:1px solid rgb(0,0,0);
                                     color:white;
                                     }''')
        # 改变光标颜色
        editor_font = QFont()
        editor_font.setFamily('Microsoft YaHei')
        # editor_font.
        self.editor.setFont(QFont('Microsoft YaHei', 12, QFont.Bold))
        # 设置不可编辑
        self.editor.setReadOnly(True)
        # 写入反馈
        self.editor.setText(self.feedback)

        # 创建布局
        # 整体布局
        self.main_layout = QVBoxLayout()
        self.main_layout.setContentsMargins(0,10,0,0)
        # 用于显示eps和shot信息的布局
        self.eps_layout = QHBoxLayout()
        self.shot_layout = QHBoxLayout()
        self.artist_layout = QHBoxLayout()
        # 上方总体横布局
        self.labels_main_layout = QHBoxLayout()

        # 创建底部的ok按钮
        self.okButton = QPushButton('OK')
        self.okButton.setFont(QFont('Microsoft YaHei', 20))

        # okButton 的样式QSS
        self.okButton_style = '''
                                                    QPushButton{
                                                    border-radius:4px;background-color:rgb(185,111,2);color:white;
                                                    border:1px solid rgb(125,125,125);
                                                    }
                                                    QPushButton:hover{
                                                    border-radius:4px;background-color:rgb(223,134,3);color:white;
                                                    }
                                                    QPushButton:pressed{
                                                    border-radius:4px;background-color:rgb(56,104,0);color:red;                 
                                                    }
                                            '''
        # 设置okButton的样式
        self.okButton.setStyleSheet(self.okButton_style)

        # 设置鼠标滑过时的鼠标形状
        self.okButton.setCursor(Qt.PointingHandCursor)

        # 绑定底部按钮的槽函数
        self.okButton.clicked.connect(self.accept)

        self.initUI()

    def initUI(self):
        # 填充布局
        self.eps_layout.addWidget(self.eps_label)
        self.eps_layout.addWidget(self.eps_value)
        self.eps_layout.setSpacing(5)

        self.shot_layout.addWidget(self.shot_label)
        self.shot_layout.addWidget(self.shot_value)
        self.shot_layout.setSpacing(5)

        self.artist_layout.addWidget(self.artist_label)
        self.artist_layout.addWidget(self.artist_value)
        self.artist_layout.setSpacing(5)

        self.labels_main_layout.addLayout(self.eps_layout)
        self.labels_main_layout.addLayout(self.shot_layout)
        self.labels_main_layout.addLayout(self.artist_layout)
        self.labels_main_layout.setSpacing(50)

        self.main_layout.addLayout(self.labels_main_layout)
        self.main_layout.addWidget(self.line)
        self.main_layout.addWidget(self.editor)
        self.main_layout.addWidget(self.okButton)
        self.main_layout.setSpacing(2)

        self.setLayout(self.main_layout)






if __name__ == '__main__':
    app = QApplication(sys.argv)
    demo = ViewFeedbackDialog(fb='Hello',eps='012',shot='012135(v003)',artist='Billy')
    demo.show()
    sys.exit(app.exec_())