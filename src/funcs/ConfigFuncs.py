import re
import os.path
from tkinter import *
from funcs.Funcs import switch_wallpaper
from tkinter.filedialog import askopenfilename

# 设置默认壁纸
def set_default(pho: object):
    top = Toplevel()
    frm = Frame(top)
    frm.grid(padx=6, pady=5)
    Label(frm, text='请输入要设置的默认默认壁纸编号').grid(row=0, column=0, columnspan=2, padx=5, pady=10)
    order_ent = Entry(frm, width=6)
    order_ent.grid(row=1, column=0, sticky='we')
    order_ent.bind('<Return>', lambda *args: opera())

    def opera():
        try:
            order = int(order_ent.get())
        except Exception:
            print("请输入数字类型")
            return
        order = (pho.count if order % pho.count == 0 else order % pho.count)-1
        switch_wallpaper(pho, order)
        pattern = r'(default_order:\s*)(\d+)'
        res_pattern = r'\g<1>' + str(order)
        with open('../resource_/default_setting.txt', 'r') as f:
            data = f.read()
        data = re.sub(pattern, res_pattern, data)
        with open('../resource_/default_setting.txt', 'w') as f:
            f.write(data)
    (Button(frm, text='<confirm>', relief='flat', fg='blue', command=opera)
        .grid(row=1, column=1, pady=5, sticky='we'))

def add_photo(pho, combobox):
    filepath = askopenfilename()
    try:
        with open(filepath, 'rb') as f:
            data = f.read()
        save_path = os.path.abspath('../resource_/photos/new/photo'+str(pho.count+1)+'.png')
        pho.count += 1
        with open(save_path, 'wb') as f:
            f.write(data)
    except Exception:
        print('添加图片时发生错误!')
    pho.add_photo(filepath)
    photo_index = list(combobox['values'])
    photo_index.append(pho.count)
    combobox['values'] = photo_index
