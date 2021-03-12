import 我们画你们猜.NetRoom as Net
from pygame import time
from pygame import display
from pygame import Surface
from pygame import init
from pygame import event as events
from pygame import MOUSEMOTION
from pygame import MOUSEBUTTONDOWN
from pygame import MOUSEBUTTONUP
from pygame import KEYDOWN
from pygame import KEYUP
from pygame import QUIT
from pygame import image
from sys import exit
import 我们画你们猜.Ui as Ui


class Mind:
    level_now = '初始房间'  # 当前层次
    size = 1100, 650  # 尺寸
    fps = 60
    time_now = 0  # 当前时间

    def __init__(self):
        self.clock = time.Clock()
        self.screen = display.set_mode(Mind.size)
        self.time_max = Mind.fps
        self.if_run = True  # 时间开关
        self.ui = Ui.Ui()
        self.init_data()

    def init_data(self):
        pass

    def draw(self):
        self.ui.draw(self.screen)

    def deal_event(self, event):
        if event == 'MOUSE_LEFT_DOWN':
            self.ui.judge_button()
            self.ui.judge_exit_box()
            self.ui.open_pen()
        elif event == 'MOUSE_LEFT_UP':
            self.ui.close_pen()
        elif event == 'MOUSE_MID_UP':
            self.ui.set_pen_size(1)
        elif event == 'MOUSE_MID_DOWN':
            self.ui.set_pen_size(-1)
        elif event == 'del' or '0' <= event <= '9' or event == '.' or 'a' <= event <= 'z':
            self.ui.input_box(event)


def run():
    init()
    display.set_caption("我们画你们猜")
    mind = Mind()
    while True:
        mind.screen.fill((255, 255, 255))
        mind.draw()
        for event in events.get():
            if event.type == QUIT:
                exit()
            elif event.type == MOUSEMOTION:
                pass
            elif event.type == MOUSEBUTTONDOWN:
                # button  左1 右3 向下5 向上4
                if event.button == 1:
                    mind.deal_event('MOUSE_LEFT_DOWN')
                elif event.button == 3:
                    mind.deal_event('MOUSE_RIGHT_DOWN')
                elif event.button == 4:
                    mind.deal_event('MOUSE_MID_UP')
                elif event.button == 5:
                    mind.deal_event('MOUSE_MID_DOWN')
            elif event.type == MOUSEBUTTONUP:
                # button
                if event.button == 1:
                    mind.deal_event('MOUSE_LEFT_UP')
            elif event.type == KEYDOWN:
                if 256 <= event.key <= 265:
                    mind.deal_event(str(event.key - 256))  # 纯数字输入
                elif 48 <= event.key <= 57:
                    mind.deal_event(str(event.key - 48))  # 纯数字输入
                elif event.key == 47 or event.key == 266:
                    mind.deal_event('.')  # 小数点
                elif event.key == 8:
                    mind.deal_event('del')  # 退格键按下
                elif 97 <= event.key <= 122:
                    mind.deal_event(chr(event.key))
            elif event.type == KEYUP:
                # print(event.key)
                pass
        mind.clock.tick(mind.fps)
        display.update()


if __name__ == '__main__':
    run()
