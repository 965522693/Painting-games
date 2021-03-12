from pygame import font
from pygame import Surface
from pygame import mouse
from pygame import draw
from pygame import image
import 我们画你们猜.NetRoom as Net
import os


class Label:
    def __init__(self, name, label, pos, font_size=30):
        self.name = name
        self.label = label
        self.pos = pos
        self.font = font.SysFont('SimHei', font_size)
        self.label = self.font.render(self.label, True, (0, 0, 0))
        self.if_draw = True  # 是否显示

    def draw(self, screen: Surface):
        if not self.if_draw:
            return None
        screen.blit(self.label, self.pos)


class EditBox:
    Inputting_color = (0, 0, 255)
    Free_color = (0, 0, 0)

    def __init__(self, name, label, pos):
        self.name = name
        self.label_word = label
        self.pos = pos
        self.if_inputting = False
        self.label = Label(name, label, (pos[0] + 5, pos[1] + 5))
        self.rect = (pos[0], pos[1], self.get_rect_size(), 40)
        self.line_begin_pos = (self.rect[0] + self.rect[2], self.rect[1] + self.rect[3])
        self.line_end_pos = (self.line_begin_pos[0] + 200, self.line_begin_pos[1])
        self.content = ''  # 所记录的内容
        self.content_pos = (self.line_begin_pos[0] + 2, self.rect[1] + 2)
        self.content_label = Label(name, self.content, self.content_pos)
        self.judge_rect_x = (self.rect[0], self.line_end_pos[0])
        self.judge_rect_y = (self.rect[1], self.line_end_pos[1])
        self.if_draw = True  # 是否显示

    def del_content(self):
        if not self.if_draw:
            return None
        self.content = self.content[:-1]
        self.content_label = Label(self.name, self.content, self.content_pos)

    def input_content(self, word):
        if not self.if_draw:
            return None
        self.content += word
        self.content_label = Label(self.name, self.content, self.content_pos)

    def get_rect_size(self):
        size = 0
        for a in self.label_word:
            if 'a' <= a <= 'z' or 'A' <= a <= 'Z':
                size += 15
            else:
                size += 30
        return int(size + 10)

    def judge_rect(self):
        # 当位置准确时返回true 否则返回false
        if not self.if_draw:
            return False
        x, y = mouse.get_pos()
        if self.judge_rect_x[0] <= x <= self.judge_rect_x[1] and self.judge_rect_y[0] <= y <= self.judge_rect_y[1]:
            self.if_inputting = True
            return True
        self.if_inputting = False
        return False

    def draw(self, screen: Surface):
        if not self.if_draw:
            return None
        self.label.draw(screen)
        draw.rect(screen, EditBox.Inputting_color if self.if_inputting else EditBox.Free_color, self.rect, 1)
        draw.line(screen, EditBox.Inputting_color if self.if_inputting else EditBox.Free_color,
                  self.line_begin_pos, self.line_end_pos)
        self.content_label.draw(screen)


class Button:
    word_color = (0, 0, 0)
    rect_color = (0, 0, 0)
    choice_color = (0, 255, 0)

    def __init__(self, name, show_name, pos, img=None, event_fun=None, *args):
        self.name = name
        self.show_name = show_name
        self.event = event_fun
        self.args = args  # 参数列表
        self.pos = pos
        self.img = img
        self.font = font.SysFont('SimHei', 30)
        self.label = self.font.render(self.show_name, True, Button.word_color)
        self.word_rect_width = 10
        self.word_pos = (pos[0] + self.word_rect_width, pos[1] + self.word_rect_width)
        self.rect = ()
        self.if_draw = True  # 是否显示
        self.if_choice = False  # 是否被选中，用于图被选择
        self.init_data()

    def init_data(self):
        if self.img is not None:
            self.rect = (self.pos[0], self.pos[1], self.img.get_rect()[2], self.img.get_rect()[3])
        else:
            self.rect = (self.pos[0], self.pos[1], len(self.show_name) * 30 + self.word_rect_width * 2,
                         30 + self.word_rect_width * 2)

    def judge_rect(self):
        if not self.if_draw:
            return False
        x, y = mouse.get_pos()
        if 0 < x - self.pos[0] < self.rect[2] and 0 < y - self.pos[1] < self.rect[3]:
            if self.event is not None:
                self.event(*self.args)
            if self.rect[2] == 50:
                self.if_choice = True
            return True
        else:
            return False

    def draw(self, screen: Surface):
        if not self.if_draw:
            return None
        if self.img is not None:
            screen.blit(self.img, self.pos)
            if self.if_choice:
                draw.rect(screen, Button.choice_color, self.rect, 1)
            return None
        screen.blit(self.label, self.word_pos)
        draw.rect(screen, Button.rect_color, self.rect, 1)


class Pen:

    def __init__(self, color, pen_type='pen'):
        self.color = color
        self.size = 5
        self.open = False  # 是否允许留下痕迹
        self.pen_type = pen_type  # 画笔类型
        self.pen_time_max = 2  # 最大采样频率
        self.pen_time = self.pen_time_max  # 采样计数

    def pen_draw(self, screen):
        if self.pen_type == 'rubber':
            # 橡皮
            draw.circle(screen, (0, 0, 0), mouse.get_pos(), self.size, 2)
        if self.open:
            self.pen_time -= 1
            if self.pen_time == 0:
                self.pen_time = self.pen_time_max
            else:
                return None
            img = PlayerImg('circle', self.color, mouse.get_pos(), self.size)
            return img


class PlayerImg:
    # 该类用于保存玩家所绘制的图形对象

    def __init__(self, draw_type, color, pos, size):
        self.draw_type = draw_type
        self.color = color
        self.pos = pos
        self.size = size

    def draw_img(self, screen):
        if self.draw_type == 'circle':
            draw.circle(screen, self.color, self.pos, self.size)

    def pack_info(self):
        info = self.draw_type + '-' + str(self.color) + '-' + str(self.pos) + '-' + str(self.size)
        return info


class Ui:

    def __init__(self):
        self.level = '初始房间'
        self.button_dict = {}
        self.exit_box_dict = {}
        self.label_dict = {}
        self.head_img_list = []  # 头像列表
        self.pen_img_dict = {}  # 画笔功能字典
        self.choice_box = None  # 选中的编辑框
        self.choice_head_img = 0  # 选中头像序号
        self.net = None  # 网络对象
        self.pen_color = (0, 0, 0)  # 当前使用笔的颜色
        self.pen = Pen(self.pen_color)  # 当前使用的笔
        self.draw_player_img = []  # 玩家绘制的图画
        self.init_data()

    def init_data(self):
        path = os.getcwd() + '/素材'
        head_dir = path + '/头像'
        head_img = os.listdir(head_dir)
        pen_dir = path + '/游戏功能'
        pen_img = os.listdir(pen_dir)
        for head in head_img:
            img = image.load(head_dir + '/' + head)
            self.head_img_list.append(img)
        for pen in pen_img:
            img = image.load(pen_dir + '/' + pen)
            name = pen.split('.')[0]
            self.pen_img_dict[name] = img
        self.button_dict = {'初始房间-创建房间': Button('创建房间', '创建房间', (400, 180), None, self.open_room),
                            '初始房间-加入房间': Button('加入房间', '加入房间', (600, 180), None,
                                                lambda n='加入房间': self.switch_level(n)),
                            '加入房间-确定': Button('确定', '确定', (800, 120), None, self.join_room),
                            '房间中-铅笔': Button('铅笔', '铅笔', (200, 600), self.pen_img_dict['铅笔'], self.get_pen),
                            '房间中-橡皮': Button('橡皮', '橡皮', (250, 600), self.pen_img_dict['橡皮'], self.set_rubber),
                            '房间中-红色': Button('红色', '红色', (300, 600), self.pen_img_dict['红色'],
                                             lambda n='红色': self.set_pen_color(n)),
                            '房间中-黄色': Button('黄色', '黄色', (350, 600), self.pen_img_dict['黄色'],
                                             lambda n='黄色': self.set_pen_color(n)),
                            '房间中-绿色': Button('绿色', '绿色', (400, 600), self.pen_img_dict['绿色'],
                                             lambda n='绿色': self.set_pen_color(n)),
                            '房间中-黑色': Button('黑色', '黑色', (450, 600), self.pen_img_dict['黑色'],
                                             lambda n='黑色': self.set_pen_color(n)),
                            '房间中-蓝色': Button('蓝色', '蓝色', (500, 600), self.pen_img_dict['蓝色'],
                                             lambda n='蓝色': self.set_pen_color(n)),
                            '房间中-重画': Button('重画', '重画', (550, 600), self.pen_img_dict['重画'], self.redraw),
                            '房间中-切换': Button('切换', '切换', (600, 600), self.pen_img_dict['切换'],
                                             self.change_draw_player)
                            }

        head_img_init_x = 600 - (len(head_img) // 2) * 100
        head_img_init_y = 300
        head_img_max_num = 8  # 一行最多的容纳数
        for head in range(len(head_img)):
            pos = (head_img_init_x + (head % head_img_max_num) * 100,
                   head_img_init_y + (head // head_img_max_num) * 100)
            key = '初始房间-头像{}'.format(head)
            self.button_dict[key] = Button('头像{}'.format(head), '头像{}'.format(head),
                                                                pos, self.head_img_list[head], self.set_head_img_num,
                                                                head, key)
        self.exit_box_dict = {'初始房间-昵称': EditBox('昵称', '昵称', (400, 100)),
                              '加入房间-房间名': EditBox('房间名', '房间名', (400, 100)),
                              '加入房间-房间ip': EditBox('房间ip', '房间ip', (400, 150))}
        self.label_dict = {'初始房间-头像选择': Label('头像', '请选择头像', (500, 250))}
        self.switch_level()

    def change_draw_player(self):  # 切换绘制玩家
        if self.net.index != self.net.drawing_player_index:
            return None
        index = (self.net.drawing_player_index + 1) % len(self.net.player_list)
        self.net.change_draw(index)

    def redraw(self):  # 重画
        self.draw_player_img.clear()

    def pack_img(self):
        if self.net is None or len(self.draw_player_img) == 0:
            return None
        info = ''
        for img_player in self.draw_player_img:
            info = info + img_player.pack_info() + '%'
        self.net.send_img(info[:-1])

    def up_pack_img(self):  # 将收到的图像信息解包绘制
        if self.net is not None and self.net.drawing_player_index != self.net.index:
            self.draw_player_img.clear()
            if self.net.img_info == '':
                return None
            info = self.net.img_info.split('%')
            for i in info:
                draw_type, color, pos, size = i.split('-')
                color = color[1:-1].split(',')
                color = (int(color[0]), int(color[1]), int(color[2]))
                pos = pos[1:-1].split(',')
                pos = (int(pos[0]), int(pos[1]))
                size = int(size)
                self.draw_player_img.append(PlayerImg(draw_type, color, pos, size))

    def set_pen_color(self, color):
        if color == '红色':
            self.pen_color = (255, 0, 0)
        elif color == '绿色':
            self.pen_color = (0, 255, 0)
        elif color == '蓝色':
            self.pen_color = (0, 0, 255)
        elif color == '黄色':
            self.pen_color = (255, 255, 0)
        elif color == '黑色':
            self.pen_color = (0, 0, 0)
        if self.pen.pen_type == 'pen':
            self.pen.color = self.pen_color

    def get_pen(self):  # 设置pen为画笔
        self.pen = Pen(self.pen_color)
        self.pen.pen_type = 'pen'

    def set_rubber(self):  # 设置橡皮
        self.pen.color = (255, 255, 255)
        self.pen.pen_type = 'rubber'

    def open_room(self):  # 创建房间并成为服务器
        self.net = Net.Server(self.exit_box_dict['初始房间-昵称'].content, self.choice_head_img)
        self.switch_level('房间中')

    def join_room(self):  # 作为用户加入房间
        self.net = Net.Client(self.exit_box_dict['初始房间-昵称'].content, self.exit_box_dict['加入房间-房间ip'].content,
                              self.exit_box_dict['加入房间-房间名'].content, self.choice_head_img)
        self.switch_level('房间中')

    def set_head_img_num(self, num, button_key):  # 设置头像编号
        for key, button in self.button_dict.items():
            if key != button_key:
                button.if_choice = False
        self.choice_head_img = num

    def switch_level(self, level='初始房间'):
        self.level = level
        for key, button in self.button_dict.items():
            key_level, button_name = key.split('-')
            if key_level == self.level:
                button.if_draw = True
            else:
                button.if_draw = False
        for key, box in self.exit_box_dict.items():
            key_level, box_name = key.split('-')
            if key_level == self.level:
                box.if_draw = True
            else:
                box.if_draw = False
        for key, label in self.label_dict.items():
            key_level, button_name = key.split('-')
            if key_level == self.level:
                label.if_draw = True
            else:
                label.if_draw = False
        if self.level == '初始房间':
            self.choice_box = self.exit_box_dict['初始房间-昵称']
        elif self.level == '房间中':
            self.choice_box = None
        elif self.level == '加入房间':
            pass

    def judge_exit_box(self):
        if self.level == '加入房间':
            for key, box in self.exit_box_dict.items():
                if box.judge_rect():
                    self.choice_box = box
                    break

    def judge_button(self):
        for key, button in self.button_dict.items():
            button.judge_rect()

    def input_box(self, content):  # 输入内容
        if self.choice_box is not None:
            if content == 'del':
                self.choice_box.del_content()
            else:
                self.choice_box.input_content(content)

    def open_pen(self):
        if self.level == '房间中' and self.pen is not None and self.net.index == self.net.drawing_player_index:
            self.pen.open = True

    def close_pen(self):
        if self.level == '房间中' and self.pen is not None:
            self.pen.open = False

    def set_pen_size(self, abs_size):
        # 设置画笔大小，参数为相对值
        if self.pen is not None:
            self.pen.size += abs_size
            if self.pen.size < 1:
                self.pen.size = 1

    def draw(self, screen: Surface):
        self.pack_img()
        self.up_pack_img()
        for key, box in self.exit_box_dict.items():
            box.draw(screen)
        for key, label in self.label_dict.items():
            label.draw(screen)
        for img in self.draw_player_img:
            img.draw_img(screen)
        if self.net is not None:
            self.net.draw(screen, self.level)
        if self.pen is not None:
            draw_now = self.pen.pen_draw(screen)
            if draw_now is not None:
                self.draw_player_img.append(draw_now)
        for key, button in self.button_dict.items():
            button.draw(screen)


if __name__ == '__main__':
    pass
