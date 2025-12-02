from funcs.TextColorConfiger import TextColor
from tkinter import *
from tkinter.ttk import Combobox

class FontConfigure:
    def __init__(self, top_, text_, index_text_):
        self.content = None
        self.root = None
        self.toolsbar = Frame(top_, padx=10, relief='groove', bd=2)
        self.toolsbar.grid(row=0, column=0, columnspan=2, sticky='nsew', padx=3, pady=5)
        # region toolsbar
        # region font
        Label(self.toolsbar, text='type', font='微软雅黑 10 normal').pack(side='left', padx=4)
        self.type_cbox = Combobox(self.toolsbar, height=5)
        self.type_cbox.pack(side='left', pady=0)
        self.type_cbox['value'] = ['微软雅黑', '宋体', 'Times', '黑体', 'Courier', 'Verdana', 'Calibri',
                                   '行楷', 'Courier New', 'Menlo', 'Consolas']
        self.type_cbox.set('Times')
        self.type_cbox.bind("<Return>", lambda event: self.change_font_size())
        type_confirm_btn = Button(self.toolsbar, text='confirm', width=6, pady=1, relief='groove',
                                  command=self.change_font_type)
        type_confirm_btn.pack(side='left', padx=5, pady=5)
        Label(self.toolsbar, text='size', font='微软雅黑 10 normal').pack(side='left', padx=4)
        self.size_cbox = Combobox(self.toolsbar)
        self.size_cbox.pack(side='left')
        self.size_cbox['value'] = tuple(range(1, 60))
        self.size_cbox.set(12)
        self.size_cbox.bind("<Return>", lambda event: self.change_font_size())
        size_confirm_btn = Button(self.toolsbar, text='confirm', width=6, pady=1, relief='groove',
                                  command=self.change_font_size)
        size_confirm_btn.pack(side='left', padx=5, pady=5)
        self.is_bold = BooleanVar()
        self.is_bold.set(True)
        self.exchange_b_n_btn = Button(self.toolsbar, text='normal', width=8, pady=1, relief='groove',
                                       command=self.exchange_bold_normal)
        self.exchange_b_n_btn.pack(side='left', padx=5, pady=5)
        # endregion

        self.text = text_
        self.index_text = index_text_

        # region color bar
        self.color_btn = Button(self.toolsbar, text='config color', width=10, bd=2, relief='groove',
                                command=lambda: self.color_chooser.change_color())
        self.color_btn.pack(side='left', padx=10, pady=5)
        self.color_chooser = TextColor(top_, self.text, self.color_btn)
        self.turn_back_btn = Button(self.toolsbar, text='Return', command=self.turn_back, relief='groove', bd=2)
        self.turn_back_btn.pack(side='left', pady=5)
        # endregion
        # endregion

    def get_root(self, root_):
        self.root = root_

    # return 按钮回调函数
    def turn_back(self):
        # 获取文本编辑区域全部内容，用于后续操作
        self.content = self.text.get('1.0', 'end')
        # 显示root窗口
        self.root.deiconify()
        self.root.lift()

    def update_while_select(self, font_used):
        font = tuple(font_used.split())
        self.type_cbox.set(font[0])
        self.size_cbox.set(font[1])

    def change_font_type(self):
        # 获取当前字体样式
        current_font = self.text.cget("font")
        size = int(current_font.split()[1]) if current_font else 12
        weight = current_font.split()[-1] if current_font else "normal"
        type_ = self.type_cbox.get() if self.type_cbox.get() != '' else "微软雅黑"
        # 如果选取了内容，更新标签字体
        new_font = (type_, size, weight)
        print(new_font)
        try:
            # 如果选取了内容，对选取内容进行字体样式修改
            self.text.tag_config("font_style", font=new_font)
            self.text.tag_add("font_style", "sel.first", "sel.last")
            self.index_text.tag_config('font_style', font=new_font)
            index_ = self.text.index('sel.first')
            begin = "".join([index_[0], ".0"])
            end = "".join([index_[0], '.1'])
            self.index_text.tag_add('font_style', begin, end)
            self.update_while_select(current_font)
        except:
            # 全局修改字体
            self.text.config(font=new_font)     # 通过修改标签更改字体样式
            self.index_text.config(font=new_font)
            print('未选取内容，使用全局修改: in method change_font_type()')

    def change_font_size(self):
        current_font = self.text.cget("font")
        type_ = current_font.split()[0] if current_font else "微软雅黑"
        weight = current_font.split()[-1] if current_font else "normal"
        size_ = self.size_cbox.get() if self.size_cbox.get() else 12
        new_font = (type_, size_, weight)
        print(new_font)
        try:
            # 如果选取了字体，更新标签字体
            self.text.tag_config("font_style", font=new_font)
            self.text.tag_add("font_style", "sel.first", "sel.last")
            self.index_text.tag_config("font_style", font=new_font)
            index_ = self.text.index('sel.first')
            begin = ''.join([index_[0], '.0'])
            end = ''.join([index_[0], '.1'])
            self.index_text.tag_add('font_style', begin, end)
            self.update_while_select(current_font)
        except:
            # 全局修改字体
            self.text.config(font=new_font)
            self.index_text.config(font=new_font)
            print('未选取内容，使用全局更改: in method change_font_size()')

    def exchange_bold_normal(self):
        current_font = self.text.cget("font")
        type_ = current_font.split()[0] if current_font else "宋体"
        size_ = int(current_font.split()[1]) if current_font else 9
        weight = ''
        if current_font:
            self.is_bold.set(1 - self.is_bold.get())
            if self.is_bold.get():  # 如果当前状态为bold
                self.exchange_b_n_btn.config(text='normal')
                weight = 'normal'
            else:
                self.exchange_b_n_btn.config(text='bold')
                weight = 'bold'

        new_font = (type_, size_, weight)
        try:
            # 如果选取了内容，更新标签字体
            self.text.tag_config("font_style", font=new_font)
            self.text.tag_add("font_style", "sel.first", "sel.last")
        except TclError:
            # 全局修改字体
            self.text.config(font=new_font)
        finally:
            self.get_font_style()

    def get_font_style(self):
        if __name__ == "__main__":
            font_str = self.text.cget("font")
            print(font_str)
