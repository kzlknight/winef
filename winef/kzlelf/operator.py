from .keyboard_elf import *
from .mouse_elf import *
from .window_elf import *

import random


# 封装好的Window对象
class Window():
    def __init__(self,hwnd):
        self.hwnd = hwnd

    # 得到类内句柄的左顶点与右底点
    def get_point(self):
        left, top, right, bot = win32gui.GetWindowRect(self.hwnd)
        point_start = (left, top)
        point_end = (right, bot)
        return point_start, point_end

    # 得到类内句柄的位置与大小
    def get_position_size(self):
        left, top, right, bot = win32gui.GetWindowRect(self.hwnd)
        position = (left,top)
        width = right - left
        height = bot - top
        return position,(width,height)

    # 对类内句柄窗口搜索图片，返回第一个匹配成功的图片中心位置
    def search_img_one(self,src,position_relative=(),size_relative=(),confidence=0.8):
        position,size = self.get_position_size()
        if position_relative:
            position = (np.array(position_relative) + np.array(position)).tolist()
        if size_relative:
            size = size_relative
        point = search_img_one(src=src,position=position,size=size,confidence=confidence)
        if not point:
            return None
        else:
            return point[0] - position[0],point[1] - position[1]

    def search_imgs_one(self,srcs,position_relative=(),size_relative=(),confidence=0.8):
        position, size = self.get_position_size()
        if position_relative:
            position = (np.array(position_relative) + np.array(position)).tolist()
        if size_relative:
            size = size_relative
        point = search_imgs_one(srcs=srcs, position=position, size=size, confidence=confidence)
        if not point:
            return None
        else:
            return point[0] - position[0], point[1] - position[1]

    # 对类内句柄窗口搜索图片，返回所有匹配成功的图片中心位置
    def search_img_all(self,src, position_relative=(),size_relative=(),confidence=0.8):
        position,size = self.get_position_size()
        if position_relative:
            position = (np.array(position_relative) + np.array(position)).tolist()
        if size_relative:
            size = size_relative
        points = search_img_all(src=src,position=position,size=size, confidence=confidence)
        if not points:
            return None
        else:
            points_relative = []
            for point in points:
                points_relative.append(
                    (point[0] - position[0],point[1] - position[1])
                )
            return points_relative

    def search_img_all_relative_position(self,src,relative_position,relative_size,confidence=0.8): # todo 和上面的方法重复了
        position,size = self.get_position_size()
        this_position = position[0] + relative_position[0],position[1] + relative_position[1]
        points = search_img_all(src=src,position=this_position,size=relative_size, confidence=confidence)
        if not points:
            return None
        else:
            points_relative = []
            for point in points:
                points_relative.append(
                    (point[0] - position[0],point[1] - position[1])
                )
            return points_relative

    def search_img_one_relative_position(self,src,relative_position,relative_size,confidence=0.8):
        points_relative = self.search_img_all_relative_position(src,relative_position,relative_size,confidence)
        return points_relative[0] if points_relative else None


    def search_imgs_one_relative_position(self,srcs,relative_position,relative_size,confidence=0.8):
        for src in srcs:
            points_relative = self.search_img_all_relative_position(src, relative_position, relative_size, confidence)
            if points_relative:
                return points_relative[0]
        return None


    def screenshot(self,relative_position, relative_size, save_path=None):
        position, size = self.get_position_size()
        this_position = position[0] + relative_position[0], position[1] + relative_position[1]
        return screenshot(this_position,relative_size,save_path)





    # 对类内窗口设置位置与大小，如果设置成功返回True，否则返回False
    def set_window_pos(self,position=(),size=()):
        return set_window_pos(self.hwnd,position=position,size=size)

    # 顶层显示句柄窗口
    def set_window_foreground_top(self):
        set_window_foreground_top(self.hwnd)

    # 最小化窗口
    def set_window_min(self):
        set_window_min(self.hwnd)

    # 最大化窗口
    def set_window_max(self):
        set_window_max(self.hwnd)

    # 关闭窗口
    def close_window(self):
        return close_window_by_hwnd(self.hwnd)

    # 得到句柄的标题
    def get_title(self):
        return get_window_title(self.hwnd)



    # 读取剪贴板
    # def clipboard_get(self):
    #     return get_clipboard(charset=self.clipboard_charset)

class Keyboard():
    def __init__(self,keyboard_press_time,keyboard_delay_time):
        self.keyboard_press_time = keyboard_press_time
        self.keyboard_delay_time = keyboard_delay_time

    # 按键
    def press_key(self,key):
        press_key(key=key,press_time=self.keyboard_press_time)

    # 按住Ctrl,再按键
    def press_key_ctrl(self,key):
        press_key_ctrl(key=key,press_time=self.keyboard_press_time)

    # 回车
    def press_enter(self):
        press_enter(press_time=self.keyboard_press_time)

    # 删除
    def press_delete(self):
        press_delete(press_time=self.keyboard_press_time)


class Clipboard():
    def __init__(self,clipboard_charset):
        self.clipboard_charset = clipboard_charset

    # 读取剪切板
    def get_clipboard(self):
        return get_clipboard(charset=self.clipboard_charset)

    # 清空剪贴板
    def clear_clipboard(self):
        set_clipboard('')

    # 清空剪贴板，然后写入剪切板
    def set_clipboard(self,str):
        set_clipboard(str)

    # 设置剪贴板，Ctrl+V
    def write_clipboard(self,str):
        write_clipboard(str)


class Mouse():
    def __init__(self,hwnd,mouse_press_time,mouse_move_delay_time):
        self.hwnd = hwnd
        self.mouse_press_time = mouse_press_time
        self.mouse_move_delay_time = mouse_move_delay_time

    def move(self,point):
        move(point=point)

    def move_relative(self,point):
        position_start,position_end = get_window_point(self.hwnd)
        point_relative = position_start[0] + point[0],position_start[1] + point[1]
        self.move(point=point_relative)

    def click_l(self):
        click_l(press_time=self.mouse_press_time)

    def click_r(self):
        click_r(press_time=self.mouse_press_time)

    def scroll(self,rposition_x,rposition_y):
        scroll(rposition_x=rposition_x,rposition_y=rposition_y)

    def select_l(self,points):
        point_start = points[0]
        point_end = points[1]
        select_l(point_start=point_start,point_end=point_end,press_time=mouse_press_time)

    def select_l_relative(self,points):
        position_start,position_end = get_window_point(self.hwnd)

        point_start = points[0]
        point_end = points[1]

        point_start_relative = position_start[0] + point_start[0],position_start[1] + point_start[1]
        point_end_relative = position_start[0] + point_end[0],position_start[1] + point_end[1]

        points_relative = [point_start_relative,point_end_relative]
        self.select_l(points_relative)


    def move_l(self,point):
        move_l(point=point)

    def move_l_relative(self,point):
        position_start,position_end = get_window_point(self.hwnd)
        point_relative = position_start[0] + point[0],position_start[1] + point[1]
        self.move_l(point_relative)


    def move_r(self,point):
        move_r(point=point)

    def move_r_relative(self,point):
        position_start,position_end = get_window_point(self.hwnd)
        point_relative = position_start[0] + point[0],position_start[1] + point[1]
        self.move_r(point_relative)




func_retry_delay = 1 # 函数的重试延时
func_retry_num = 3 # 函数的重试次数
func_delay = 1 # 函数执行成功后的延时

window_delay = 1 # 打开关闭新窗口的延时
window_retry_num = 3 # 窗口的重试次数

action_delay = 0.5 # 动作延时
action_retry_num = 3 # 检查动作的重试次数



class Operator():
    def __init__(self,hwnd):
        self.hwnd = hwnd

        self.keyboard_press_time = 0.2  # 键盘按住的时间
        self.keyboard_delay_time = 0.1  # 键盘动作后的等待时间
        self.clipboard_charset = 'gbk' # 剪贴板的默认编码
        self.mouse_press_time = 0.2  # 鼠标点击按住的时间
        self.mouse_move_delay_time = 0.1  # 鼠标移动或点击后停留的时间

        self.window = Window(self.hwnd)
        self.keyboard = Keyboard(self.keyboard_press_time,self.keyboard_delay_time)
        self.clipboard = Clipboard(clipboard_charset=self.clipboard_charset)
        self.mouse = Mouse(self.hwnd,self.mouse_press_time,self.mouse_move_delay_time)

    def cg_window_hwnd(
            self,
            point,
            new_window_title,
            is_close_old_old_window=True,
            window_delay = window_delay,
            window_retry_num = window_retry_num,
    ):
        # 窗口最上层显示
        self.window.set_window_foreground_top()
        # 关闭之前的新标题窗口
        if is_close_old_old_window:
            close_windows_by_title(new_window_title)
        # 点开查找
        self.mouse.move_l_relative(point)
        for i in range(window_retry_num):
            # 延时window_delay
            time.sleep(window_delay)
            # 找到查找
            hwnds = get_window_hwnd_by_title(new_window_title)
            # 如果找到的句柄不唯一，返回False
            if len(hwnds) == 1:
                return hwnds[0]
        return False


    def check_window_load_by_img(
            self,
            srcs,
            window_delay=window_delay,
            window_retry_num=window_retry_num
    ):
        if type(srcs).__name__ == 'str':
            srcs = [srcs,]

        for i in range(window_retry_num):
            time.sleep(window_delay)
            search_zhaoqun_point = self.window.search_imgs_one(srcs=srcs)
            if search_zhaoqun_point:
                return True
        return False

    def get_window_hwnd_by_title(
            self,
            title,
            is_title_vague=False, # 是否开启title模糊查找
            window_delay = window_delay,
            window_retry_num = window_retry_num,
    ):
        # 顶层窗口的title是否为传入进来的title,如果是，返回这个窗口的句柄
        for i in range(window_retry_num):
            # 顶层窗口的句柄
            foreground_window_hwnd = get_window_hwnd()
            # 顶层窗口的title
            foreground_window_title = get_window_title(
                foreground_window_hwnd
            )

            # 如果title符合，返回句柄
            if title == foreground_window_title:
                return foreground_window_hwnd
            # 如果支持模糊查询
            elif is_title_vague:
                if title[0:1] in foreground_window_title:
                    return foreground_window_hwnd
            # title不相等，模糊查询也没找到，就延时window_delay
            else:
                time.sleep(window_delay)


        # 在不是顶层窗口中查找
        for i in range(window_retry_num):
            window_datas = get_all_window_datas()
            for window_data in window_datas:
                # 窗口的title
                this_window_title = window_data['title']
                # 窗口的hwnd
                this_window_hwnd = window_data['hwnd']
                # 如果title符合，返回hwnd
                if title == this_window_title:
                    return this_window_hwnd
                # 如果支持模糊查询
                elif is_title_vague:
                    if title[0:1] in this_window_title:
                        return this_window_hwnd
            # 转了一圈，没找到，在等window_delay
            time.sleep(window_delay)
        # 顶层和非顶层都没有找到，返回False
        return False

    def get_window_load_hwnd_by_size(
            self,
            new_window_size,
            old_window_hwnd,
            window_delay=window_delay,
            window_retry_num=window_retry_num,

    ):
        for i in range(window_retry_num):
            foreground_window_hwnd = get_window_hwnd()
            foreground_window_position,foreground_window_size = get_window_position_size(foreground_window_hwnd)

            # 如果新句柄与老窗口句柄不相等且尺寸为预定的尺寸
            if foreground_window_hwnd != old_window_hwnd and foreground_window_size == new_window_size:
                return foreground_window_hwnd
            else:
                time.sleep(window_delay)
        return False







