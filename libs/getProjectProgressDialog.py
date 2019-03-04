# -*- coding:utf-8 -*-
import sys,os
from PySide2.QtWidgets import *
from PySide2.QtCore import *
from PySide2.QtGui import *
sys.path.append(r"c:/cgteamwork/bin/base")
import cgtw


class GetProjectProgressDialog(QDialog):
    def __init__(self,parent = None):
        super(GetProjectProgressDialog, self).__init__(parent)
        self.parent_win = parent
        # 获取CGTeamWork的实例,用于操作teamwork数据
        self.t_tw = cgtw.tw()
        # 设置窗口样式(无标题)
        self.setWindowFlags(Qt.Dialog | Qt.FramelessWindowHint)

        self.label = QLabel('获取项目信息中...')
        self.label.setFont(QFont('Microsoft YaHei', 18))
        self.label.setStyleSheet('''QLabel{color:rgb(155,155,155)}''')
        self.label.setFixedSize(250,30)
        # 设置背景色
        self.setStyleSheet('''QDialog{background-color:black}''')
        # 创建进度条控件
        self.pbar = QProgressBar()

        # 创建时间对象(用于控制进度条)
        self.timer = QBasicTimer()
        self.step = 0

        self.resize(350,220)
        self.setWindowTitle('GETTING_PROJECTS...:')

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
        # 设置窗口对齐桌面正中
        # 获取屏幕坐标系
        screen = QDesktopWidget().screenGeometry()
        # 获取窗口坐标系
        size = self.geometry()
        newLeft = (screen.width() - size.width()) / 2
        newTop = (screen.height() - size.height()) / 2
        self.move(newLeft, newTop)
        self.initUI()
        # 连接父级窗口的信号
        # parent.progress_signal.connect(self.getEmi)

    def timerEvent(self, e):
        # 进度条停止条件
        if self.step >= 100:
            self.timer.stop()
            self.setWindowTitle('完成')
            # 进度条走完关闭窗口~
            self.accept()
            return

        # 获取项目列表
        self.parent_win.proj_list = ['-SELECT-']
        project_dict = self.t_tw.info_module('public', 'project').get_with_filter(['project.database'],
                                                                                  [['project.status', '!=',
                                                                                    'Lost'], 'and',
                                                                                   ['project.status', '!=',
                                                                                    'Close']])

        for i in range(len(project_dict)):
            # 去除没有任务的项目：
            filter_module = self.t_tw.task_module(project_dict[i]['project.database'], 'shot')
            check_shot_list = filter_module.get_with_filter(['shot.shot'], [['task.pipeline', '=', 'cmp'],
                                                                            'and',
                                                                            ['task.remaining_day', '=', '0']])
            if len(check_shot_list) > 0:
                self.parent_win.proj_list.append(project_dict[i]['project.database'][5:])
            self.step = (float(i)/(len(project_dict)-1))*100
            self.pbar.setValue(self.step)
            self.label.setText('获取项目信息中...%d' % self.step + '%')

    def initUI(self):
        self.timer.start(100,self)

    def getEmi(self,pro):
        print(pro)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    demo = GetProjectProgressDialog()
    demo.show()
    sys.exit(app.exec_())
