# -*- coding:utf-8 -*-

import sys,os
from PySide2.QtWidgets import *
from PySide2.QtCore import *
from PySide2.QtGui import *
from libs.showImageButton import *
from libs.imageShower import *


class CreateFeedbackDialog(QDialog):
    customSignal = Signal(dict)
    customSignal2 = Signal()

    def __init__(self,eps=None,shot=None,artist=None,parent=None,):
        super(CreateFeedbackDialog, self).__init__(parent)
        # 设置保存图片的迭代数
        self.index = 0
        # 设置表头显示样式
        self.setWindowFlags(Qt.Dialog | Qt.FramelessWindowHint)
        self.setWindowTitle('CreateFeedBack:')
        # 设置默认大小
        self.resize(500,400)
        # 用于存放图片反馈的字典
        self.fb_pic_dict = dict()
        # 设置背景色
        self.setStyleSheet('''QDialog{background-color:black}''')
        # 获取镜头参数
        self.eps_num = eps
        self.shot_num = shot
        self.artist = artist
        self.feedback = dict()
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

        # 创建布局
        # 整体布局
        self.main_layout = QVBoxLayout()
        self.main_layout.setContentsMargins(0,10,0,0)
        # 用于显示eps和shot,Artist信息的布局
        self.eps_layout = QHBoxLayout()
        self.shot_layout = QHBoxLayout()
        self.artist_layout = QHBoxLayout()
        # 上方总体横布局
        self.labels_main_layout = QHBoxLayout()
        # 下方按钮横布局
        self.buttons_main_layout = QHBoxLayout()

        # 创建底部的ok按钮
        self.okButton = QPushButton('SUBMIT')
        self.okButton.setFont(QFont('Microsoft YaHei', 20))

        # okButton 的样式QSS
        self.okButton_style = '''
                                                    QPushButton{
                                                    border-radius:4px;background-color:rgb(185,111,2);color:white;
                                                    border:2px solid rgb(112,112,112);
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

        # 创建底部的cancle按钮
        self.cancleButton = QPushButton('CANCEL')
        self.cancleButton.setFont(QFont('Microsoft YaHei', 20))

        # cancleButton 的样式QSS
        self.cancleButton_style = '''
                                           QPushButton{
                                           border-radius:4px;background-color:rgb(131,0,4);color:white;
                                           border:2px solid rgb(112,112,112);
                                           }
                                           QPushButton:hover{
                                           border-radius:4px;background-color:rgb(183,0,6);color:white;
                                           }
                                           QPushButton:pressed{
                                           border-radius:4px;background-color:rgb(113,0,4);color:red;                 
                                           }
                                   '''
        # 设置cancleButton的样式
        self.cancleButton.setStyleSheet(self.cancleButton_style)

        # 创建插入图片按钮
        self.addImageButton = QPushButton()
        self.addImageButton.setFixedSize(80,80)
        self.addImageButton.setIcon(QIcon('../images/add_image_2.png'))
        self.addImageButton.setIconSize(QSize(80,80))
        self.addImageButton.setToolTip('点击插入剪贴板图片,快捷键：Ctrl + d')


        # addImageButton 的样式QSS
        self.addImageButton_style = '''
                                           QPushButton{
                                           border-radius:4px;background-color:rgb(0,0,0);
                                           
                                           }
                                           QPushButton:hover{
                                           border-radius:4px;background-color:rgb(25,25,25);color:white;
                                           }
                                           QPushButton:pressed{
                                           border-radius:4px;background-color:rgb(113,0,4);color:red;
                                           }
                                   '''
        # 设置addImageButton的样式
        self.addImageButton.setStyleSheet(self.addImageButton_style)

        # 设置鼠标滑过时的鼠标形状
        self.okButton.setCursor(Qt.PointingHandCursor)
        self.cancleButton.setCursor(Qt.PointingHandCursor)
        self.addImageButton.setCursor(Qt.PointingHandCursor)

        # 实例化剪贴板
        self.clipboard = QApplication.clipboard()

        # 创建imageLayout布局用于显示反馈中的图片
        self.imageLayout = QHBoxLayout()
        self.imageLayout.setSpacing(5)

        # 创建存放imageButton实例的字典
        self.imageButtonDict = dict()

        # 连接槽函数
        self.okButton.clicked.connect(self.emit_signal)
        self.cancleButton.clicked.connect(self.accept)
        # 关联添加图片按钮
        self.addImageButton.clicked.connect(self.insertFromMimeData)
        # 关联剪贴板发生变化时的槽函数
        self.clipboard.dataChanged.connect(self.insertFromMimeData)

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

        self.buttons_main_layout.addWidget(self.okButton)
        self.buttons_main_layout.addWidget(self.cancleButton)
        self.buttons_main_layout.setSpacing(1)

        self.main_layout.addLayout(self.imageLayout)
        self.main_layout.addLayout(self.buttons_main_layout)

        self.main_layout.setSpacing(2)

        self.setLayout(self.main_layout)

    # 创建自定义信号发送，用于发送textEdit中的信息给checkShotClass类的实例
    def emit_signal(self):
        self.feedback['text'] = self.editor.toPlainText()
        if self.fb_pic_dict.has_key('pic_path'):
            self.feedback['pic'] = self.fb_pic_dict['pic_path']
        else:
            self.feedback['pic'] = list()
        self.customSignal.emit(self.feedback)
        self.accept()

    def getFeedback(self):
        self.feedback = self.editor.toHtml()
        return self.feedback

    # 检测键盘按键
    def keyPressEvent(self, event):
        # 按下 ctrl + d 发射信号
        if event.key() == Qt.Key_D:
            if QApplication.keyboardModifiers() == Qt.ControlModifier:
                self.insertFromMimeData()
            else:
                pass

    def insertFromMimeData(self):
        if self.clipboard.mimeData().hasImage():
            self.index += 1
            # 第一次截图的时候给fb_pic_dict添加key和一个默认的空字典用于存储图片路径
            if self.index == 1:
                self.fb_pic_dict['pic_path'] = []
            # 创建保存路径
            dir = './fb_img/%s/%s/%s_%d.png' % (self.eps_num,self.shot_num,self.eps_num + '_' + self.shot_num,self.index)
            self.fb_pic_dict['pic_path'].append(dir)
            if not os.path.exists(os.path.dirname(dir)):
                os.makedirs(os.path.dirname(dir))
            elif os.path.exists(dir):
                os.remove(dir)
            # 得到并保存图片
            pic = self.clipboard.pixmap()
            pic.save(dir)

            # 创建图片按钮用于在面板展示截图
            # 创建存放imageButton实例的字典
            self.imageButtonDict[self.index] = ImageButton(pic=dir,item=self.index)
            # 连接槽函数
            self.imageButtonDict[self.index].clicked.connect(self.onImageButtonClicked)
            self.imageButtonDict[self.index].mouseRightClicked.connect(self.onImageButtonRightClicked)
            # 添加图片按钮到布局
            if self.index == 1:
                self.imageLayout.addWidget(self.imageButtonDict[self.index], Qt.AlignLeft)
                self.imageLayout.addStretch()
            else:
                self.imageLayout.insertWidget(0,self.imageButtonDict[self.index], Qt.AlignLeft)

    def onImageButtonClicked(self):
        '''
        定义点击ImageButton被点击的事件
        :param pic:要展示图片路径
        :return: 展示传入的图片
        '''
        imageShower = ImageShower(self,self.sender().pic)
        imageShower.show()

    def onImageButtonRightClicked(self):
        '''
        image按钮的右键单击事件响应，删除控件和图片文件,清除相应的字典项
        :return:
        '''
        # 清除图片文件
        os.remove(self.sender().pic)
        # 清除图片文件路径对应的字典项
        self.fb_pic_dict['pic_path'].remove(self.sender().pic)
        # 清除按钮字典以及按钮本身
        del self.imageButtonDict[self.sender().item]
        self.imageLayout.removeWidget(self.sender())
        self.sender().deleteLater()

    # 窗口拖动和关闭实现
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.m_drag = True
            self.m_DragPosition = event.globalPos() - self.pos()
            self.setCursor(QCursor(Qt.OpenHandCursor))

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
    demo = CreateFeedbackDialog(eps='012',shot='012135(v003)',artist='Billy')
    demo.show()
    sys.exit(app.exec_())