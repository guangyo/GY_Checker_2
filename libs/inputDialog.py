# -*- coding:utf-8 -*-

import sys,os
from PySide2.QtWidgets import *
from PySide2.QtCore import *
from PySide2.QtGui import *
from libs.getProjectProgressDialog import *
from libs.cgtw_control import *
from libs.pathClass import *
sys.path.append(r"c:/cgteamwork/bin/base")
import cgtw, re, json


class InputDialog(QDialog):
    progress_signal = Signal(int)

    def __init__(self,parent=None,):
        super(InputDialog, self).__init__(parent)
        # 设置窗口样式(无标题)
        self.setWindowFlags(Qt.Dialog | Qt.FramelessWindowHint)

        # debug参数
        self.debug1 = 0
        self.debug2 = 0
        self.debug3 = 0

        # 创建一个路径对象,用于设置引用路径
        self.path_obj = PathClass()

        # 设置默认参数
        self.proj_list = ['-select-']
        self.eps_list = ['-ALL-']

        # 获取CGTeamWork的实例,用于操作teamwork数据
        self.t_tw = cgtw.tw()

        # 设置表头显示样式
        self.setWindowFlags(Qt.Dialog | Qt.WindowCloseButtonHint)
        self.setWindowTitle('InputDialog:')
        # 设置默认大小
        self.resize(500,250)
        # 设置背景色
        self.setStyleSheet('''QDialog{background-color:black}''')

        # 创建所有要使用的控件

        self.head_label = QLabel('请选择要检查的项目')
        self.head_label.setFont(QFont('Microsoft YaHei', 18, QFont.Bold))
        self.head_label.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.head_label.setStyleSheet('''QLabel{color:red}''')

        self.proj_label = QLabel('PRO:')
        self.proj_label.setStyleSheet('''QLabel{color:red}''')
        self.proj_label.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.proj_label.setFont(QFont('Microsoft YaHei', 16))

        self.proj_combo = QComboBox()
        self.comboStyle = '''QComboBox{font-size:16px;
                             color:white;
                             border-radius:4;
                             background-color:grey;
                             font-family:Microsoft YaHei;
                             selection-background-color:grey;
                             }
                             QComboBox::drop-down{
                             image:url(%s/arrow_down_2.png);
                             }
                             QComboBox QAbstractItemView{
                             color:white;
                             background-color:grey;
                             selection-background-color:rgb(159,5,11);
                             selection-color:white;
                             }''' % self.path_obj.iconPath
        self.proj_combo.setStyleSheet(self.comboStyle)

        self.eps_label = QLabel('EPS:')
        self.eps_label.setStyleSheet('''QLabel{color:red}''')
        self.eps_label.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.eps_label.setFont(QFont('Microsoft YaHei', 16))

        self.eps_combo = QComboBox()
        self.eps_combo.setStyleSheet(self.comboStyle)

        self.line = QFrame()
        self.line.setFrameShape(QFrame.HLine)
        self.line.setLineWidth(2)
        self.line.setStyleSheet('''QFrame{color:rgb(127,127,127)}''')

        # 创建底部的INPUT按钮
        self.inputButton = QPushButton('INPUT')
        self.inputButton.setFont(QFont('Microsoft YaHei', 20))

        # inputButton 的样式QSS
        self.inputButton_style = '''
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
        self.inputButton.setStyleSheet(self.inputButton_style)

        # 设置鼠标滑过时的鼠标形状
        self.inputButton.setCursor(Qt.PointingHandCursor)

        # 绑定底部按钮的槽函数
        self.inputButton.clicked.connect(self.onInputButtonClicked)

        # 创建布局
        # 整体布局
        self.main_layout = QVBoxLayout()
        self.main_layout.setContentsMargins(0, 4, 0, 0)
        # 用于显示project和eps信息的布局
        self.combo_layout = QGridLayout()
        # 右侧总体纵布局
        self.info_layout = QVBoxLayout()
        # 中间左侧面板
        self.midLeftWidget = QWidget()
        # 中间部分的spliter可拖动边界
        self.splitter = QSplitter(Qt.Horizontal)
        self.splitter.setHandleWidth(2)
        self.splitter.setStyleSheet('''QSplitter:handle{background-color:black}''')

        # 中间右侧面板
        self.midRightWidget = QWidget()
        # 中间右侧面板的组件
        self.totalCheckLabel = QLabel('今日任务总数:')
        self.totalCheckLabel.setStyleSheet('''QLabel{color:rgb(178,178,178)}''')
        self.totalCheckLabel.setFont(QFont('Microsoft YaHei', 10, QFont.Bold))

        self.waitingForChecker = QLabel('待检查任务总数:')
        self.waitingForChecker.setStyleSheet('''QLabel{color:rgb(178,178,178)}''')
        self.waitingForChecker.setFont(QFont('Microsoft YaHei', 10, QFont.Bold))

        self.totalCheckValue = QLabel('...')
        self.totalCheckValue.setStyleSheet('''QLabel{color:rgb(255,0,9)}''')
        self.totalCheckValue.setFont(QFont('Microsoft YaHei', 18, QFont.Bold))

        self.waitingCheckerValue = QLabel('...')
        self.waitingCheckerValue.setStyleSheet('''QLabel{color:rgb(255,152,0)}''')
        self.waitingCheckerValue.setFont(QFont('Microsoft YaHei', 18, QFont.Bold))

        self.aprCheckLabel = QLabel('已通过任务总数:')
        self.aprCheckLabel.setStyleSheet('''QLabel{color:rgb(178,178,178)}''')
        self.aprCheckLabel.setFont(QFont('Microsoft YaHei', 10, QFont.Bold))

        self.aprCheckerValue = QLabel('...')
        self.aprCheckerValue.setStyleSheet('''QLabel{color:rgb(124,227,4)}''')
        self.aprCheckerValue.setFont(QFont('Microsoft YaHei', 18, QFont.Bold))

        # 默认状态下隐藏EPS选项
        self.eps_label.setHidden(True)
        self.eps_combo.setHidden(True)

        # 设置project设置的初始值，用于判定是否设置了project，一旦选择了项目，就把第一个-select-选项去除
        self.proj_set_index = 0

        self.initUI()

        self.proj_combo.currentIndexChanged.connect(self.onProjectChange)
        self.eps_combo.currentIndexChanged.connect(self.onEpsChanged)

    def initUI(self):
        # 用teamwork数据填充project_list
        # 因为检查任务时间稍长，显示进度条
        self.waitingBar = GetProjectProgressDialog(self)
        self.waitingBar.exec_()
        # 填充布局
        self.combo_layout.setSpacing(20)
        self.combo_layout.addWidget(self.proj_label, 0, 0)
        self.combo_layout.addWidget(self.proj_combo, 0, 1)
        self.combo_layout.addWidget(self.eps_label, 1, 0)
        self.combo_layout.addWidget(self.eps_combo, 1, 1)
        self.midLeftWidget.setLayout(self.combo_layout)

        self.info_layout.addWidget(self.totalCheckLabel,0,Qt.AlignHCenter)
        self.info_layout.addWidget(self.totalCheckValue, 0, Qt.AlignHCenter)
        self.info_layout.addWidget(self.waitingForChecker, 0, Qt.AlignHCenter)
        self.info_layout.addWidget(self.waitingCheckerValue, 0, Qt.AlignHCenter)
        self.info_layout.addWidget(self.aprCheckLabel, 0, Qt.AlignHCenter)
        self.info_layout.addWidget(self.aprCheckerValue, 0, Qt.AlignHCenter)
        self.info_layout.setSpacing(0)
        self.midRightWidget.setLayout(self.info_layout)

        self.splitter.addWidget(self.midLeftWidget)
        self.splitter.addWidget(self.midRightWidget)
        self.splitter.setContentsMargins(0,0,0,0)

        self.main_layout.addWidget(self.head_label,0,Qt.AlignHCenter)
        self.main_layout.addWidget(self.line)
        self.main_layout.addWidget(self.splitter)
        self.main_layout.addWidget(self.inputButton)
        self.main_layout.setSpacing(0)

        # 填充combo组件
        self.proj_combo.addItems(self.proj_list)
        self.eps_combo.addItems(self.eps_list)

        self.setLayout(self.main_layout)

    def onProjectChange(self,index):
        # 记录Project更改的次数
        self.proj_set_index += 1
        # 第一次选择项目后把默认的-select-选项去除
        if self.proj_combo.currentIndex() != 0 and self.proj_set_index == 1:
            # 为了避免重复刷新,首先断开EPS的槽函数连接,对EPS的选项更新完毕之后再重新连接
            self.eps_combo.currentIndexChanged.disconnect(self.onEpsChanged)
            # 刷新右侧面板信息
            self.refreshCheckInfo()
            # 去除默认选项
            self.proj_combo.removeItem(0)
            # 显示eps选项
            self.eps_label.setHidden(False)
            self.eps_combo.setHidden(False)
            # 根据选择的项目刷新集数信息
            self.eps_combo.clear()
            self.eps_combo.addItems(self.eps_list)
            # 重新连接槽函数
            self.eps_combo.currentIndexChanged.connect(self.onEpsChanged)

        # 当选择的项目变化时，重新装载集数信息
        elif self.proj_combo.currentText() != '-SELECT-' and self.proj_set_index > 2:
            # 为了避免重复刷新,首先断开EPS的槽函数连接,对EPS的选项更新完毕之后再重新连接
            self.eps_combo.currentIndexChanged.disconnect(self.onEpsChanged)
            # 刷新右侧面板信息
            self.refreshCheckInfo()
            # 刷新集数信息
            self.eps_combo.clear()
            self.eps_combo.addItems(self.eps_list)
            # 重新连接槽函数
            self.eps_combo.currentIndexChanged.connect(self.onEpsChanged)

    # 定义当集数信息改变时刷新右侧面板信息
    def onEpsChanged(self):
        self.debug1 += 1
        self.refreshCheckInfo()
        return self.proj_list

    # 根据选择的项目信息刷新右侧面板的信息
    def refreshCheckInfo(self):
        filter_module = self.t_tw.task_module('proj_'+self.proj_combo.currentText(), 'shot')
        total_filter_func_list = [['task.task_name', '=', 'cmp'], 'and', ['task.remaining_day', '=', '0']]
        check_filter_func_list = [['task.task_name','=','cmp'],'and', ['task.status','=','Check'],'and',
                                  ['task.leader_status', '!=', 'Publish'],
                                   'and',['task.remaining_day','=','0']]
        publish_filter_func_list = [['task.task_name', '=', 'cmp'], 'and', ['task.leader_status', '=', 'Publish'],
                                  'and', ['task.remaining_day', '=', '0']]

        if self.eps_combo.currentText() != '-ALL-' and self.sender() == self.eps_combo:
            total_filter_func_list.extend(['and', ['eps.eps_name', '=', '%s' % self.eps_combo.currentText()]])
            check_filter_func_list.extend(['and', ['eps.eps_name', '=', '%s' % self.eps_combo.currentText()]])
            publish_filter_func_list.extend(['and', ['eps.eps_name', '=', '%s' % self.eps_combo.currentText()]])

        total_check_shot_list = filter_module.get_with_filter(['shot.shot','eps.eps_name'],total_filter_func_list)
        ready_check_shot_list = filter_module.get_with_filter(['shot.shot','eps.eps_name'],check_filter_func_list)
        publish_shot_list = filter_module.get_with_filter(['shot.shot','eps.eps_name'],publish_filter_func_list)

        total_check_shot_num = len(total_check_shot_list)
        ready_check_shot_num = len(ready_check_shot_list)
        publish_shot_num = len(publish_shot_list)

        self.totalCheckValue.setText(str(total_check_shot_num))
        self.waitingCheckerValue.setText(str(ready_check_shot_num))
        self.aprCheckerValue.setText(str(publish_shot_num))

        # 当项目更新时更新集数信息
        if self.sender() == self.proj_combo:
            self.debug2 += 1

            self.eps_list = ['-ALL-']
            # 把有检查任务的集数挑选出来，放入combo选项中，避免无效选项
            check_eps_list = []
            for i in total_check_shot_list:
                check_eps_list.append(i['eps.eps_name'])
            # 去重
            check_eps_list = list(set(check_eps_list))
            # 刷新集数信息
            for i in check_eps_list:
                self.eps_list.append(i)

    def closeEvent(self, QCloseEvent):
        # 解除父窗口不可用状态
        self.parent().setDisabled(False)

    def onInputButtonClicked(self):
        # 解除父窗口不可用状态
        self.parent().setDisabled(False)
        # 获取检查数据
        self.getCheckData()
        # 父窗口装载数据
        self.parent().import_table_value()
        # 关闭子窗口
        self.accept()

    def getCheckData(self):
        # 用于装填所有检查数据的列表
        dataList = list()
        # 用于匹配版本信息
        vernum_check = re.compile(r'v\d{3,6}', re.IGNORECASE)
        filter_module = self.t_tw.task_module('proj_' + self.proj_combo.currentText(), 'shot')
        check_filter_func_list = [['task.task_name', '=', 'cmp'], 'and', ['task.status', '=', 'Check'],
                                  'and', ['task.leader_status', '!=', 'Publish'],
                                  'and', ['task.remaining_day', '=', '0']]
        if self.eps_combo.currentText() != '-ALL-':
            check_filter_func_list.extend(['and', ['eps.eps_name', '=', '%s' % self.eps_combo.currentText()]])

        ready_check_shot_list = filter_module.get_with_filter(['shot.shot', 'eps.eps_name','task.artist'], check_filter_func_list)

        # 获取数据
        for i in range(len(ready_check_shot_list)):
            cgtw_control = CGTW_control(self.proj_combo.currentText(), ready_check_shot_list[i]['eps.eps_name'],
                                        ready_check_shot_list[i]['shot.shot'])
            temp_dict = dict()
            temp_dict['project'] = self.proj_combo.currentText()
            temp_dict['eps'] = ready_check_shot_list[i]['eps.eps_name']
            temp_dict['shot'] = ready_check_shot_list[i]['shot.shot']
            temp_dict['file_path'] = cgtw_control.get_final_check_path()
            temp_dict['version'] = vernum_check.findall(temp_dict['file_path']['check_file'])[0]
            temp_dict['artist'] = ready_check_shot_list[i]['task.artist']
            fb_image_path = os.path.join('%s/last_fb_img' % self.path_obj.last_fb_img_path, 'EPS' + temp_dict['eps'], temp_dict['shot'])
            temp_dict['last_fb'] = cgtw_control.get_shot_note(-1, fb_image_path)
            dataList.append(temp_dict)

        # 将数据写入json文件
        if not os.path.exists(self.path_obj.dataPath):
            os.makedirs(self.path_obj.dataPath)
        json_file_path = r'C:/HOME/.nuke/data/data_from_cgtw.json'
        data = json.dumps(dataList)
        with open(json_file_path, 'w') as f:
            f.write(data)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    demo = InputDialog()
    demo.show()
    sys.exit(app.exec_())