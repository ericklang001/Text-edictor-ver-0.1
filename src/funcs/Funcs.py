import re
import os.path
import ctypes
from tkinter import *
from random import randint
from tkinter import colorchooser
from funcs.FontConfiger import FontConfigure
from funcs.IndexMaker import IndexMaker

ctypes.windll.shcore.SetProcessDpiAwareness(1)
ctypes.windll.shcore.GetScaleFactorForDevice(0)


class OpenTop:
    tap_size = 4  # 按下 tab 键的空格数

    def __init__(self, root_win):
        # region toplevel
        self.root = root_win
        self.top = Toplevel(root_win)
        self.top.title('记事本')
        self.top.geometry('1350x900')
        self.top.config(bg='#F0F0F0')
        self.top.rowconfigure(1, weight=1)
        self.top.columnconfigure(0, weight=1)
        # endregion
        # region text frame
        self.text_frm = Frame(self.top, width=380, height=150, bg='lightgray')
        self.text_frm.grid(row=1, padx=10, sticky='nsew')
        self.text_frm.propagate(False)
        self.text_frm.rowconfigure(0, weight=1)
        self.text_frm.columnconfigure(1, weight=1)
        x_scrollbar = Scrollbar(self.text_frm, orient='horizontal')
        y_scrollbar = Scrollbar(self.text_frm, orient='vertical')
        self.text = Text(self.text_frm, width=30, height=10, wrap='none', undo=True, font='Times 12 normal',
                         xscrollcommand=x_scrollbar.set, yscrollcommand=y_scrollbar.set)
        self.index_text = Text(self.text_frm, width=3, yscrollcommand=y_scrollbar.set, font='Times 12 normal', )
        self.index_maker = IndexMaker(self.text, self.index_text)
        self.index_text.bind('<MouseWheel>', lambda *args: self.on_mousewheel(*args))
        self.text.bind('<MouseWheel>', lambda *args: self.on_mousewheel(*args))
        self.text.bind("<Control-z>", lambda event: self.undo())
        self.text.bind("<Control-y>", lambda event: self.redo())
        x_scrollbar.grid(row=1, column=1, sticky='we', pady=0)
        y_scrollbar.grid(row=0, column=2, sticky='ns')
        self.index_text.grid(row=0, column=0, sticky='ns')
        self.text.grid(row=0, column=1, sticky='nsew')
        self.text.bind('<Tab>', OpenTop.tab_space_edit)
        Label(self.text_frm, bg='#f0f0f0').grid(row=1, column=2, sticky='nsew')
        Label(self.text_frm, bg='#f0f0f0').grid(row=1, column=0, sticky='nsew')
        x_scrollbar.config(command=self.text.xview)
        y_scrollbar.config(command=lambda *args: (self.text.yview(*args), self.index_text.yview(*args)))
        # 配置 'underline' 标签和 'strikethrough' 删除线标签
        self.text.tag_config('underline', underline=True)
        self.text.tag_config('strikethrough', overstrike=True)
        self.text.tag_config('font_style', font='Times 12 normal')
        self.index_text.tag_config('font_style', font='Times 12 normal')
        # endregion+
        self.menubar = Menu(self.top)
        self.font_config = FontConfigure(self.top, self.text, self.index_text)
        self.font_config.get_root(self.root)
        self.menu_pack()
        self.top.config(menu=self.menubar)

    def on_mousewheel(self, event):
        # 根据鼠标滚轮事件滚动两个 Text 组件
        self.text.yview_scroll(-1 * (event.delta // 120), "units")
        self.index_text.yview_scroll(-1 * (event.delta // 120), "units")
        return "break"

    def menu_pack(self):
        # region 删除线和下划线操作
        self.menubar.add_command(label='underline', underline=0, command=self.add_underline)
        self.menubar.add_command(label='deleteline', underline=2, command=self.deleteline)
        self.menubar.add_command(label='remove underline', command=self.rev_underline)
        self.menubar.add_command(label='remove deleteline', command=self.rev_deleteline)
        # endregion
        # region 颜色操作
        self.menubar.add_command(label='foreground', underline=0, command=self.fg_change_chooser)
        self.menubar.add_command(label='background', underline=3, command=self.bg_change_chooser)
        # endregion
        # region 控制操作
        self.menubar.add_command(label='clear all', underline=0, command=self.clear_all)
        self.menubar.add_command(label='select all', underline=0, command=lambda: OpenTop.select_all(self.text))
        self.menubar.add_command(label='delete', underline=0, command=lambda: OpenTop.delete(self.text))
        self.menubar.add_command(label='undo', command=self.undo)
        self.menubar.add_command(label='redo', command=self.redo)
        # endregion

    # region deleteline and underline methods
    # 添加下划线
    def add_underline(self):
        try:
            self.text.tag_add("underline", "sel.first", "sel.last")
        except TclError:
            print("未选取文字: in method add_underline()")

    # 去除下划线
    def rev_underline(self):
        try:
            self.text.tag_remove('underline', 'sel.first', 'sel.last')
        except TclError:
            print('未选取文字: in method rev_underline()')

    # 添加删除线
    def deleteline(self):
        try:
            # 添加标签
            self.text.tag_add('strikethrough', 'sel.first', 'sel.last')
        except TclError:
            # 如果没有选取，输出报错信息
            print('未选取文字: in method deleteline()')

    # 去除删除线
    def rev_deleteline(self):
        try:
            self.text.tag_remove('strikethrough', 'sel.first', 'sel.last')
        except TclError:
            print('未选取文字: in method(rev_deleteline)')

    # endregion

    # region color methods
    # noinspection PyTypeChecker
    # 设置选中文字的前景颜色
    def fg_change_chooser(self, color_=None):
        if color_ is None:
            try:
                color = colorchooser.askcolor()[1]
                if color:
                    self.text.tag_add('fg_color_tag', 'sel.first', 'sel.last')
                    self.text.tag_config('fg_color_tag', foreground=color)
            except TclError:
                print('未选取文字')
        else:
            try:
                self.text.tag_add('fg_color_tag', 'sel.first', 'sel.last')
                self.text.tag_config('fg_color_tag', foreground=color_)
            except TclError:
                print('未选取文字')

    # noinspection PyTypeChecker
    # 设置选中文字的背景颜色
    def bg_change_chooser(self, color_=None):
        if color_ is None:
            try:
                color = colorchooser.askcolor()[1]
                if color:
                    self.text.tag_add('bg_color_tag', 'sel.first', 'sel.last')
                    self.text.tag_config('bg_color_tag', background=color)
            except TclError:
                print('未选取文字')
        else:
            try:
                self.text.tag_add('bg_color_tag', 'sel.first', 'sel.last')
                self.text.tag_config('bg_color_tag', background=color_)
            except TclError:
                print('未选取文字')

    # endregion

    # endregion
    # region 控制操作

    @staticmethod
    def select_all(target_text):
        target_text.tag_add('sel', '1.0', 'end')
        target_text.mark_set('insert', '1.0')
        target_text.see('insert')

    @staticmethod
    def delete(target: Text):
        try:
            target.delete('sel.first', 'sel.last')
        except TclError:
            print('未选取文字')

    # 撤销操作
    def undo(self):
        index0 = self.text.index("end")  # 获取初始最后一行的后一行的索引
        try:
            self.text.edit_undo()
            index1 = self.text.index("end")  # 获取撤销后最后一行的后一行的索引
            if int(index1.split('.')[0]) < int(index0.split('.')[0]):  # 如果撤销后行数变少
                self.index_text.delete(index1, index0)
            elif int(index1.split('.')[0]) > int(index0.split('.')[0]):  # 如果撤销后行数变多
                mark = self.index_maker.index       # 通过self.index_maker对象来同步处理行号
                for i in range(mark, int(index1.split('.')[0]) - int(index0.split('.')[0]) + mark):
                    self.index_text.insert('end', f'\n{i}')
                    self.index_maker.index += 1
            self.index_maker.index = int(index1.split('.')[0])
            self.index_text.yview_moveto(self.text.yview()[0])  # 同步更新索引的滚轴位置
        except:
            print('先前没有动作')
        return "break"

    # 取消撤销操作
    def redo(self):
        index0 = self.text.index('end')
        try:
            self.text.edit_redo()
            index1 = self.text.index('end')
            print('删除后index：', index1)
            self.index_text.delete(index0, index1)
        except:
            print('先前没有动作')
        return "break"

    # 清除当前所有内容
    def clear_all(self):
        OpenTop.select_all(self.text)
        self.delete(self.text)
        OpenTop.select_all(self.index_text)
        self.delete(self.index_text)
        self.index_text.insert('1.0', '1')
        self.index_maker.index = 2

    # endregion

    # 设置一个Tab键的缩进空格数，不同的文体同样数目空格下可能长度不同
    @staticmethod
    def tab_space_edit(event):
        text_widget = event.widget
        text_widget.insert(INSERT, " " * OpenTop.tap_size)
        return 'break'  # return 'break' 似乎作用是使修改tab键绑定函数修改生效


# 随机更换壁纸
def change_wallpaper(pho: object, last, cb):
    pho.order = randint(0, last - 1)        # 设置PhotoApy对象的order属性，用于修改壁纸
    cb.current(pho.order)       # 调用combobox的当前选取的值，同步更新壁纸索引显示
    pho.update(pho.use_size)    # 调用PhotoApy对象的update()方法，更新壁纸显示


# 更换壁纸为指定索引的壁纸
def switch_wallpaper(pho: object, choice):
    pho.order = choice      # 设置PhotoApy对象的order属性，用于修改壁纸
    pho.update(pho.use_size)    # 调用PhotoApy对象的update()方法，更新壁纸显示


# 使用Func.py中的主类OpenTop()来打开文本编辑界面
def open_text1(root_win):
    return OpenTop(root_win)


if __name__ == '__main__':
    root = Tk()
    root.withdraw()
    op = OpenTop(root)
    op.top.protocol('WM_DELETE_WINDOW', root.destroy)
    root.mainloop()
