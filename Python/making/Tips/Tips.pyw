import tkinter as tk
import os
import System32
from tkinter import messagebox
import turtle as tx

class main:
    def __init__(self):
            self.root = tk.Tk()
            self.root.geometry(f"1500x800+{System32.infomation['screen_w'] // 2 - 1500 // 2}+{System32.infomation['screen_h'] // 2 - 800 // 2}")
            self.root.title("Tips")
            self.root.resizable(False, False)
                
            # 创建画布
            self.black_frame = tk.Frame(self.root, bg='white')
            self.black_frame.pack(fill=tk.BOTH, expand=True)
            width, height = 500, 250
            self.c = tk.Canvas(self.black_frame, width=width, height=height, bg='white', highlightthickness=0)
            self.c.pack(fill=tk.BOTH, expand=True)
            
            # 设置turtle
            self.ts = tx.TurtleScreen(self.c)
            self.ts.setworldcoordinates(-width/2, -height/2, width/2, height/2)
            self.t = tx.RawTurtle(self.ts)
            self.t.hideturtle()
            
            def clear():
                if self.root.winfo_children():
                    for widget in self.root.winfo_children():
                        widget.destroy()
                # 创建画布
                self.black_frame = tk.Frame(self.root, bg='white')
                self.black_frame.pack(fill=tk.BOTH, expand=True)
                width, height = 500, 250
                self.c = tk.Canvas(self.black_frame, width=width, height=height, bg='white', highlightthickness=0)
                self.c.pack(fill=tk.BOTH, expand=True)
                
                # 设置turtle
                self.ts = tx.TurtleScreen(self.c)
                self.ts.setworldcoordinates(-width/2, -height/2, width/2, height/2)
                self.t = tx.RawTurtle(self.ts)
                self.t.hideturtle()

            def time_set():
                clear()
                time_button = tk.Button(self.root, text='Time', bg='white', width=10, command=time_set, font=('Microsoft YaHei', 12))
                time_button.place(x=0, y=0)
                
                
                
            time_button = tk.Button(self.root, text='Time', bg='white', width=10, command=time_set, font=('Microsoft YaHei', 12))
            time_button.place(x=0, y=0)

            self.root.mainloop()
            
    def run():
        main()

main.run()