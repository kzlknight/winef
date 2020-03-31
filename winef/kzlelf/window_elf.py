import numpy as np
import pyautogui
import cv2
import aircv as ac
import win32gui
import win32com.client
import win32con
import time


# 例如关闭某个窗口后，等待多少秒确认窗口是否关闭成功
window_manage_delay_time = 0.5
# 最多确定多少次某个窗口是否操作成功
window_manage_confirm_num = 3

# 得到所有window的信息
def get_all_window_datas():
    window_datas = []
    def get_all_hwnd(hwnd, mouse):
        if win32gui.IsWindow(hwnd) and win32gui.IsWindowEnabled(hwnd) and win32gui.IsWindowVisible(hwnd):
            title = win32gui.GetWindowText(hwnd)
            if title:
                window_datas.append(
                    {
                        'hwnd':hwnd,'title':title
                    }
                )
    win32gui.EnumWindows(get_all_hwnd, 0)
    return window_datas

# 得到最前面窗口的句柄
def get_window_hwnd():
    hwnd = win32gui.GetForegroundWindow()
    return hwnd

# 得到句柄的标题
def get_window_title(hwnd):
    title = win32gui.GetWindowText(hwnd)
    return title

# 根据标题得到句柄
def get_window_hwnd_by_title(title):
    hwnds = []
    def get_all_hwnd(hwnd, mouse):
        if win32gui.IsWindow(hwnd) and win32gui.IsWindowEnabled(hwnd) and win32gui.IsWindowVisible(hwnd):
            this_title = win32gui.GetWindowText(hwnd)
            if title == this_title:
                hwnds.append(hwnd)
    win32gui.EnumWindows(get_all_hwnd, 0)
    return hwnds


# 判断句柄是否有对应的窗口，是：True，否：False
def is_window_by_hwnd(hwnd):
    return bool(win32gui.IsWindow(hwnd))

# 判断title时候有对应的窗口
def is_window_by_title(title):
    hwnds = get_window_hwnd_by_title(title)
    for hwnd in hwnds:
        if is_window_by_hwnd(hwnd):
            return True
        else:
            return False

# 根据句柄返回窗口的左顶点与右底点
def get_window_point(hwnd):
    left,top,right,bot = win32gui.GetWindowRect(hwnd)
    point_start = (left,top)
    point_end = (right,bot)
    return point_start,point_end

# 根据句柄返回最顶点与大小
def get_window_position_size(hwnd):
    left, top, right, bot = win32gui.GetWindowRect(hwnd)
    position = (left, top)
    width = right - left
    height = bot - top
    return position, (width, height)

# 输入左顶点与右底点，返回大小
def get_size(point_start,point_end):
    return (point_end[0] - point_start[0], point_end[1] - point_start[1])

# 根据句柄关闭窗口，返回关闭的结果
def close_window_by_hwnd(hwnd,window_manage_delay_time=window_manage_delay_time,window_manage_confirm_num=window_manage_confirm_num):
    win32gui.PostMessage(hwnd, win32con.WM_CLOSE, 0, 0)
    for i in range(window_manage_confirm_num):
        ret = not bool(is_window_by_hwnd(hwnd))
        if ret:
            return ret
        else:
            time.sleep(window_manage_delay_time)
    return ret

# 根据title，得到所有的句柄，并尝试关闭，如果都关闭程成功，返回True，否则返回False
def close_windows_by_title(title):
    try:
        hwnds = get_window_hwnd_by_title(title)
        close_rets = []
        for hwnd in hwnds:
            close_rets.append(
                close_window_by_hwnd(hwnd)
            )
        for close_ret in close_rets:
            if not close_ret:
                return False
        return True
    except:
        return False

# 指定左顶点，大小进行截图，如果传递save_path，为图片保存路径
def screenshot(position=(0,0),size=(1920,1080),save_path=None):
    src_img = pyautogui.screenshot(
        region=[position[0],position[1],size[0],size[1]]
    )
    if save_path:
        src_img.save(save_path)
    return src_img

# 读取src路径的图片，在范围中所有返回第一个匹配到图片的中心位置
def search_img_one(src,position=(0,0),size=(1920,1080),confidence=0.8):
    points = search_img_all(src=src,position=position,size=size,confidence=confidence)
    return points[0] if points else None

# 读取src路径的图片，在范围中所有返回所有匹配到图片的中心位置
def search_img_all(src,position=(0,0),size=(1920,1080),confidence=0.8):
    src_img = screenshot(position=position,size=size)
    src_img_digital = cv2.cvtColor(
        np.asarray(src_img),
        cv2.COLOR_RGB2BGR,
    )
    target_img_digital = ac.imread(src)
    match_results = ac.find_all_template(
        src_img_digital,
        target_img_digital,
        confidence
    )
    if match_results:
        result_points = []
        for match_result in match_results:
            x = int(match_result['result'][0]) + position[0]
            y = int(match_result['result'][1]) + position[1]
            result_points.append((x,y))
        return result_points
    else:
        return None


def search_imgs_one(srcs,position=(0,0),size=(1920,1080),confidence=0.8):
    for src in srcs:
        point = search_img_one(src,position=position,size=size,confidence=confidence)
        if point:
            return point
    return None



# 根据句柄得到窗口位置与大小，在其中搜索返回匹配成功第一个图片的中心位置
def search_img_one_by_hwnd(src,hwnd=None,confidence=0.8):
    position,size = get_window_position_size(hwnd)
    return search_img_one(src=src,position=position,size=size,confidence=confidence)

# 根据句柄得到窗口位置与大小，在其中搜索返回匹配成功所有图片的中心位置
def search_img_all_by_hwnd(src,hwnd=None,confidence=0.8):
    position,size = get_window_position_size(hwnd)
    return search_img_all(src=src,position=position,size=size,confidence=confidence)



# 设置窗口的位置与大小
def set_window_pos(hwnd=None,position=(),size=()):
    if not hwnd:
        hwnd = get_window_hwnd()
    # 讲窗口置于顶层
    set_window_foreground_top(hwnd)
    current_position, current_size = get_window_position_size(hwnd)
    if not position:
        position = current_position
    if not size:
        size = current_size
    win32gui.SetWindowPos(
        hwnd,
        win32con.HWND_TOPMOST,
        position[0], position[1],
        size[0], size[1],
        win32con.SWP_SHOWWINDOW
    )
    current_position, current_size = get_window_position_size(hwnd)
    if position == current_position and size == current_size:
        return True
    else:
        return False

# 顶层显示句柄窗口
def set_window_foreground_top(hwnd):
    # shell = win32com.client.Dispatch("WScript.Shell")
    # shell.SendKeys('%')
    try:
        win32gui.SendMessage(hwnd, win32con.WM_SYSCOMMAND, win32con.SC_RESTORE, 0)
        win32gui.SetForegroundWindow(hwnd)
        win32gui.BringWindowToTop(hwnd)
        time.sleep(window_manage_delay_time)
        return True
    except:
        return False

# 最小化窗口
def set_window_min(hwnd):
    win32gui.ShowWindow(hwnd,win32con.SW_MINIMIZE)


# 最大化窗口
def set_window_max(hwnd):
    win32gui.ShowWindow(hwnd,win32con.SW_MAXIMIZE)

# 返回活跃窗口的句柄与标题，key=hwnd，value=title
def get_all_window():
    window = dict()
    def get_all_hwnd(hwnd, mouse):
        if win32gui.IsWindow(hwnd) and win32gui.IsWindowEnabled(hwnd) and win32gui.IsWindowVisible(hwnd):
            title = win32gui.GetWindowText(hwnd)
            if title:
                window.update({hwnd:title})
    win32gui.EnumWindows(get_all_hwnd, 0)
    return window


