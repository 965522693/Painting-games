import socket
from _thread import start_new_thread
import 我们画你们猜.Player as Player
from 我们画你们猜.Ui import Label


class Server:

    def __init__(self, name, head_img_number):  # 名字和头像序号
        self.ip = socket.gethostbyname(socket.gethostname())
        self.ip_show = Label('ip', 'ip:' + self.ip, (0, 0), 10)
        self.name = name
        self.head_img_number = head_img_number
        self.port = get_port_by_name(self.name)  # 获取端口号
        self.sockets = (self.ip, self.port)  # 套接字
        self.clients_list = []  # 所有其他用户套接字
        self.player_list = []  # 所有用户对象，包括自己
        self.udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.udp.bind(self.sockets)
        start_new_thread(self.get_net_info, ())  # 网络信息线程
        self.drawing_player_index = 0  # 当前正在绘制玩家的索引
        self.index = 0  # 自身索引
        self.img_info = ''  # 收到来自某用户的图像暂存信息
        self.init_data()

    def init_data(self):
        my_player = Player.Player(self.name, self.head_img_number, 0)
        self.player_list.append(my_player)

    def get_net_info(self):
        while True:
            get_date = self.udp.recvfrom(65535)
            client_socket = get_date[1]  # 收到来自某客户的地址
            info_list = get_date[0].decode('utf-8').split('!')
            order = info_list[0]  # 命令字
            info = info_list[1]  # 信息字
            if order == 'join':  # 主机收到来自客户端的消息  请求加入房间
                self.join_one_in_room(info, client_socket)
            elif order == 'new_img_client':  # 主机收到来自客户的图像转发请求
                self.send_img_client(info, client_socket)
            elif order == 'new_draw_index':  # 主机收到来自客户端的更新玩家转发请求
                self.change_draw_client(info, client_socket)

    def change_draw(self, index):  # 切换玩家
        self.drawing_player_index = index
        info = bytes('next_draw!' + str(index), encoding='utf-8')
        for i in self.clients_list:
            self.udp.sendto(info, i)

    def change_draw_client(self, info, client_socket):
        self.drawing_player_index = int(info)
        info = bytes('new_draw!' + str(info), encoding='utf-8')
        for i in self.clients_list:
            if i != client_socket:
                self.udp.sendto(info, i)

    def send_img_client(self, info, client_socket):
        self.img_info = info
        info = bytes('new_img!' + info, encoding='utf-8')
        for i in self.clients_list:
            if i != client_socket:
                self.udp.sendto(info, i)

    def send_img(self, info):  # 由绘制玩家向其他玩家发送当前的图像
        info = bytes('new_img!' + str(info), encoding='utf-8')
        for i in self.clients_list:
            self.udp.sendto(info, i)

    def join_one_in_room(self, info, client_socket):  # 让某个玩家加入房间
        info = info.split('`')
        client = Player.Player(info[0], int(info[1]), len(self.player_list))
        self.player_list.append(client)
        self.clients_list.append(client_socket)
        self.renew_info_to_clients()
        self.udp.sendto(bytes('index!' + str(len(self.player_list) - 1),
                              encoding='utf-8'), client_socket)  # 想该玩家发送他的索引

    def renew_info_to_clients(self):
        info = ''
        for i in self.player_list:
            info += i.pack_info()
            info += '`'
        info = bytes('renew!' + info[:-1], encoding='utf-8')
        for i in self.clients_list:
            self.udp.sendto(info, i)

    def draw(self, screen, level):
        if level == '房间中':
            self.ip_show.draw(screen)
            for player in self.player_list:
                player.draw_player_ui(screen)
            self.player_list[self.drawing_player_index].draw_now_player_rect(screen)


class Client:

    def __init__(self, name, server_ip, server_name, head_img_number):  # 提供用户名和服务器套接字,头像序号
        self.ip = socket.gethostbyname(socket.gethostname())
        self.name = name
        self.port = get_port_by_name(self.name)  # 获取端口号
        self.server_socket = (server_ip, get_port_by_name(server_name))  # 服务器套接字
        self.head_img_number = head_img_number  # 头像序号
        self.sockets = (self.ip, self.port)  # 套接字
        self.player_list = []  # 所有用户对象，包括自己
        self.udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.udp.bind(self.sockets)
        start_new_thread(self.get_net_info, ())  # 网络信息线程
        self.drawing_player_index = 0  # 当前正在绘制玩家的索引
        self.index = 0  # 自己的玩家索引
        self.img_info = ''  # 收到来自某用户的图像暂存信息
        self.init_data()

    def init_data(self):
        self.apply_join_room()

    def apply_join_room(self):  # 向服务器申请加入房间
        self.udp.sendto(bytes('join!' + self.name + '`' + str(self.head_img_number), encoding='utf-8'),
                        self.server_socket)

    def get_net_info(self):
        while True:
            get_date = self.udp.recvfrom(65535)
            server_address = get_date[1]  # 收到来自服务器的地址
            info_list = get_date[0].decode('utf-8').split('!')
            order = info_list[0]  # 命令字
            info = info_list[1]  # 信息字
            if order == 'renew':  # 客户收到服务器的命令 更新玩家列表
                self.renew_info(info)
            elif order == 'index':  # 客户收到服务器的命令 设置自己的索引
                self.index = int(info)
            elif order == 'new_img':  # 客户收到服务器的命令 刷新图像
                self.img_info = info
            elif order == 'next_draw':  # 客户端收到服务器的命令 切换绘制用户
                self.drawing_player_index = int(info)

    def change_draw(self, index):  # 切换玩家
        self.drawing_player_index = index
        info = bytes('new_draw_index!' + str(index), encoding='utf-8')
        self.udp.sendto(info, self.server_socket)

    def send_img(self, info):  # 由绘制玩家向服务器发送当前的图像
        info = bytes('new_img_client!' + info, encoding='utf-8')
        self.udp.sendto(info, self.server_socket)

    def renew_info(self, info):  # 更新来自服务器的玩家信息
        info = info.split('`')
        self.player_list = []
        for i in info:
            key = i.split(',')
            player = Player.Player(key[0], int(key[1]), int(key[2]))
            self.player_list.append(player)

    def draw(self, screen, level):
        if level == '房间中':
            for player in self.player_list:
                player.draw_player_ui(screen)
            try:
                self.player_list[self.drawing_player_index].draw_now_player_rect(screen)
            except IndexError:
                return None


def get_port_by_name(name, first=True):
    low = 1024
    bottle = 65535
    if first:
        count = (sum(ord(i) for i in name) + low) % bottle
    else:
        count = (name + low) % bottle
    if bottle >= count >= low:
        return count
    else:
        return get_port_by_name(count, False)


