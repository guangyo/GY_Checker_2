# -*- coding:utf-8 -*-

from PySide2.QtWidgets import *
from data.test_data import *


class ResultPageTable(QTableWidget):
    def __init__(self,parent =None):
        super(ResultPageTable, self).__init__(parent)
        self.setObjectName('checkTable')
        # 设置result_page的初始排序bool值
        self.sort_upordown = False

        # 设置行列数据
        self.setColumnCount(6)
        # self.setRowCount(len(testData))

        # 设置默认行高和每列的宽度
        # 设置表格宽度模式，暂时关闭是为了让用户可以自行改变窗口每列宽度
        # self.resultPageTable.horizontalHeader().setSectionResizeMode(QHeaderView.Custom)
        self.horizontalHeader().setStretchLastSection(True)
        self.verticalHeader().setDefaultSectionSize(59)
        self.setColumnWidth(0, 60)
        self.setColumnWidth(1, 50)
        self.setColumnWidth(2, 100)
        self.setColumnWidth(3, 92)
        self.setColumnWidth(4, 85)
        self.setColumnWidth(5, 68)

        # 设置表格格式
        # checkTable的样式表
        self.resultPageTableStyle = '''
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
        self.verticalHeader().setVisible(False)
        # 单击选中一行
        self.setSelectionBehavior(QAbstractItemView.SelectRows)

        # 使用style
        self.setStyleSheet(self.resultPageTableStyle)

        # 设置不可编辑
        self.setEditTriggers(QAbstractItemView.NoEditTriggers)

        # 取消表头的选中高亮
        self.horizontalHeader().setHighlightSections(False)

        # 设置表头高度
        self.horizontalHeader().setFixedHeight(30)

        # 设置垂直滚动条样式
        self.verticalScrollBar().setStyleSheet('''
                        QScrollBar{background:rgb(108,108,108); width:17px; }
                        QScrollBar::handle{background:rgb(150,0,6);border-radius:5px;}    
                        QScrollBar::handle:hover{background:rgb(125,0,4); }
                        QScrollBar::add-page:vertical,QScrollBar::sub-page:vertical{background:rgb(108,108,108);}
                        ''')

        # 设置表头数据
        self.setHorizontalHeaderLabels(['STATUS', 'EPS', 'SHOTS', 'ARTIEST', 'FEED_BACK', ''])