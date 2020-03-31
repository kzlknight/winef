from pynput.mouse import Controller as MouseController
from pynput.mouse import Button
import time


mouse = MouseController()
mouse_press_time = 0.2 # 鼠标点击按住的时间
mouse_move_delay_time = 0.1 # 鼠标移动或点击后停留的时间

# 鼠标操作后的延时
def __mouseSecurityDelay(func):
    def wrapper(*args,**kwargs):
        ret = func(*args,**kwargs)
        time.sleep(mouse_move_delay_time)
        return ret
    return wrapper

# 移动鼠标位置
@__mouseSecurityDelay
def move(point):
    mouse.position = point

# 鼠标相对移动
def move_relative(point):
    position_last = mouse.position
    position_new = position_last[0] + point[0],position_last[1] + point[1]
    mouse.position = position_new



# 左键点击
@__mouseSecurityDelay
def click_l(press_time=mouse_press_time):
    mouse.press(Button.left)
    time.sleep(press_time)
    mouse.release(Button.left)

# 右键点击
@__mouseSecurityDelay
def click_r(press_time=mouse_press_time):
    mouse.press(Button.right)
    time.sleep(press_time)
    mouse.release(Button.right)

# 滚轮滚动
@__mouseSecurityDelay
def scroll(rposition_x,rposition_y):
    mouse.scroll(rposition_x,rposition_y)

# 移动到point_start,鼠标左键按住，移动到point_end，鼠标左键弹起
@__mouseSecurityDelay
def select_l(point_start,point_end,press_time=mouse_press_time):
    move(point_start)
    mouse.press(Button.left)
    time.sleep(press_time/2)
    move(point_end)
    time.sleep(press_time/2)
    mouse.release(Button.left)

# 移动到点并左键单击
def move_l(point):
    move(point)
    click_l()

# 移动到点并右键单击
def move_r(point):
    move(point)
    click_r()