# -*- coding:utf-8 -*-
import hiero

def test():
    print 'hellow world'


class TimeLineControl(object):
    def __init__(self):
        self.version = '0.1'

    def find_shot(self, bin_name, eps, shot_name, rail_name):
        # 根据提供的集数和镜头号，打开对应的剪辑序列并且把时间针移动到该镜头的第一帧
        """
        :param bin_name: 剪辑线所处的文件夹的名字，type is string。 列如，01
        :param eps: 集数名， type is string
        :param shot_name: 镜头号 type is string
        :param rail_name: 轨道名， 想要得到那个轨道上的视频信息，用于确定checker或者lastVersion的位置， 一般默认是ORI
                            type is string
        :return:None
        """

        # 得到当前的Viewer
        old_viewer = hiero.ui.currentViewer()

        # 关闭旧的viewer
        old_viewer.window().close()

        # 得到当前的项目
        proj = hiero.core.projects()[-1]

        # sequence 所在的文件夹
        dst_bin = proj.bins(str(bin_name))[0]

        # 目标的sequence, type is BinItem
        dst_BinItem_seq = dst_bin.sequences()[0]

        # 打开Viewer
        current_viewer = hiero.ui.openInViewer(dst_BinItem_seq)

        # 得到EP%s % (eps)的sequence
        ep_sequence = hiero.core.findItemsInProject(proj, ['sequences'], 'EP%s' % eps, 1)[0]

        # 得到目标轨道的index
        i = 0
        dst_index = 0
        for each_track in ep_sequence:
            if str(rail_name) in each_track.name():
                dst_index = i
                i += 1
                break

        # 目标 轨道
        dst_video_track = ep_sequence.videoTrack(dst_index)

        # 定义 ORI的目标素材视频
        dst_shot_name = ''

        # 循环目标轨道
        for each_track_item in dst_video_track:
            if eps in each_track_item.name() and shot_name in each_track_item.name():
                # 得到要检测起始帧的镜头的名字
                dst_shot_name = each_track_item.name()

        # 在ORI轨道上的TrackItem
        ori_trackItem = hiero.core.findItemsInProject(proj, ['TrackItem'], dst_shot_name, 1)[0]

        # 创建的开始帧
        begin_frame = ori_trackItem.handleInTime()

        # 转到该镜头的起始帧
        current_viewer.setTime(int(begin_frame))

    def import_check_shots(self, check_dict):
        # 根据给定的待检查信息(dict),将对应镜头的最新版本导入相应时间线的对应位置
        # 注意：有上一版本的，需要在last_version轨道上放入上一版本的素材
        # 注意判断时间线的对应位置是否有上一次检查留下的素材(对比版本做相应处理)
        """

        :param check_dict:输入的字典
        check_dict['eps']:  集数
        check_dict['clip_name']:  clip_name 代表的是不带版本号的镜头名， 例：dza012231_cmp_liuwz_pre_v0101.mov， clip_name
                为 dza012231_cmp_liuwz_pre

        check_dict['full_path']:   完整路径
        check_dict['shot_name']：镜头号
        check_dict['version']: 当前的版本号

        :return:None
        """

        # 定义dst_bin
        dst_checker_Bin = ''

        # 得到当前的项目
        proj = hiero.core.projects()[-1]

        # 得到该镜头对应的checker文件夹
        bin_tuple = proj.bins('checker')

        # 循环包含‘checker’的 Bin tuple
        for each_Bin in bin_tuple:
            # 如果当前的bin文件夹的父文件夹在目标集数里
            if check_dict['eps'] in each_Bin.parentBin().name():
                # 得到目标文件夹
                dst_checker_Bin = each_Bin
                break

        # 判断给定的镜头是否存在, 返回是一个list
        find_result = hiero.core.findItemsInProject(proj, ['TrackItem'], check_dict['clip_name'], 1)

        # 如果存在
        if len(find_result):
            print 'current shot exists'
            # 存在的版本
            exist_version = find_result[0].currentVersion()

            # 如果版本不相等
            if check_dict['version'] not in exist_version.name():
                # 移除就版本
                exist_binItem = exist_version.parent()
                exist_binItem.parentBin().removeItem(exist_binItem)

                # 导入并在checker轨道创建 新版本
                self.add_shot_to_checker_rail(check_dict, dst_checker_Bin, proj, 'checker')

            else:
                # 如果相等
                pass

        # 如果不存在
        else:
            print 'current shot does not exist and will be created.'

            self.add_shot_to_checker_rail(check_dict, dst_checker_Bin, proj, 'checker')

    def add_shot_to_checker_rail(self, check_dict, dst_Bin, proj, rail_name):
        """
        将当前镜头加到 对应的文件夹和轨道上
        :param check_dict: 给定的字典， 跟 import_check_shots 函数的check_dict应该保持一样
        :param dst_Bin: 对应的checker 文件夹, type is hiero.core.Bin
        :param proj: 当前的项目, type is hiero.core.project
        :param rail_name: 目标轨道的名字， type is string
        :return:None
        """
        # 导入mov
        source1 = hiero.core.MediaSource(check_dict['full_path'])

        # 创建clip
        clip1 = hiero.core.Clip(source1)

        # 添加到指定的文件夹
        binItem_add = dst_Bin.addItem(hiero.core.BinItem(clip1))

        # 得到EP%s % (eps)的sequence
        ep_sequence = hiero.core.findItemsInProject(proj, ['sequences'], 'EP%s' % (str(check_dict['eps'])), 1)[0]

        # 得到目标轨道的index
        i = 0
        checker_index = 0
        for each_track in ep_sequence:
            if str(rail_name) in each_track.name():
                checker_index = i
                i += 1
                break

        # 目标 轨道
        checker_track = ep_sequence.videoTrack(checker_index)

        # binItem转成clip
        dst_clip = binItem_add.activeVersion().item()

        # 在ORI轨道上的TrackItem
        ori_trackItem = hiero.core.findItemsInProject(proj, ['TrackItem'], check_dict['shot_name'], 1)[0]

        # 创建的开始帧
        begin_frame = ori_trackItem.handleInTime()

        # 在轨道上创建trackItem
        checker_track.addTrackItem(dst_clip, begin_frame)

    def clear_old_version(self, submit_dict):
        """
        目前只写了清除时间线的部分，提交到cgtw的部分为完成， 缺失对应的module
        ::param submit_dict: 输入的字典， 跟check字典，一样
        submit_dict['eps']:  集数
        submit_dict['clip_name']:  clip_name 代表的是不带版本号的镜头名， 例：dza012231_cmp_liuwz_pre_v0101.mov， clip_name
                为 dza012231_cmp_liuwz_pre

        submit_dict['full_path']:   完整路径
        submit_dict['shot_name']：镜头号
        submit_dict['version']: 当前的版本号
        :return:
        """
        # submit_dict是检查完发送到CGTW的镜头信息
        # 清除submit_dict中的包含镜头上一个版本还老的素材(为了让文件不卡)

        # 定义dst_bin
        dst_checker_Bin = ''
        dst_last_version_Bin = ''
        dst_checker_video_rail = ''

        # 得到当前的项目
        proj = hiero.core.projects()[-1]

        # 得到该镜头对应的lastVersion文件夹
        last_version_bin_tuple = proj.bins('lastVersion')
        # 循环包含‘lastVersion’的 Bin tuple
        for each_Bin in last_version_bin_tuple:
            # 如果当前的bin文件夹的父文件夹在目标集数里
            if submit_dict['eps'] in each_Bin.parentBin().name():
                # 得到目标lastVersion文件夹
                dst_last_version_Bin = each_Bin
                break

        # 得到该镜头对应的checker文件夹
        checker_bin_tuple = proj.bins('checker')
        # 循环包含‘lastVersion’的 Bin tuple
        for each_Bin in checker_bin_tuple:
            # 如果当前的bin文件夹的父文件夹在目标集数里
            if submit_dict['eps'] in each_Bin.parentBin().name():
                # 得到目标checker文件夹
                dst_checker_Bin = each_Bin
                break

        # 得到对应的checker 轨道
        checker_rail_list = hiero.core.findItemsInProject(proj, ['VideoTrack'], 'checker', 1)
        for each_rail in checker_rail_list:
            if submit_dict['eps'] in each_rail.parent().name():
                dst_checker_video_rail = each_rail

        # 得到checker 轨道上面对应的trackItem
        checker_trackItem = hiero.core.findItemsInProject(proj, ['TrackItem'], submit_dict['clip_name'], 1)[0]

        # 删除在checker 轨道上的 trackItem
        dst_checker_video_rail.removeItem(checker_trackItem)

        # 删除checker文件夹的旧版本
        dst_checker_Bin.removeItem(checker_trackItem.currentVersion().parent())

        # 导入lastVersion文件夹并在lastVersion创建trackItem
        self.add_shot_to_checker_rail(submit_dict, dst_last_version_Bin, proj, 'lastVersion')

        print('send to cgtw~')
        print('发送到cgtw')
        pass
