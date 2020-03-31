from .operator import *
from .settings import Settings as st



def retry(func):
    def wrapper(*args,**kwargs):
        for i in range(3):
            ret = func(*args,**kwargs)
            if ret:return ret
            print('尝试第%s次'%i)
        return False
    return wrapper




class QQOperator(Operator):
    def __init__(self,hwnd):
        Operator.__init__(self,hwnd)
        self.position_a = st.QQ.position_a
        self.position_c = st.QQ.position_c
        self.size = st.QQ.size

    @retry
    def normalize_size(self):
        '''
        把窗口的尺寸设置成self.size
        :return:
        '''
        self.window.set_window_pos(size=self.size)
        position,size = self.window.get_position_size()
        if size == self.size:
            return True
        else:
            return False

    def put_window_to_position_a(self):
        '''

        :return:
        '''
        pass

if __name__ == '__main__':
    hwnds = get_window_hwnd_by_title('鬼 - 酷狗音乐 G.E.M.邓紫棋 - 来自天堂的魔')
    print(hwnds)



