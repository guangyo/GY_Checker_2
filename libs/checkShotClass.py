# -*- coding:utf-8 -*-
from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *
from libs.viewFeedbackDialog import *
from libs.createFeedbackDialog import *
from libs.viewLastFeedbackDialog import *
from functools import partial

class CheckShot():
    count = 0

    def __init__(self, id, project, eps, shot_num, version, artiest, last_fb, file_path, check_table, result_table):
        # 实例化计数（DEBUG用）
        CheckShot.count += 1
        # 实例化两张数据表
        self.check_table = check_table
        self.result_table = result_table
        # checkshot的相关属性设置
        self.id = id
        self.project = project
        self.eps = eps
        self.shot = shot_num
        self.version = version
        self.artiest = artiest
        self.last_fb = last_fb
        self.file_path = file_path
        self.eps_item = QTableWidgetItem(self.eps)
        self.eps_item.setTextAlignment(Qt.AlignCenter)
        self.shot_item = QTableWidgetItem(self.shot + '(' + self.version + ')')
        self.shot_item.setTextAlignment(Qt.AlignCenter)
        self.artiest_item = QTableWidgetItem(self.artiest)
        self.artiest_item.setTextAlignment(Qt.AlignCenter)

        # 用于显示在result视图中
        self.eps2 = eps
        self.eps_item2 = QTableWidgetItem(self.eps2)
        self.eps_item2.setTextAlignment(Qt.AlignCenter)
        self.shot_item2 = QTableWidgetItem(self.shot + '(' + self.version + ')')
        self.shot_item2.setTextAlignment(Qt.AlignCenter)
        self.artiest_item2 = QTableWidgetItem(self.artiest)
        self.artiest_item2.setTextAlignment(Qt.AlignCenter)

        # 设置表格查询时使用的参数默认值
        self.tableIndex = None
        self.row_num = None
        self.colum_num = None
        # 默认当前反馈给空
        self.fb = None
        # 默认检查状态
        self.checked = False
        # 设置镜头的默认通过状态
        self.apr = False

        # 设置初始状态的鼠标点击的x和y位置信息
        self.x = 0
        self.y = 0

        # 设置镜头的相关按钮
        # 镜头通过按钮
        self.apr_btn = QPushButton()
        self.apr_btn.setFixedSize(37,37)
        self.apr_btn.setObjectName('apr_btn')
        # 设置鼠标滑过时的鼠标形状
        self.apr_btn.setCursor(Qt.PointingHandCursor)
        # 设置通过按钮的样式
        self.apr_btn.setFlat(True)
        self.apr_btn_style = '''
                QPushButton{
                background-image:url('./images/YES.png');
                border-radius:10px;                
                }
                QPushButton:hover
                {
                background-image:url('./images/YES_hover.png');
                }
                QPushButton:pressed
                {
                background-image:url('./images/YES_press.png');
                }
                '''
        self.apr_btn.setStyleSheet(self.apr_btn_style)
        # 使用一个容器安放通过按钮，以实现在单元格中的中对齐
        self.apr_btn_widget = QWidget()
        self.apr_btn_layout = QHBoxLayout()
        self.apr_btn_layout.setSpacing(0)
        self.apr_btn_layout.setContentsMargins(0,0,0,0)
        self.apr_btn_layout.addWidget(self.apr_btn,Qt.AlignCenter)
        self.apr_btn_widget.setLayout(self.apr_btn_layout)

        # 反馈按钮
        self.retake_btn = QPushButton()
        self.retake_btn.setFixedSize(37,37)
        self.retake_btn.setObjectName('retake_btn')
        # 设置鼠标滑过时的鼠标形状
        self.retake_btn.setCursor(Qt.PointingHandCursor)
        # 设置反馈按钮的样式
        self.retake_btn.setStyleSheet('''
                        QPushButton#retake_btn{
                        background-image:url('./images/retake.png');
                        border-radius:4px;                        
                        }
                        QPushButton#retake_btn:hover
                        {
                        background-image:url('./images/retake_hover.png');
                        }
                        QPushButton#retake_btn:pressed
                        {
                        background-image:url('./images/retake_press.png');
                        }
                        ''')
        # 使用一个容器安放retake_btn按钮，以实现在单元格中的中对齐
        self.retake_btn_widget = QWidget()
        self.retake_btn_layout = QHBoxLayout()
        self.retake_btn_layout.setSpacing(0)
        self.retake_btn_layout.setContentsMargins(0, 0, 0, 0)
        self.retake_btn_layout.addWidget(self.retake_btn, Qt.AlignCenter)
        self.retake_btn_widget.setLayout(self.retake_btn_layout)

        # 回退按钮
        self.rollback_btn = QPushButton()
        self.rollback_btn.setFixedSize(37,37)
        self.rollback_btn.setObjectName('rollback_btn')
        # 设置鼠标滑过时的鼠标形状
        self.rollback_btn.setCursor(Qt.PointingHandCursor)
        # 设置回退按钮的样式
        self.rollback_btn.setStyleSheet('''
                                QPushButton#rollback_btn{
                                background-image:url('./images/reload.png');
                                border-radius:4px;                                
                                }
                                QPushButton#rollback_btn:hover
                                {
                                background-image:url('./images/reload_hover.png');
                                }
                                QPushButton#rollback_btn:pressed
                                {
                                background-image:url('./images/reload_press.png');
                                }
                                ''')
        # 使用一个容器安放rollback_btn按钮，以实现在单元格中的中对齐
        self.rollback_btn_widget = QWidget()
        self.rollback_btn_layout = QHBoxLayout()
        self.rollback_btn_layout.setSpacing(0)
        self.rollback_btn_layout.setContentsMargins(0, 0, 0, 0)
        self.rollback_btn_layout.addWidget(self.rollback_btn, Qt.AlignCenter)
        self.rollback_btn_widget.setLayout(self.rollback_btn_layout)

        # 查看上一版反馈按钮
        self.view_last_fb_btn = QPushButton('VIEW')
        self.view_last_fb_btn.setFont(QFont("Microsoft YaHei", 12, QFont.Bold))
        self.view_last_fb_btn.setObjectName('last_fb_btn')
        # 设置按钮大小
        self.view_last_fb_btn.setFixedSize(60, 38)
        # 设置鼠标滑过时的鼠标形状
        self.view_last_fb_btn.setCursor(Qt.PointingHandCursor)
        # 设置按钮的样式
        self.view_last_fb_btn.setStyleSheet('''
                QPushButton{
                border-radius:4px;
                border:2px groove rgb(187,187,187);
                border-style: outset;
                background-color:rgb(145,86,0);
                color:white;       
                }
                QPushButton:hover
                {
                color:red;
                background-color:rgb(202,120,0);
                border:2px groove rgb(5,121,221);
                }
                QPushButton:pressed
                {
                color:white;
                background-color:rgb(240,142,0);
                }
                ''')
        # 使用一个容器安放view_last_fb_btn按钮，以实现在单元格中的中对齐
        self.view_last_fb_btn_widget = QWidget()
        self.view_last_fb_btn_layout = QHBoxLayout()
        self.view_last_fb_btn_layout.setSpacing(0)
        self.view_last_fb_btn_layout.setContentsMargins(0, 0, 0, 0)
        self.view_last_fb_btn_layout.addWidget(self.view_last_fb_btn, Qt.AlignCenter)
        self.view_last_fb_btn_widget.setLayout(self.view_last_fb_btn_layout)

        # 查看反馈按钮
        self.view_fb_btn = QPushButton('VIEW')
        self.view_fb_btn.setFont(QFont("Microsoft YaHei", 12, QFont.Bold))
        self.view_fb_btn.setObjectName('fb_btn')
        # 设置按钮大小
        self.view_fb_btn.setFixedSize(60, 38)
        # 设置鼠标滑过时的鼠标形状
        self.view_fb_btn.setCursor(Qt.PointingHandCursor)
        # 设置按钮的样式
        self.view_fb_btn.setStyleSheet('''
                        QPushButton#fb_btn{
                        border-radius:4px;
                        border:2px groove rgb(187,187,187);
                        border-style: outset;
                        background-color:rgb(145,86,0);
                        color:white;       
                        }
                        QPushButton#fb_btn:hover
                        {
                        color:red;
                        background-color:rgb(202,120,0);
                        border:2px groove rgb(5,121,221);
                        }
                        QPushButton#fb_btn:pressed
                        {
                        color:white;
                        background-color:rgb(240,142,0);
                        }
                        ''')
        # 使用一个容器安放view_fb_btn按钮，以实现在单元格中的中对齐
        self.view_fb_btn_widget = QWidget()
        self.view_fb_btn_layout = QHBoxLayout()
        self.view_fb_btn_layout.setSpacing(0)
        self.view_fb_btn_layout.setContentsMargins(0, 0, 0, 0)
        self.view_fb_btn_layout.addWidget(self.view_fb_btn, Qt.AlignCenter)
        self.view_fb_btn_widget.setLayout(self.view_fb_btn_layout)

        # 创建任务的状态标签
        self.status = QPushButton()
        self.status.setFixedSize(37,37)
        self.status.setStyleSheet('''
        QPushButton{
        background-image:url('./images/YES.png');
        border-radius:10px;
        }
        ''')
        self.status.setDisabled(True)
        # 创建一个容器放置状态标签，以实现在单元格中的中对齐
        self.status_widget = QWidget()
        self.status_layout = QHBoxLayout()
        self.status_layout.setSpacing(0)
        self.status_layout.setContentsMargins(0, 0, 0, 0)
        self.status_layout.addWidget(self.status, Qt.AlignCenter)
        self.status_widget.setLayout(self.status_layout)

        self.apr_btn2 = QPushButton()
        self.apr_btn2.clicked.connect(self.test_btn)

        # 连接槽函数
        self.apr_btn.clicked.connect(lambda : self.click_on_apr_btn(self.check_table,self.result_table))
        self.rollback_btn.clicked.connect(lambda: self.click_on_rollback_btn(self.check_table, self.result_table))

        self.click_on_apr_btn2 = self.click_on_apr_btn

        self.view_fb_btn.clicked.connect(self.view_feedback_dialog)

        self.view_last_fb_btn.clicked.connect(self.view_last_feedback_dialog)

        self.retake_btn.clicked.connect(self.on_click_retake_btn)

    def __del__(self):
        CheckShot.count -= 1

    # 设置row_num的方法
    def setRowNum(self,rownum):
        self.row_num = rownum

    # 设置apr_btn的槽函数
    def click_on_apr_btn(self,check_table,result_table):
        # 设置镜头检查状态
        self.checked = True
        # 更改镜头通过状态
        self.apr = True
        # 确定点击的按钮所在行
        (x, y) = (self.apr_btn_widget.frameGeometry().x(), self.apr_btn_widget.frameGeometry().y())
        self.tableIndex = check_table.indexAt(QPoint(x, y))
        self.row_num = self.tableIndex.row()
        # 隐藏check_table表格的对应行
        check_table.hideRow(self.row_num)
        # 显示result_table的对应行
        result_table.showRow(self.row_num)
        # 设置状态图标
        self.status.setStyleSheet('''
                        QPushButton{
                        background-image:url('./images/YES.png');
                        border-radius:10px;
                        }
                        ''')

    # 设置rollback_btn的槽函数
    def click_on_rollback_btn(self, check_table, result_table):
        # 更加镜头检查状态
        self.checked = False
        # 如果镜头状态为通过，更改状态
        if self.apr:
            self.apr = False
        # 确定点击的按钮所在行
        (x, y) = (self.rollback_btn_widget.frameGeometry().x(), self.rollback_btn_widget.frameGeometry().y())
        self.tableIndex = result_table.indexAt(QPoint(x, y))
        self.row_num = self.tableIndex.row()
        # 隐藏result_table表格的对应行
        result_table.hideRow(self.row_num)
        # 显示check_table的对应行
        check_table.showRow(self.row_num)

    def view_feedback_dialog(self):
        fb_view = ViewFeedbackDialog(fb=self.fb,eps=self.eps,shot=self.shot+'('+self.version+')')
        fb_view.exec_()

    def view_last_feedback_dialog(self):
        fb_view = ViewLastFeedbackDialog(fb=self.last_fb,eps=self.eps,shot=self.shot+'('+self.version+')',artist=self.artiest)
        fb_view.exec_()

    # retake按钮的槽函数，绑定子窗口中的自定义信号与实例的槽函数
    def on_click_retake_btn(self):
        retake_dialog = CreateFeedbackDialog(eps=self.eps,shot=self.shot,artist=self.artiest)
        retake_dialog.customSignal.connect(partial(self.set_feedback,self.check_table,self.result_table))
        retake_dialog.exec_()

    # 用于获取反馈信息的函数,获取反馈信息后将镜头发送到result表格显示
    def set_feedback(self,check_table,result_table,feedback):
        self.fb = feedback
        # 设置镜头检查状态
        self.checked = True
        # 更改镜头通过状态
        self.apr = False
        # 确定改镜头项所在行
        (x, y) = (self.apr_btn_widget.frameGeometry().x(), self.apr_btn_widget.frameGeometry().y())
        self.tableIndex = check_table.indexAt(QPoint(x, y))
        self.row_num = self.tableIndex.row()
        # 隐藏check_table表格的对应行
        check_table.hideRow(self.row_num)
        # 显示result_table的对应行
        result_table.showRow(self.row_num)
        # 设置result_table中的图标状态
        self.status.setStyleSheet('''
                QPushButton{
                background-image:url('./images/retake.png');
                border-radius:10px;
                }
                ''')

    def test_btn(self):
        print('OK')

