from tkinter import *

class TextColor:
    def __init__(self, root_, text_, button_):
        self.root = root_
        self.top = None
        self.text = text_
        self.button = button_
        self.is_toplevel_opened = False
        self.is_sync = StringVar()
        self.is_sync.set('< No >')
        self.is_sync_dict = {'< No >': False, '< Yes >': True}
        self.new_fg = None
        self.new_bg = None

    def on_close(self):
        # 当没有打开config color toplevel时按钮可用
        if self.is_toplevel_opened is False:
            self.top = Toplevel(self.root)
            self.top.resizable(width=False, height=False)
            self.top.title('color chooser')
            self.is_toplevel_opened = True
            self.button.config(state='disabled')
        else:
            self.top.destroy()
            self.button.config(state='normal')
            self.is_toplevel_opened = False

    def change_color(self):
        orig_color = (self.text.cget('foreground'), self.text.cget('background'))  # 保留原始颜色数据

        # region change_color
        # noinspection PyUnusedLocal
        def choose_color(*args):
            red = red_slider.get()
            red2 = red_slider2.get()
            blue = blue_slider.get()
            blue2 = blue_slider2.get()
            green = green_slider.get()
            green2 = green_slider2.get()
            color = "#%02x%02x%02x" % (red, green, blue)
            color2 = "#%02x%02x%02x" % (red2, green2, blue2)
            [lab.config(bg=color, fg=color2) for lab in labs]  # 使用列表推导式对样式标签进行逐个更改
            self.new_fg = color2
            self.new_bg = color
            if self.is_sync_dict[self.is_sync.get()]:  # 如果 synchronize（同步）
                self.text.config(bg=color, fg=color2)  # 同步修改 text 的颜色
            else:
                pass

        def confirm_change():  # 当self.is_sync == False可用
            self.text.config(fg=self.new_fg, bg=self.new_bg)

        def config_sync():  # 改变 text是否同步修改
            self.is_sync = True

        self.on_close()
        self.top.protocol('WM_DELETE_WINDOW', self.on_close)
        lab_frm = Frame(self.top)
        lab_frm.pack(padx=10, pady=0, fill=X)
        # region label frame
        Label(lab_frm, width=16, text='background color').pack(side='left')
        Label(lab_frm, width=14).pack(side='left')
        Label(lab_frm, width=17, text='foreground color').pack(side='left')
        # endregion
        render_frm = Frame(self.top, relief='groove', bd=2)  # 用于包含实时展现颜色变化内容的框架
        func_frm = Frame(self.top)  # 用于包含记录内容以及确认更改的功能的框架
        render_frm.pack(padx=10, side='left', fill=Y, pady=5)
        func_frm.pack(side='left', fill=Y, pady=5)
        # region render frame
        # region sliders
        slider_frm = Frame(render_frm)
        slider_frm.pack(side='left', fill='y')
        red_slider = Scale(slider_frm, troughcolor='red', length=535, from_=0, to=255,
                           sliderrelief='flat', width=20, command=choose_color)
        blue_slider = Scale(slider_frm, troughcolor='blue', length=535, from_=0, to=255,
                            sliderrelief='flat', width=20, command=choose_color)
        green_slider = Scale(slider_frm, troughcolor='green', length=535, from_=0, to=255,
                             sliderrelief='flat', width=20, command=choose_color)
        red_slider.set(255)
        green_slider.set(255)
        blue_slider.set(255)

        red_slider.grid(row=0, column=0)
        blue_slider.grid(row=0, column=1)
        green_slider.grid(row=0, column=2)
        # endregion
        # region labels
        lab_frm = Frame(render_frm, padx=10, pady=5)
        lab_frm.pack(side='left', fill='both', expand=True)
        lab1 = Label(lab_frm, text='hello', font='Times 25 bold')
        lab1.pack(fill='x')
        lab2 = Label(lab_frm, text='hello', font='Times 17 normal')
        lab2.pack(fill='x')
        lab3 = Label(lab_frm, text='hello', font='微软雅黑 25 bold')
        lab3.pack(fill='x')
        lab4 = Label(lab_frm, text='hello', font='微软雅黑 19 normal')
        lab4.pack(fill='x')
        lab5 = Label(lab_frm, text='hello', font='宋体 30 normal')
        lab5.pack(fill='x')
        lab6 = Label(lab_frm, text='hello', font='宋体 19 bold')
        lab6.pack(fill='x')
        lab7 = Label(lab_frm, text='world', font='Times 25 bold')
        lab7.pack(fill='x')
        lab9 = Label(lab_frm, text='hello', font='Times 24 bold')
        lab9.pack(fill='x')
        lab8 = Label(lab_frm, text='hello', font='Times 30 bold')
        lab8.pack(fill='both', expand=True)
        labs = [lab1, lab2, lab3, lab4, lab5, lab6, lab7, lab8, lab9]
        # endregion
        # region slider frm2
        slider_frm2 = Frame(render_frm)
        slider_frm2.pack(side='left', fill='y')
        red_slider2 = Scale(slider_frm2, troughcolor='red', length=535, from_=0, to=255,
                            sliderrelief='flat', width=20, command=choose_color)
        blue_slider2 = Scale(slider_frm2, troughcolor='blue', length=535, from_=0, to=255,
                             sliderrelief='flat', width=20, command=choose_color)
        green_slider2 = Scale(slider_frm2, troughcolor='green', length=535, from_=0, to=255,
                              sliderrelief='flat', width=20, command=choose_color)
        red_slider2.set(0)
        green_slider2.set(0)
        blue_slider2.set(0)

        red_slider2.grid(row=0, column=0)
        blue_slider2.grid(row=0, column=1)
        green_slider2.grid(row=0, column=2)
        # endregion
        # endregion

        # region functional frame
        ctrl_frm = LabelFrame(func_frm, text='confirm change', relief='groove',
                              fg='green', bd=2, padx=2, pady=5)
        ctrl_frm.pack(padx=5, side='left', fill='y')  # control method frame
        used_style_frm = LabelFrame(func_frm, text='historical color style', relief='groove',
                                    fg='green', bd=2, padx=2, pady=5)  # history style choose frame
        used_style_frm.pack(padx=5, side='left', fill='y')
        # region control frame
        # region confirm frame
        confirm_frm = Frame(ctrl_frm, relief='groove', bd=2)
        confirm_frm.pack(anchor='nw', padx=5, pady=8, fill=X)
        Label(confirm_frm, text='would you like to change your text edite region\'s color to new color?',
              font='Times 11 normal', justify='left', wraplength=180).pack(padx=2)
        Button(confirm_frm, text='<confirm>', command=confirm_change, relief='flat', fg='blue').pack(padx=5)

        # endregion
        # region synchronize frame (同步更改)
        def update_sync():
            if self.is_sync.get() == '< Yes >':         # 检查同步显示标记变量
                self.is_sync.set('< No >')
            else:
                self.is_sync.set('< Yes >')
        # 创建LabelFrame框架用于放置组件
        sync_frm = LabelFrame(ctrl_frm, text='synchronize', relief='groove', bd=2,
                              fg='green', font='微软雅黑12bold')
        sync_frm.pack(anchor='nw', pady=8, padx=5, fill=X)
        # 显示文字
        Label(sync_frm, text='would you like to change your text color while you choose '
                             'color in this window, it will synchronize in the text region'
                             ' without the confirm from you and the same time it\'s irrevocable',
              font='Times 11 normal', justify='left', wraplength=180).pack(padx=2)
        Label(sync_frm, text='is sync?', padx=5).pack(side='left')
        sync_btn = Button(sync_frm, textvariable=self.is_sync, command=update_sync, fg='blue',
                          width=6, relief='flat')
        sync_btn.pack(side='left')
        # endregion
        # endregion
        # region history style frame
        Label(used_style_frm, text='hello world style').pack()
        # endregion
        # endregion
