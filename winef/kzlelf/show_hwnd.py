import win32gui

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


if __name__ == '__main__':
    window_datas = get_all_window_datas()
    import pprint
    pprint.pprint(window_datas)





