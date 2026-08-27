import tkinter as tk
import System32
import time as tm

# System32.Get_Administrtor_permissions()
System32.Adaptation_DPI_Hight()

class main:
    def __init__(self):
        self.c = ""
        # make target
        self.root = tk.Tk()
        
        # Safety Update
        def update():
            self.root.update()
            self.root.after(800, self.root.update)
            self.root.update()
            self.root.update_idletasks()
            self.root.update()
            self.root.after(800, self.root.update)
            self.root.update()
        
        # Main Window
        update()
        self.root.title('counter')
        update()
        self.root.geometry(f'600x400+{System32.infomation['screen_w'] // 2 - 600 // 3}+{System32.infomation['screen_h'] // 2 - 400 // 3}')
        update()
        self.root.resizable(False, False)
        update()
        
        # Text_loader
        self.text_loader = tk.Text(self.root, font=('Microsoft YaHei', 48))
        update()
        self.text_loader.place(width=550, height=80, x=20, y=30)
        update()
        # __init__
        self.text_loader.config(state=tk.DISABLED)
        update()
        
        def disk(Error):
            temp = tk.Toplevel(self.root)
            temp.title('Tip')
            temp.resizable(False, False)
            center_x = System32.infomation['screen_w'] // 2 - 400 // 2
            center_y = System32.infomation['screen_h'] // 2 - 150 // 2
            
            temp.geometry(f'0x150+{center_x}+{center_y}')
            
            tk.Label(temp, text=Error, font=('Microsoft YaHei', 18), anchor='center').place(relx=0.5, rely=0.5, anchor='center')
            
            for i in range(0, 401):
                current_x = center_x - i // 2
                temp.geometry(f'{i}x150+{current_x}+{center_y}')
                self.root.update()
                
            tm.sleep(2)
            
            for i in range(400, -1, -1):
                current_x = center_x - i // 2
                temp.geometry(f'{i}x150+{current_x}+{center_y}')
                self.root.update()
                
            temp.destroy()
        
        # I/O insert
        def io(text):
            self.c = self.text_loader.get("1.0", tk.END)+text
            update()
            self.text_loader.config(state=tk.NORMAL)
            update()
            self.text_loader.insert(tk.END, text)
            update()
            self.text_loader.config(state=tk.DISABLED)
            update()
        
        # Button_DSL
        def _percent():
            s = self.text_loader.get("1.0", tk.END)
            if not s[-2].isdigit():
                disk('There are no numbers in front.')
                return False
            io('%')
        
        def _add():
            s = self.text_loader.get("1.0", tk.END)
            if not s[-2].isdigit():
                disk('There are no numbers in front.')
                return False
            io('+')
        
        def _back():
            s = self.text_loader.get("1.0", tk.END)
            if not s[-2].isdigit():
                disk('There are no numbers in front.')
                return False
            io('-')
        
        def _ride():
            s = self.text_loader.get("1.0", tk.END)
            if not s[-2].isdigit():
                disk('There are no numbers in front.')
                return False
            io('*')
        
        def _besides():
            s = self.text_loader.get("1.0", tk.END)
            if not s[-2].isdigit():
                disk('There are no numbers in front.')
                return False
            io('/')

        def num0():
            io('0')

        def num1():
            io('1')

        def num2():
            io('2')

        def num3():
            io('3')

        def num4():
            io('4')

        def num5():
            io('5')

        def num6():
            io('6')

        def num7():
            io('7')

        def num8():
            io('8')

        def num9():
            io('9')

        def back():
            self.c = self.text_loader.get("1.0", tk.END)[:-2]
            self.text_loader.delete('1.0', tk.END)
            for i in self.c:
                self.text_loader.insert(tk.END, i)

        def compile():
            try:
                answer = eval(self.c)
                io(answer)
            except:
                disk('The formula is incorrect.')
        
        tk.Button(self.root, text='    %    ', command=_percent, font=('Microsoft YaHei', 18, 'bold')).place(x=20, y=130)
        tk.Button(self.root, text='    +    ', command=_add, font=('Microsoft YaHei', 18, 'bold')).place(x=140, y=130)
        tk.Button(self.root, text='    -    ', command=_back, font=('Microsoft YaHei', 18, 'bold')).place(x=260, y=130)
        tk.Button(self.root, text='    *    ', command=_ride, font=('Microsoft YaHei', 18, 'bold')).place(x=380, y=130)
        tk.Button(self.root, text='    /    ', command=_besides, font=('Microsoft YaHei', 18, 'bold')).place(x=500, y=130)
        tk.Button(self.root, text='    0    ', command=num0, font=('Microsoft YaHei', 18, 'bold')).place(x=100, y=300)
        
        # Display
        self.root.mainloop()
    
    def run():
        main()

main.run()