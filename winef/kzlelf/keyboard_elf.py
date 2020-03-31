from pynput.keyboard import Key
from pynput.keyboard import Controller as KeyController
from pynput.keyboard import KeyCode
import win32clipboard
import win32con
import time


# 普通键盘操作 ---------------------------------------------------
keyboard = KeyController()
keyboard_press_time = 0.2 # 键盘按住的时间
keyboard_delay_time = 0.1 # 键盘动作后的等待时间

# 键盘标操作后的延时
def __keyboardSecurityDelay(func):
    def wrapper(*args,**kwargs):
        ret = func(*args,**kwargs)
        time.sleep(keyboard_delay_time)
        return ret
    return wrapper

# 按键
@__keyboardSecurityDelay
def press_key(key,press_time=keyboard_press_time):
    keyboard.press(key)
    time.sleep(press_time)
    keyboard.release(key)

# 按住Ctrl,再按键
@__keyboardSecurityDelay
def press_key_ctrl(key,press_time=keyboard_press_time):
    with keyboard.pressed(Key.ctrl):
        keyboard.press(key)
        time.sleep(press_time)
        keyboard.release(key)

# 回车
@__keyboardSecurityDelay
def press_enter(press_time=keyboard_press_time):
    keyboard.press(Key.enter)
    time.sleep(press_time)
    keyboard.release(Key.enter)

# 删除
@__keyboardSecurityDelay
def press_delete(press_time=keyboard_press_time):
    keyboard.press(Key.delete)
    time.sleep(press_time)
    keyboard.release(Key.delete)

# 剪贴板 ------------------------------------------------------------
# 剪贴板的默认编码
clipboard_charset = 'gbk'

# 读取剪切板
def get_clipboard(charset=clipboard_charset):
    win32clipboard.OpenClipboard()
    text = win32clipboard.GetClipboardData(win32con.CF_TEXT).decode(charset,"ignore")
    win32clipboard.CloseClipboard()
    return text

# 清空剪贴板
def clear_clipboard():
    set_clipboard('')

# 清空剪贴板，然后写入剪切板
def set_clipboard(str):
    win32clipboard.OpenClipboard()
    win32clipboard.EmptyClipboard()
    win32clipboard.SetClipboardText(str)
    win32clipboard.CloseClipboard()

# 设置剪贴板，Ctrl+V
def write_clipboard(str):
    set_clipboard(str)
    press_key_ctrl('v')