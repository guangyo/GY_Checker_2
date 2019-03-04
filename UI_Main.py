# -*- coding:utf-8 -*-

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *
from libs.checkShotClass import *
from libs.checkPageTable import *
from libs.resultPageTable import *
from libs.submitDialog import *
from libs.inputDialog import *
from libs.cgtw_control import *
import sys,json,shutil


class UI_Main(QTabWidget):
    def __init__(self,parent = None):
        super(UI_Main, self).__init__(parent)
        # input窗口
        self.inputWin = None
        # 设置Tab的样式
        self.setStyleSheet('''QTabBar::tab{
                                font:12px 'Microsoft YaHei';
                                width:245;
                                height:18;
                                color:white;
                                background-color:rgb(45,45,45);
                                border:1px solid rgb(85,85,85);
                                }
                                QTabBar::tab:hover{
                                background-color:rgb(125,5,0);
                                }
                                QTabBar::tab:selected{
                                background-color:rgb(125,5,0);
                                }'''
                           )
        self.setMinimumSize(500,800)
        self.setMaximumWidth(1000)
        self.setWindowTitle('GY_Cherker_Main_window')

        # 创建检查和结果页面
        self.checkPage = QWidget()
        self.checkPage.setObjectName('checkPage')
        self.resultPage = QWidget()
        self.checkPage.setStyleSheet('#checkPage{background-color:black;}')

        self.addTab(self.checkPage,'Check_page')
        self.addTab(self.resultPage,'Result_page')

        # 创建Input按钮
        self.inputButton = QPushButton('INPUT')
        self.inputButton.setFont(QFont('Microsoft YaHei',20))
        self.inputButton.setObjectName('inputButton')

        # inputButton 的样式QSS
        self.inputButton_style = '''
                                    #inputButton{
                                    border-radius:4px;background-color:rgb(56,104,0);color:white;
                                    border:1px solid rgb(125,125,125);
                                    }
                                    #inputButton:hover{
                                    border-radius:4px;background-color:rgb(105,195,0);color:white;
                                    }
                                    #inputButton:pressed{
                                    border-radius:4px;background-color:rgb(56,104,0);color:red;                 
                                    }
                                '''
        # 设置InputButton的样式
        self.inputButton.setStyleSheet(self.inputButton_style)

        # 创建两个窗口的Submit按钮
        self.submitButton = QPushButton('SUBMIT')
        self.submitButton.setFont(QFont('Microsoft YaHei', 20))

        self.submitButton2 = QPushButton('SUBMIT')
        self.submitButton2.setFont(QFont('Microsoft YaHei', 20))

        # submitButton 的样式QSS
        self.submitButton_style = '''
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
        # 设置submitButton的样式
        self.submitButton.setStyleSheet(self.submitButton_style)
        self.submitButton2.setStyleSheet(self.submitButton_style)

        # 创建checkPageTable
        self.checkPageTable = CheckPageTable()

        # 创建resultPageTable
        self.resultPageTable = ResultPageTable()

        # 设置表头单击后的对齐方式
        self.checkPageTable.horizontalHeader().sectionClicked.connect(self.onChecktableHeaderClicked)
        self.resultPageTable.horizontalHeader().sectionClicked.connect(self.onChecktableHeaderClicked)

        # 数据导入
        # 创建待检查镜头字典，用于存放待检查镜头的实例
        self.checkshot_dict = {}
        # 设置镜头ID迭代
        self.shot_id_item = 0

        self.check_data = None

        # 将表格放入如布局
        self.checkPageUI()
        self.resultPageUI()

        # 导入数据
        # self.import_table_value()

        # 连接槽函数
        # 测试按钮槽函数
        self.inputButton.clicked.connect(self.onInputButtonClicked)
        self.submitButton.clicked.connect(self.onClickSubmitButton)
        self.submitButton2.clicked.connect(self.onClickSubmitButton)

    # 设置checkPage
    def checkPageUI(self):
        layout1 = QVBoxLayout()
        layout1.setAlignment(Qt.AlignTop)
        layout1.setContentsMargins(0,0,0,0)
        layout1.setSpacing(0)

        # 添加布局
        layout1.addWidget(self.inputButton)
        layout1.addWidget(self.checkPageTable)
        layout1.addWidget(self.submitButton)
        self.checkPage.setLayout(layout1)

    def resultPageUI(self):
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignTop)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        layout.setSpacing(0)

        # 添加布局
        layout.addWidget(self.resultPageTable)
        layout.addWidget(self.submitButton2)
        self.resultPage.setLayout(layout)

    def test(self):
        print('Hello Billy')

    def import_table_value(self):
        # 从json文件获取DATA
        with open(r'C:/HOME/.nuke/data/data_from_cgtw.json', 'r') as f:
            data = f.read()
        self.check_data = json.loads(data)
        self.checkPageTable.setRowCount(len(self.check_data))
        self.resultPageTable.setRowCount(len(self.check_data))

        for i in range(len(self.check_data)):
            self.shot_id_item = i
            for j in range(6):
                # 将实例对象的数据填入表格
                if j == 0:
                    # 实例化CheckShot并放入checkshot_dict中方便调用
                    # print(self.check_data[i]['eps'])
                    # print
                    self.checkshot_dict['shot' + str(self.shot_id_item)] = CheckShot(self.shot_id_item,
                                                                                     self.check_data[i]['project'],
                                                                                     self.check_data[i]['eps'],
                                                                                     self.check_data[i]['shot'],
                                                                                     self.check_data[i]['version'],
                                                                                     self.check_data[i]['artist'],
                                                                                     self.check_data[i]['last_fb'],
                                                                                     self.check_data[i]['file_path'],
                                                                                     self.checkPageTable,
                                                                                     self.resultPageTable
                                                                                     )

                    self.checkPageTable.setCellWidget(i, j, self.checkshot_dict['shot' + str(self.shot_id_item)].
                                                      apr_btn_widget)
                    self.resultPageTable.setCellWidget(i, j, self.checkshot_dict['shot' + str(self.shot_id_item)].
                                                       status_widget)

                elif j == 1:
                    self.checkPageTable.setItem(i, j, self.checkshot_dict['shot'+str(self.shot_id_item)].eps_item)
                    self.resultPageTable.setItem(i, j, self.checkshot_dict['shot' + str(self.shot_id_item)].eps_item2)
                elif j == 2:
                    self.checkPageTable.setItem(i, j, self.checkshot_dict['shot'+str(self.shot_id_item)].shot_item)
                    self.resultPageTable.setItem(i, j, self.checkshot_dict['shot' + str(self.shot_id_item)].shot_item2)
                elif j == 3:
                    self.checkPageTable.setItem(i, j, self.checkshot_dict['shot'+str(self.shot_id_item)].artiest_item)
                    self.resultPageTable.setItem(i, j, self.checkshot_dict['shot' + str(self.shot_id_item)].artiest_item2)
                elif j == 4:
                    self.checkPageTable.setCellWidget(i, j, self.checkshot_dict['shot' + str(self.shot_id_item)].
                                                      view_last_fb_btn_widget)
                    self.resultPageTable.setCellWidget(i, j, self.checkshot_dict['shot' + str(self.shot_id_item)].
                                                       view_fb_btn_widget)
                elif j == 5:
                    self.checkPageTable.setCellWidget(i, j, self.checkshot_dict['shot' + str(self.shot_id_item)].
                                                      retake_btn_widget)
                    self.resultPageTable.setCellWidget(i, j, self.checkshot_dict['shot' + str(self.shot_id_item)].
                                                       rollback_btn_widget)
            # 初始隐藏所有resultPageTable中的项目
            self.resultPageTable.hideRow(i)
        # 表格填完之后设置默认状态根据eps正序排布
        self.checkPageTable.sortItems(1, Qt.AscendingOrder)
        self.resultPageTable.sortItems(1, Qt.AscendingOrder)

    # 根据点击的表头设置相应的排序方式
    def onChecktableHeaderClicked(self,index):
        if self.checkPageTable.sort_upordown:
            self.checkPageTable.sortItems(index,Qt.AscendingOrder)
            self.resultPageTable.sortItems(index,Qt.AscendingOrder)
            self.checkPageTable.sort_upordown = False
        else:
            self.checkPageTable.sortItems(index, Qt.DescendingOrder)
            self.resultPageTable.sortItems(index, Qt.DescendingOrder)
            self.checkPageTable.sort_upordown = True

    def onClickSubmitButton(self):
        # submitDialog = SubmitDialog()
        # submitDialog.exec_()
        # 遍历所有待检查任务，对不同状态的任务做不同的处理
        for task in self.checkshot_dict.values():
            # 创建一个CGTW的控制实例
            cgtw_controler = CGTW_control(task.project,task.eps,task.shot,)
            # 镜头状态修改并更新反馈:
            if task.checked == True:
                # 从result表中隐藏所有要提交检查的镜头
                # 确定提交的task在表中的哪一行
                (x, y) = (task.rollback_btn_widget.frameGeometry().x(), task.rollback_btn_widget.frameGeometry().y())
                tableIndex = self.resultPageTable.indexAt(QPoint(x, y))
                row_num = tableIndex.row()
                # 镜头通过的情况
                if task.apr == True:
                    # 改变cgtw状态
                    cgtw_controler.update_shot_status('Publish')

                    # 将通过的文件复制到对应目录下
                    # 当前日期
                    cur_date = QDate.currentDate().toString('yyyyMMdd')
                    # 根据当前日期创建存放文件夹
                    to_client_file_path = r'Z:\GY_Project\%s\prd\to_client\%s\EP%s\%s' % (str(task.project),str(cur_date),str(task.eps),str(os.path.basename(task.file_path["file_path"])))
                    # 如果没有该路径，创建一个~
                    if not os.path.exists(os.path.dirname(to_client_file_path)):
                        os.makedirs(os.path.dirname(to_client_file_path))
                    # 拷贝文件到目标位置
                    shutil.copy2(task.file_path["file_path"],to_client_file_path)
                # 镜头没有通过的情况
                else:
                    # 镜头没有通过的
                    cgtw_controler.update_shot_status('Retake')
                    # 有文字反馈的情况
                    if task.fb['text'] != '':
                        # 有文字反馈但没有图片反馈的
                        if len(task.fb['pic']) == 0:
                            cgtw_controler.create_shot_note(task.fb['text'])
                        # 既有文字也有图片反馈的
                        else:
                            cgtw_controler.create_shot_note(task.fb['text'], task.fb['pic'])
                    # 没有文字反馈的情况
                    else:
                        # 没有文字，没有图片的
                        if len(task.fb['pic']) == 0:
                            pass
                        # 没有文字，有图片的
                        else:
                            cgtw_controler.create_shot_note(task.fb['text'], task.fb['pic'])
                    print('Retake!!')

                # 检查完毕后，删除对应行
                self.resultPageTable.removeRow(row_num)
                self.checkPageTable.removeRow(row_num)

                # 根据值获取对象字典的key
                key = list(self.checkshot_dict.keys())[list(self.checkshot_dict.values()).index(task)]

                # 删除对应的字典项
                del self.checkshot_dict[key]

                # 清除对应task的图片文件夹
                # 清除fb_img
                fb_path = r'./fb_img/%s/%s' % (task.eps,task.shot)
                if os.path.exists(fb_path):
                    shutil.rmtree(fb_path)
                # 清除last_fb_img
                last_fb_path = r'./last_fb_img/%s/%s' % ('EPS' + task.eps, task.shot)
                if os.path.exists(last_fb_path):
                    shutil.rmtree(last_fb_path)
            else:
                pass

    def onInputButtonClicked(self):
        self.setDisabled(True)
        self.inputWin = InputDialog(self)
        self.inputWin.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    demo = UI_Main()
    demo.show()
    sys.exit(app.exec_())