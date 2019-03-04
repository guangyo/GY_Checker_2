# -*- coding:utf-8 -*-

import sys
from PySide2.QtWidgets import *
from PySide2.QtCore import *
from PySide2.QtGui import *
from libs.imageShower import *
from libs.showImageButton import *


class ViewFeedbackDialog(QDialog):
    def __init__(self, fb=None,eps=None,shot=None,artist=None,parent=None,):
        super(ViewFeedbackDialog, self).__init__(parent)
        # 设置窗口显示样式
        self.setWindowFlags(Qt.Dialog | Qt.FramelessWindowHint)
        self.setWindowTitle('LastFeedBack:')
        # 设置默认大小
        self.resize(500,400)
        # 设置背景色
        self.setStyleSheet('''QDialog{background-color:rgb(20,20,20)}''')
        # 设置窗口拖动参数的默认值
        self.m_drag = False
        # 获取镜头参数
        self.eps_num = eps
        self.shot_num = shot
        self.artist = artist
        self.feedback = fb
        if not self.feedback:
            self.feedback = dict()
        # 将反馈分为文字和图片两类
        self.text_feedback = ''
        self.pic_feedback = list()
        # 从反馈信息中填充反馈
        if 'text' in self.feedback.keys():
            self.text_feedback = self.feedback['text']
        if 'pic' in self.feedback.keys():
            self.pic_feedback = self.feedback['pic']
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

        # 创建imageLayout布局用于显示反馈中的图片
        self.imageLayout = QHBoxLayout()
        self.imageLayout.setSpacing(5)

        # 创建存放imageButton实例的字典
        self.imageButtonDict = dict()

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

        self.write_feedback()

    def write_feedback(self):
        '''
        将反馈信息写入textEdit
        :return:
        '''
        self.editor.setText(self.text_feedback)
        self.editor.moveCursor(QTextCursor.End,QTextCursor.MoveAnchor)
        # 使用append实现换行
        self.editor.append('')
        if len(self.pic_feedback) != 0:
            self.makeImageButton()

    def makeImageButton(self):
        '''
        根据反馈中的图片，创建显示图片的控件
        :return: None
        '''
        for i in self.pic_feedback:
            # 创建按钮
            self.imageButtonDict[i] = ImageButton(pic=i)
            # 连接槽函数
            self.imageButtonDict[i].clicked.connect(self.onImageButtonClicked)
            # 添加图片按钮到布局
            self.imageLayout.addWidget(self.imageButtonDict[i],Qt.AlignLeft)

        self.imageLayout.addStretch()
        self.main_layout.insertLayout(3, self.imageLayout)

    def onImageButtonClicked(self):
        '''
        定义点击ImageButton被点击的事件
        :param pic:要展示图片路径
        :return: 展示传入的图片
        '''
        imageShower = ImageShower(self,self.sender().pic)
        imageShower.show()

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
    test_fb = {u'text': u'\u786e\u8ba4\u8c03\u8272\uff0c\u73b0\u5728\u611f\u89c9\u53ef\u80fd\u8fc7\u84dd\u4e86\uff08\u89d2\u8272\u4e3a\u7ea2\u8863\u670d\uff09\u3002\u6ce8\u610f\u4f4e\u8bed\u4e4b\u529b\u989c\u8272\u7684\u5339\u914d', u'pic': [u'./last_fb_img\\EPS012\\dza012106\\dza_012_dza012106_0.png', u'./last_fb_img\\EPS012\\dza012106\\dza_012_dza012106_1.png']}
    app = QApplication(sys.argv)
    demo = ViewFeedbackDialog(fb=test_fb,eps='012',shot='012135(v003)',artist='Billy')
    demo.show()
    sys.exit(app.exec_())