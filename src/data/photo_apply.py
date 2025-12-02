import os.path
import re
import ctypes
from tkinter import *
from PIL import ImageTk, Image
from data import photos_store as phs

ctypes.windll.shcore.SetProcessDpiAwareness(1)
ctypes.windll.shcore.GetScaleFactorForDevice(0)


class PhotoApy:
    default_order: int = 0
    path = os.path.abspath('../resource_/default_setting.txt')
    with open(path, 'r') as f:
        pattern = r'(default_order:\s*)(-?\d+)'
        data = f.read()
        num = re.search(pattern, data).groups()[1]
        try:
            default_order = int(num)
        except Exception:
            print("初始化默认壁纸索引失败")

    def __init__(self, root_win: object, targ_size_w: int = 800,
                 color: str = 'white', order: int = default_order):
        # noinspection PyTypeChecker
        self.img: PhotoImage = None
        self.root_win = root_win
        self.photos_msg: list = phs.photos_link_list
        self.count: int = len(phs.photos_link_list)
        self.order = order
        self.color = color
        self.path = self.photos_msg[self.order]["path"]
        self.ori_size = self.photos_msg[self.order]["ori_size"]
        self.std_size = self.photos_msg[self.order]["std_size"]
        self.targ_size = (targ_size_w, targ_size_w * self.ori_size[1] // self.ori_size[0])
        self.use_size = self.targ_size if targ_size_w != 800 else self.std_size

    def add_photo(self, path):
        size = phs.get_image_size(path)
        std_size = std_sizes = (850, 820 * size[1] // size[0])
        pho_msg = {
            'path': path,
            'ori_size': size,
            'std_size': std_size
        }
        self.photos_msg.append(pho_msg)

    # 将图片应用为壁纸
    def use_img(self):
        try:
            photo_ = Image.open(self.path)
            resized_photo = photo_.resize(self.use_size)
            self.img: PhotoImage = ImageTk.PhotoImage(resized_photo)
            # noinspection PyTypeChecker
            label = Label(self.root_win, image=self.img, anchor='nw',
                          font='Times 20 bold', fg=self.color)
            label.grid(row=1, column=0)
        except:
            print('Not found photo')

    # 更新图片显示
    def update(self, use_size_):
        self.path = self.photos_msg[self.order]['path']
        self.ori_size = self.photos_msg[self.order]['ori_size']
        self.std_size = self.photos_msg[self.order]['std_size']
        self.use_size = (use_size_[0], use_size_[0]*self.ori_size[1]//self.ori_size[0])
        self.use_img()

    # 显示图片信息
    def show_msg(self):
        print(f'path: {self.path}, ori_size{self.ori_size}, std_size{self.std_size}, '
              f'targ_size{self.targ_size}, use_size{self.use_size}')


if __name__ == '__main__':
    root = Tk()
    po = PhotoApy(root, targ_size_w=800, color='white', order=3)
    po.use_img()
    po.show_msg()

    root.mainloop()
