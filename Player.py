import os
from pygame import image
from 我们画你们猜.Ui import Label
from pygame import draw


class Player:
    head_img_list = []
    path = os.getcwd() + '/素材'
    head_dir = path + '/头像'
    head_img = os.listdir(head_dir)
    for head in head_img:
        img = image.load(head_dir + '/' + head)
        head_img_list.append(img)

    def __init__(self, name, head_img_number, room_number):  # 用户名,头像序号,自身在房间中的序号
        self.name = name
        self.head_img_number = head_img_number
        self.room_number = room_number
        self.pos = (10, 10 + self.head_img_number * 60)
        self.label_show = Label(self.name, self.name, (self.pos[0] + 60, self.pos[1] + 10))

    def pack_info(self):
        # 打包成可发送信息
        info = self.name + ',' + str(self.head_img_number) + ',' + str(self.room_number)
        return info

    def draw_player_ui(self, screen):
        # 绘制游戏中的左侧用户头像ui
        screen.blit(Player.head_img_list[self.head_img_number], self.pos)
        self.label_show.draw(screen)

    def draw_now_player_rect(self, screen):  # 绘制正在绘画的玩家的边框
        draw.rect(screen, (0, 255, 0), (self.pos[0], self.pos[1], 50, 50), 1)



