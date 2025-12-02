class IndexMaker:
    def __init__(self, content_text_, index_text_):
        self.index = 1
        self.content_text = content_text_
        self.content_text.bind('<Control-v>', lambda event: self.track_paste(event))
        self.index_text = index_text_
        self.index_text.insert('end', f'{self.self_increase()}')
        self.content_text.bind('<Return>', self.enter_track)
        self.content_text.bind('<BackSpace>', self.delete_last_line)

    def self_increase(self):
        self.index += 1
        return self.index - 1

    # 监视回车操作
    def enter_track(self, event):
        self.index_text.insert('end', f'\n{self.index}')
        self.index += 1     # 更新行号数据
        # 更新行号显示区域显示滚动轴更新
        self.index_text.see(self.content_text.index('end'))
        self.content_text.see('end')

    def delete_last_line(self, event):
        try:
            begin = self.content_text.index('sel.first')
            end = self.content_text.index('sel.last')
            step = int(float(end)) - int(float(begin))
            if step == self.index - 1:  # 如果全选进行删除，执行保留第一行操作
                step -= 1

            last_line_start = self.index_text.index(f'end -{step + 1} lines lineend')
            last_line_end = self.index_text.index('end -1 lines lineend')
            self.index -= step - 1  # index 处理 1
        except:
            if (self.index_text.index('end -1 lines').split('.')[0] == self.content_text.index('insert').split('.')[0]
                    and self.content_text.index('insert').split('.')[-1] != '0'):
                return
            if (self.index_text.index('end-1 lines') == '1.0' or
                    (self.content_text.index('insert') == '1.0')):
                return
            last_line_start = self.index_text.index('end -2 lines lineend')
            last_line_end = self.index_text.index('end -1 lines lineend')
        # 获取最后一行的起始位置

        self.index_text.delete(last_line_start, last_line_end)
        self.index -= 1  # index 处理 2

    def track_paste(self, event):
        step = [0]
        self.content_text.after(10, self.index_update, step)

    # 该函数用于撤销或重做操作后的行号更新
    def index_update(self, step: list):
        # 获取操作前后的行索引
        index_old = int(self.content_text.index('end').split('.')[0])
        index_new = int(self.index_text.index('end').split('.')[0])
        # 计算变化行数
        step[0] = abs(index_old - index_new)
        # 更新行号
        for i in range(step[0]):
            self.index_text.insert('end', f'\n{self.index}')
            self.index += 1
        # 更行行号纵轴滚动显示
        self.index_text.see(self.content_text.index('end'))
        self.content_text.see('end')
