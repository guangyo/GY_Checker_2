# -*- coding:utf-8 -*-

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import sys, test_data

class UI_Main(QTabWidget):
    def __init__(self,parent = None):
        super(UI_Main, self).__init__(parent)
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

        # 创建Submit按钮
        self.submitButton = QPushButton('SUBMIT')
        self.submitButton.setFont(QFont('Microsoft YaHei', 20))
        self.submitButton.setObjectName('submitButton')

        # inputButton 的样式QSS
        self.submitButton_style = '''
                                            #submitButton{
                                            border-radius:4px;background-color:rgb(185,111,2);color:white;
                                            border:1px solid rgb(125,125,125);
                                            }
                                            #submitButton:hover{
                                            border-radius:4px;background-color:rgb(223,134,3);color:white;
                                            }
                                            #submitButton:pressed{
                                            border-radius:4px;background-color:rgb(56,104,0);color:red;                 
                                            }
                                    '''
        # 设置submitButton的样式
        self.submitButton.setStyleSheet(self.submitButton_style)

        # 测试按钮槽函数
        self.inputButton.clicked.connect(self.test)

        # 创建checkPageTable
        self.checkPageTable = QTableWidget()
        self.checkPageTable.setObjectName('checkTable')

        # 设置check_page的初始排序bool值
        self.sort_upordown = True

        # 设置行列数据
        self.checkPageTable.setColumnCount(6)
        # 行数的数据根据导入的数据数量设置
        self.checkPageTable.setRowCount(len(test_data.testData.keys()))

        # 设置默认行高和每列的宽度
        # 设置表格宽度模式，暂时关闭时为了让用户可以自行改变窗口每列宽度
        # self.checkPageTable.horizontalHeader().setSectionResizeMode(QHeaderView.Custom)
        self.checkPageTable.horizontalHeader().setStretchLastSection(True)
        self.checkPageTable.verticalHeader().setDefaultSectionSize(59)
        self.checkPageTable.setColumnWidth(0, 50)
        self.checkPageTable.setColumnWidth(1, 64)
        self.checkPageTable.setColumnWidth(2, 110)
        self.checkPageTable.setColumnWidth(3, 92)
        self.checkPageTable.setColumnWidth(4, 70)
        self.checkPageTable.setColumnWidth(5, 71)

        # 设置表格格式
        # checkTable的样式表
        self.checkPageTableStyle = '''
                                                   QTableWidget
                                                   {
                                                   background-color:black;
                                                   font:14px 'Microsoft YaHei';
                                                   text-align:center;
                                                   color:rgb(255,255,255);                                   
                                                   gridline-color:rgb(90,90,90);
                                                   }                        
                                                   QTableWidget::item:selected
                                                   {
                                                   background-color:rgb(71,71,71);
                                                   }
                                                   QHeaderView::section
                                                   {                                            
                                                   background-color:black;
                                                   font:14px 'Microsoft YaHei';
                                                   color:red;
                                                   border:1.5px solid rgb(110,110,110);
                                                   border-left:none;
                                                   }
                                                   QHeaderView::section:hover
                                                   {                                            
                                                   background-color:rgb(54,12,4);
                                                   font:14px 'Microsoft YaHei';
                                                   color:rgb(168,168,168);                                                   
                                                   }                                                           
                                                   '''
        # 设置垂直表头不可见
        self.checkPageTable.verticalHeader().setVisible(False)
        # 单击选中一行
        self.checkPageTable.setSelectionBehavior(QAbstractItemView.SelectRows)

        # 使用style
        self.checkPageTable.setStyleSheet(self.checkPageTableStyle)

        # 设置不可编辑
        self.checkPageTable.setEditTriggers(QAbstractItemView.NoEditTriggers)

        # 取消表头的选中高亮
        self.checkPageTable.horizontalHeader().setHighlightSections(False)

        # 设置表头高度
        self.checkPageTable.horizontalHeader().setFixedHeight(30)

        # 设置垂直滚动条样式
        self.checkPageTable.verticalScrollBar().setStyleSheet('''
                QScrollBar{background:rgb(108,108,108); width:17px; }
                QScrollBar::handle{background:rgb(150,0,6);border-radius:5px;}    
                QScrollBar::handle:hover{background:rgb(125,0,4); }
                QScrollBar::add-page:vertical,QScrollBar::sub-page:vertical{background:rgb(108,108,108);}
                ''')

        # 设置表头数据
        self.checkPageTable.setHorizontalHeaderLabels(['', 'EPS', 'SHOTS', 'ARTIEST', 'LAST_FB', ''])
        # 设置表头单击后的对齐方式
        self.checkPageTable.horizontalHeader().sectionClicked.connect(self.onHeaderClicked)

        # 数据导入
        self.check_id_list = []
        self.check_data = test_data.testData
        self.import_table_value()

        self.checkPageUI()

    # 设置checkPage
    def checkPageUI(self):
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignTop)
        layout.setSpacing(0)

        # 添加布局
        layout.addWidget(self.inputButton)
        layout.addWidget(self.checkPageTable)
        layout.addWidget(self.submitButton)
        self.checkPage.setLayout(layout)

    def test(self):
        print('Hello Billy')

    def import_table_value(self):
        self.check_id_list = sorted(self.check_data.keys())
        for i in range(len(self.check_data.keys())):
            for j in [1,2,3]:
                eps_item = QTableWidgetItem(self.check_data[self.check_id_list[i]]['eps'])
                eps_item.setTextAlignment(Qt.AlignCenter)
                shot_item = QTableWidgetItem(self.check_data[self.check_id_list[i]]['shot']+
                            '('+self.check_data[self.check_id_list[i]]['version']+')')
                shot_item.setTextAlignment(Qt.AlignCenter)
                artiest_item = QTableWidgetItem(self.check_data[self.check_id_list[i]]['artiest'])
                artiest_item.setTextAlignment(Qt.AlignCenter)
                if j == 1:
                    self.checkPageTable.setItem(i, j, eps_item)
                elif j == 2:
                    self.checkPageTable.setItem(i, j, shot_item)
                else:
                    self.checkPageTable.setItem(i, j, artiest_item)

    # 根据点击的表头设置相应的排序方式
    def onHeaderClicked(self,index):
        if self.sort_upordown:
            self.checkPageTable.sortItems(index,Qt.AscendingOrder)
            self.sort_upordown = False
        else:
            self.checkPageTable.sortItems(index, Qt.DescendingOrder)
            self.sort_upordown = True


if __name__ == '__main__':
    app = QApplication(sys.argv)
    demo = UI_Main()
    demo.show()
    sys.exit(app.exec_())