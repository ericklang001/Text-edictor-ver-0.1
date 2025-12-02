import ctypes
from tkinter.ttk import Combobox

import funcs.Funcs
import data.photo_apply
from tkinter import *
from funcs.ConfigFuncs import add_photo, set_default
from funcs.MainManuFuncs import ManuFuncs
from funcs.HelpFuncs import call_help

ctypes.windll.shcore.SetProcessDpiAwareness(1)
ctypes.windll.shcore.GetScaleFactorForDevice(0)

root = Tk()
root.title('Text editor launcher')
# root.geometry('820x500+200+100')
root.config(bg='white')
menubar = Menu(root)
manu_funcs = ManuFuncs(root)

# 建立 file 子菜单
file_menu = Menu(menubar, tearoff=False)
menubar.add_cascade(label='file', menu=file_menu)
# 向 file 子菜单列表添加内容
new_file_menu = Menu(file_menu, tearoff=False)
# region new file
file_menu.add_command(label='new file', command=manu_funcs.create_text_obj)
# endregion
# region save, save as, open file
file_menu.add_command(label='save file', command=manu_funcs.save)
file_menu.add_command(label='save file as', command=manu_funcs.save_as)
file_menu.add_command(label='open file', command=manu_funcs.open_file)
# endregion

# 创建photo_apply类的实例
po = data.photo_apply.PhotoApy(root, order=data.photo_apply.PhotoApy.default_order, targ_size_w=1400)
# region tools bar
toolsbar = Frame(root, pady=2)      # 创建Frame框架对象
toolsbar.grid(row=0, column=0, sticky='nsew', padx=5, pady=2)
Button(toolsbar, text='change wallpaper', width=15, relief='raised',            # change wallpaper 按钮
       command=lambda: funcs.Funcs.change_wallpaper(po, po.count, cb)).pack(side='left', padx=5)
select_frm = Frame(toolsbar, bg='white')        # 内部框架，用于分区布置combobox组件
select_frm.pack(side='left', fill='both', expand=True)
# switch wallpaper 标签
Label(select_frm, text='switch wallpaper', width=15).pack(side='left', padx=5, fill=Y, pady=4)
cb = Combobox(select_frm)       # 在select_frm框架内创建combobox组件
cb.set(data.photo_apply.PhotoApy.default_order+1)
cb.bind('<Return>', lambda event: funcs.Funcs.switch_wallpaper(po, cb.current()))
cb['value'] = list(range(1, po.count+1))        # 设置combobox组件内列表数值
cb.pack(side='left', padx=5, pady=4)
Button(select_frm, text='confirm', width=15, command=lambda: funcs.Funcs.switch_wallpaper(po, cb.current())).pack(
                                              side='left', padx=5, pady=4)
# endregion

config_menu = Menu(menubar, tearoff=False)
menubar.add_cascade(label='config', menu=config_menu)
config_menu.add_command(label='add my wallpaper', command=lambda: add_photo(po, cb))
config_menu.add_command(label='set default wallpaper', command=lambda: set_default(po))

menubar.add_command(label='help', command=call_help)

po.use_img()

root.config(menu=menubar)
root.mainloop()
