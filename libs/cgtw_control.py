# coding=utf-8
#!/usr/bin/env python

import sys
reload(sys)
sys.setdefaultencoding('utf8')
sys.path.append(r"C:/cgteamwork/bin/base")
sys.path.append(r"C:\cgteamwork\bin\cgtw\ct")
import cgtw2
from ct_http import ct_http

import os.path


class CGTW_control:
    """
    Warning: 这个class 使用的是cgtw2
    """
    def __init__(self, project, eps, shot_name,task_name = 'cmp'):
        self.project = project
        self.eps = eps
        self.shot_name = shot_name
        self.task_name = task_name
        self.project_dm = "proj_%s" % self.project
        # login
        self.t_tw = cgtw2.tw("192.168.1.8", "zhangwq", "b332yu")
        self.task_id = self.t_tw.task.get_id(self.project_dm, 'shot',
                                         [["shot.shot", "=", self.shot_name], 'and', ['shot.eps_name', '=', self.eps],
                                          'and', ["task.task_name", '=', self.task_name]])

    def update_shot_status(self, status):
        """
        :param status:  组长状态， 例如， Publish， Check， Retake
        :return: 修改组长状态
        """
        # cgtw login

        # 获得镜头的id_list
        t_id_list = self.t_tw.task.get_id(self.project_dm, 'shot', [["eps.eps_name", "=", self.eps], "and",
                                                                    ["shot.shot", "=", self.shot_name], "and",
                                                                    ["task.task_name", "=", "cmp"]])

        # 更新镜头的组长状态
        result = self.t_tw.task.update_flow(self.project_dm, "shot", t_id_list[0], 'task.leader_status', str(status))

        return result

    def create_shot_note(self, fb_text, fb_pic_list=[]):
        """
        :param fb_text:  反馈的文字部分
        :param fb_pic_list: 反馈的图片部分， type is list
        :return:
        """

        # 获得镜头的id_list
        t_id_list = self.t_tw.task.get_id(self.project_dm, 'shot', [["eps.eps_name", "=", self.eps], "and",
                                                                    ["shot.shot", "=", self.shot_name], "and",
                                                                    ["task.task_name", "=", "cmp"]])

        # 创建镜头的note
        result = self.t_tw.note.create(self.project_dm, 'shot', 'task', t_id_list, fb_text, '', fb_pic_list)

        return result

    def get_shot_note(self, index, dst_path=None):
        """
        :param index:  第几条反馈， type is int， 0 是第一条， -1 是最后一条
        :param dst_path: 要存放图片的文件夹路径
        :return: 反馈的字典，type is dict, 键'text'是反馈的文字部分， 键'pic' 是 反馈的图片部分
        """
        note_id_list = self.t_tw.note.get_id(self.project_dm, [['module', '=', 'shot'], 'and', ['module_type', '=', 'task'], 'and' ,
                                                               ['#task_id','=',self.task_id[0]]])
        try:
            # 定义得到的反馈字典
            fb_dict = dict()

            result_list = self.t_tw.note.get(self.project_dm, [note_id_list[int(index)]], ['text'])

            # 得到的反馈字典
            get_fb_dict = eval(result_list[0]['text'])

            # 反馈的文字信息
            text_data = get_fb_dict['data']

            # 反馈字典的文字部分
            fb_dict['text'] = text_data

            # note内容的pic路径
            if len(get_fb_dict['image']) != 0:
                # 如果反馈包含有图片
                t_ip = self.t_tw.login.http_server_ip()
                t_token = self.t_tw.login.token()
                t_http = ct_http(t_ip, t_token)

                # 得到的图片路径列表
                src_pic_path_list = get_fb_dict['image']

                # 定义pic的列表
                fb_pic_list = []

                for i in range(len(src_pic_path_list)):
                    # 单个的src_pic 路径
                    src_pic_path = src_pic_path_list[i]['max']

                    # 文件格式
                    ext = os.path.splitext(src_pic_path)[1]

                    # 要保存的图片路径
                    new_name = "%s_%s_%s_%s%s" % (self.project, self.eps, self.shot_name, str(i), str(ext))
                    dst_full_path = os.path.join(dst_path, new_name)

                    # 添加到列表
                    fb_pic_list.append(dst_full_path)

                    # 从服务器下载到指定的路径
                    t_http.download(src_pic_path, dst_full_path)

                # 加到反馈字典里面
                fb_dict['pic'] = fb_pic_list
        except:
            pass

        return fb_dict

    def get_final_check_path(self):
        """
        得到check 文件的所在的位置以及 check的最后一版文件
        :return: dict， 键'file_path', 是文件所在的位置， 键'check_file' 是文件的名字
        """
        # 得到list_id
        t_id_list = self.t_tw.task.get_id(self.project_dm, 'shot', [["eps.eps_name", "=", self.eps], "and",
                                                                    ["shot.shot", "=", self.shot_name], "and",
                                                                    ["task.task_name", "=", "cmp"]])

        # 根据字段得到 列表
        submit_file_path_list = self.t_tw.task.get(self.project_dm, 'shot', t_id_list, ['task.submit_file_path'])

        # 定义字典
        file_msg_dict = dict()

        # 将unicode 转成字典
        try:
            temp_dict = eval(submit_file_path_list[0]['task.submit_file_path'])
            # 提交文件的路径
            checked_file_path = temp_dict['file_path'][0]
            # 提交的文件
            checked_file = os.path.split(checked_file_path)[1]

            # 写入字典
            file_msg_dict['file_path'] = checked_file_path
            file_msg_dict['check_file'] = checked_file
        except:
            temp_dict = dict()
            # 写入字典
            file_msg_dict['file_path'] = 'check_status_Error'
            file_msg_dict['check_file'] = 'check_status_Error'

        #print file_msg_dict

        return file_msg_dict


if __name__ == "__main__":
    content = '7、最后测试'
    pic_list = [r'D:\Python\progress_bar.png', r'D:\Python\qun.png']
    te = CGTW_control('fns2', '03', '003')
    #te.update_shot_status("Retake")
    #te.create_shot_note(content, pic_list)
    """
    a_dict = te.get_shot_note(-1, r'D:\test')
    print '----------'
    for each in a_dict:
        print each, a_dict[each]
    """
    print(te.get_final_check_path())