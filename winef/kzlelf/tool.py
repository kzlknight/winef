from pynput.keyboard import Key, Listener
from kzlelf.window_operator import *



def on_press(key):
    if key == Key.down:
        move_relative((0,1))
    elif key == Key.up:
        move_relative((0,-1))
    elif key == Key.left:
        move_relative((-1,0))
    elif key == Key.right:
        move_relative((1,0))



def on_release(key):
    if key == Key.shift:
        hwnd = get_window_hwnd()
        window = Window(hwnd)
        position,size = window.get_position_size()
        mouse_position = mouse.position
        position_relative = mouse_position[0] - position[0],mouse_position[1] - position[1]
        print('句柄',hwnd,'标题',window.get_title(),'位置',position,'窗口大小:',size,'相对位置',position_relative)







with Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()
    # 停止监视
# Listener.stop()
