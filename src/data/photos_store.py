import ctypes
import os
import re
from tkinter import *
from PIL import Image


def get_image_size(path):
    try:
        with Image.open(path) as photo_image:
            return photo_image.size
    except FileNotFoundError:
        print(f'Not found file {path}')
    except Exception as e:
        print(f'Error: {e}')
    return None


def get_filelist(folder_path_):
    return os.listdir(folder_path_)


def extract_number(filename):
    # 使用正则表达式匹配文件名中的数字部分
    match = re.search(r'\d+', filename)
    if match:
        return int(match.group())
    return 0


folder_path = os.path.abspath('../resource_/photos/new')
filelist = get_filelist(folder_path)
filelist = [folder_path.replace('\\', '/') + '/' + f.replace('\\', '/')
            for f in sorted(filelist, key=extract_number)]
ori_size_list = [get_image_size(f) for f in filelist]
std_sizes = [(850, 820 * s[1] // s[0]) for s in ori_size_list]
# 使用列表推导式和字典推导式生成所需列表
photos_link_list = [
    {
        'path': path,
        'ori_size': ori_size,
        'std_size': std_size
    }
    for path, ori_size, std_size in zip(filelist, ori_size_list, std_sizes)
]

# 美人鱼
photo1_path = r"D:\photo\game_photos\photo2\new\photo61.png"
photo1_link = {'ori_size': (1725, 776), 'std_size': (800, 800 * 776 // 1725 + 20), 'path': photo1_path}

