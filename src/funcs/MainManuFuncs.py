from funcs import Funcs
from tkinter import *
from tkinter import messagebox
from tkinter.filedialog import asksaveasfilename, askopenfilename

class ManuFuncs:
    def __init__(self, root_, ):
        self.text_obj = None
        self.root = root_

    def create_text_obj(self):
        self.text_obj = Funcs.open_text1(self.root)

    # def get_index(self):
    #     with open('recent_files.data', 'r') as f:
    #         data = f.read()
    #         data_list = json.loads(data) if data else list()
    #         return len(data_list)

    def save(self):
        def check(path_str):
            if '/' in path_str or r'\\' in path_str:
                path = path_str
            else:
                path = path_str.replace('\\', '\\\\')
            try:
                with open(path, 'w'):
                    print("hello world")
            except:
                messagebox.showwarning(title='path wrong',
                    message='can\'t find path or the path\'s format you entry is incorrect!')
                return False
            return save_(path)

        def save_(path):
            try:
                with open(path, 'w') as f:
                    f.write(content)
                font_path = ''.join([path.split('.')[-2], '_font.txt'])
                with open(font_path, 'w') as f:
                    f.write(font_type)
                print('文件保存成功')
            except:
                print('保存文件时发生错误！')
        # save 函数预处理
        try:
            content = self.text_obj.font_config.content     # 获取将要保存的文件的内容
            font_type = self.text_obj.text.cget('font')     # 后去将要保存的文件的字体样式
            print(content, font_type)
        except:         # 如果将要保留的文件所属对象为None，即未创建编辑文件对象时，报错
            content = ''
            print('self.text_obj is NoneType')

        # 用于用户输入文件路径的窗口
        save_top = Toplevel(self.root)
        save_top.title('save file')
        Label(save_top, text='Entry save path:', anchor='w', font='Times 15 normal', padx=10).pack(fill=X, pady=20)
        path_ent = Entry(save_top, width=23, font='Times 16 normal')
        path_ent.pack(pady=0, padx=10)
        confirm_btn = Button(save_top, text='confirm', command=lambda: check(path_ent.get()))
        confirm_btn.pack(pady=15)

    def save_as(self):
        # 获取编辑文件对象的内容和字体样式，如果对象存在时
        try:
            content = self.text_obj.font_config.content
            font_type = self.text_obj.text.cget('font')
            print(content, font_type)
        except:
            print('self.text_obj is NoneType')
            return
        # 使用文件另存为的文件管理器以保存文件
        filename = asksaveasfilename(defaultextension='.txt')
        if filename == '':
            return
        else:
            with open(filename, 'w') as f:
                f.write(content)
                messagebox.showinfo(title='', message='文件保存成功')
            with open(''.join([filename.split('.')[-2], '_font.txt']), 'w') as f:
                f.write(font_type)

    def open_file(self):
        filename = askopenfilename()
        try:
            with open(filename, 'r') as f:
                content = f.read()[:-1]
            font_path = filename.split('.')[-2] + '_font.txt'
        except:
            print("打开文件时发生错误，获取内容失败！")
            return None
        try:
            with open(font_path, 'r') as f:
                font = f.readline().strip()
            print(content, font)
        except:
            print("没有配置的font文件！")
            font = 'Times 12 normal'
            print(content)

        self.create_text_obj()
        self.text_obj.text.insert('end', content)
        self.text_obj.text.config(font=font)
        self.text_obj.index_text.config(font=font)
        self.text_obj.font_config.type_cbox.set(font.split()[0])
        self.text_obj.font_config.size_cbox.set(int(font.split()[1]))

