import tkinter as tk
from tkinter import ttk
import time as tm
import System32

System32.Adaptation_DPI_Hight()

class main:
    def __init__(self):
        self.c = ""
        self.root = tk.Tk()
        
        # 安全且精简的刷新函数
        def update():
            self.root.update_idletasks()
            self.root.update()
        
        # Main Window
        self.root.title('Counter')
        screen_w, screen_h = System32.infomation['screen_w'], System32.infomation['screen_h']
        x = screen_w // 2 - 450 // 2
        y = screen_h // 2 - 500 // 2
        self.root.geometry(f'450x500+{x}+{y}')
        self.root.resizable(False, False)
        
        # Text_loader (显示屏)
        self.text_loader = tk.Text(self.root, font=('Microsoft YaHei', 36), bd=0, highlightthickness=0)
        self.text_loader.place(width=410, height=80, x=20, y=40)
        self.text_loader.config(state=tk.DISABLED)
        
        # 错误提示弹窗 (带动画效果)
        def disk(Error):
            temp = tk.Toplevel(self.root)
            temp.title('Tip')
            temp.resizable(False, False)
            
            center_x = screen_w // 2 - 400 // 2
            center_y = screen_h // 2 - 150 // 2
            
            tk.Label(temp, text=Error, font=('Microsoft YaHei', 18), anchor='center').place(relx=0.5, rely=0.5, anchor='center')
            
            # 展开动画
            def expand(i=0):
                if i <= 400:
                    current_x = center_x - i // 2
                    temp.geometry(f'{i}x150+{current_x}+{center_y}')
                    temp.after(10, lambda: expand(i + 10)) 
            
            # 收缩并销毁动画
            def shrink(i=400):
                if i >= 0:
                    current_x = center_x - i // 2
                    temp.geometry(f'{i}x150+{current_x}+{center_y}')
                    temp.after(10, lambda: shrink(i - 10))
                else:
                    temp.destroy()
            
            expand()
            temp.after(2000, shrink)
        
        # I/O 插入逻辑
        def io(text):
            self.text_loader.config(state=tk.NORMAL)
            self.text_loader.insert(tk.END, text)
            self.text_loader.config(state=tk.DISABLED)
            update()
            self.c = self.text_loader.get("1.0", tk.END).strip() 

        # 运算符防呆检查
        def check_last_digit():
            s = self.c
            if not s or not s[-1].isdigit():
                disk('There are no numbers in front.')
                return False
            return True
        
        def _percent():
            if check_last_digit(): io('%')
        def _add():
            if check_last_digit(): io('+')
        def _sub(): # 改名避免与 back 混淆
            if check_last_digit(): io('-')
        def _ride():
            if check_last_digit(): io('*')
        def _besides():
            if check_last_digit(): io('/')

        # 数字键
        def num(n):
            io(str(n))

        # --- 新增：清除逻辑 ---
        def clear_all():
            self.text_loader.config(state=tk.NORMAL)
            self.text_loader.delete("1.0", tk.END)
            self.text_loader.config(state=tk.DISABLED)
            self.c = ""
            update()

        # 退格键
        def back():
            self.text_loader.config(state=tk.NORMAL)
            self.text_loader.delete("end-2c") 
            self.text_loader.config(state=tk.DISABLED)
            self.c = self.text_loader.get("1.0", tk.END).strip()
            update()

        # 计算逻辑
        def compile():
            try:
                answer = eval(self.c)
                self.text_loader.config(state=tk.NORMAL)
                self.text_loader.delete("1.0", tk.END)
                io(str(answer))
            except Exception:
                disk('The formula is incorrect.')
        
        # ================= UI 重新排版设计 (4列布局) =================
        
        # 定义按钮尺寸常量
        # 窗口宽450，左右留白各20，剩余410。
        # 分为4列：410 / 4 ≈ 100px 宽。
        btn_w = 95  # 按钮宽度
        btn_h = 60  # 按钮高度
        gap = 6     # 间隙
        
        # 计算起始X坐标以实现整体居中
        total_width = 4 * btn_w + 3 * gap
        start_x = (450 - total_width) // 2
        
        y_cursor = 150 # 起始Y坐标
        
        row1_ops = [('%', _percent), ('+', _add), ('-', _sub), ('*', _ride)]
        for idx, (text, cmd) in enumerate(row1_ops):
            ttk.Button(self.root, text=text, command=cmd).place(
                x=start_x + idx * (btn_w + gap), y=y_cursor, width=btn_w, height=btn_h
            )
        y_cursor += btn_h + gap
        
        row2_mix = [(7, lambda: num(7)), (8, lambda: num(8)), (9, lambda: num(9)), ('/', _besides)]
        for idx, item in enumerate(row2_mix):
            text, cmd = item
            ttk.Button(self.root, text=text, command=cmd).place(
                x=start_x + idx * (btn_w + gap), y=y_cursor, width=btn_w, height=btn_h
            )
        y_cursor += btn_h + gap

        row3_mix = [(4, lambda: num(4)), (5, lambda: num(5)), (6, lambda: num(6)), ('C', clear_all)]
        for idx, item in enumerate(row3_mix):
            text, cmd = item
            ttk.Button(self.root, text=text, command=cmd).place(
                x=start_x + idx * (btn_w + gap), y=y_cursor, width=btn_w, height=btn_h
            )
        y_cursor += btn_h + gap

        row4_mix = [(1, lambda: num(1)), (2, lambda: num(2)), (3, lambda: num(3)), ('=', compile)]
        for idx, item in enumerate(row4_mix):
            text, cmd = item
            ttk.Button(self.root, text=text, command=cmd).place(
                x=start_x + idx * (btn_w + gap), y=y_cursor, width=btn_w, height=btn_h
            )
        y_cursor += btn_h + gap
        
        # 0 号键占两格宽
        ttk.Button(self.root, text='0', command=lambda: num(0)).place(
            x=start_x, y=y_cursor, width=btn_w * 2 + gap, height=btn_h
        )
        
        # 退格键
        ttk.Button(self.root, text='<-', command=back).place(
            x=start_x + 2 * (btn_w + gap) + btn_w, y=y_cursor, width=btn_w, height=btn_h
        )
        
        ttk.Button(self.root, text='<-', command=back).place(
            x=start_x + 2 * (btn_w + gap), y=y_cursor, width=btn_w * 2 + gap, height=btn_h
        )

        self.root.mainloop()
    
    @staticmethod
    def run():
        main()

if __name__ == "__main__":
    main.run()