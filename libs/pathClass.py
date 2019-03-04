# -*- coding:utf-8 -*-

import os
# 管理路径的类
class PathClass():
    def __init__(self):
        self.dataPath = r'C:/HOME/.nuke/data'
        self.iconPath = r'Y:/DA/nuke/GYTools/GY_Checker/images'
        self.last_fb_img_path = r'C:/HOME/.nuke/last_fb_img'
        self.fb_img_path = r'C:/HOME/.nuke/fb_img'

if __name__ == '__main__':
    test = PathClass()
    os.startfile(test.iconPath)
    print(test.iconPath)
