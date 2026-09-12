import tkinter as tk
from tkinter import messagebox
import turtle as tx
import time as tm
import random as r
import math

root = tk.Tk()
root.geometry("500x240+580+360")
root.title("神秘的按钮")
root.resizable(False, False)
root.update()

def GeatSeeStartPlace():
    # 销毁初始窗口
    root.after(500)
    root.destroy()
    
    # 创建主窗口
    HappyNewYear = tk.Tk()
    HappyNewYear.configure(bg="white", cursor="none")
    HappyNewYear.attributes("-fullscreen", True)
    
    # 创建画布
    black_frame = tk.Frame(HappyNewYear, bg='white')
    black_frame.pack(fill=tk.BOTH, expand=True)
    width, height = 500, 250
    c = tk.Canvas(black_frame, width=width, height=height, bg='white', highlightthickness=0)
    c.pack(fill=tk.BOTH, expand=True)
    
    # 设置turtle
    ts = tx.TurtleScreen(c)
    ts.setworldcoordinates(-width/2, -height/2, width/2, height/2)
    t = tx.RawTurtle(ts)
    t.hideturtle()
    ts.bgcolor("white")

    def Write(text, size):
        t.write(str(text), align="center", font=("Microsoft YaHei", size, "normal"))

    colors = ["red", "orange", "yellow", "green", "lime", "blue", "navy", "lightblue", 
              "purple", "pink", "#4CAF50", "#55FF55", "coral", "#FF6B6B", "#FFD93D",
              "#6BCF7F", "#4D96FF", "#FF7B7B", "#FF8D29", "#6A67CE"]

    t.speed(0)
    # tm.sleep(2)

    for _ in range(3):
        # 写"新"字
    
        t.penup()
        t.goto(110, -130)
        t.pencolor(colors[r.randint(0, len(colors)-1)])
        Write("新", 120)
        
        # 更新窗口
        ts.update()
        
        # 写"年"字
        t.seth(0)
        t.fd(300)
        t.right(90)
        t.fd(150)
        t.pencolor(colors[r.randint(0, len(colors)-1)])
        Write("年", 120)
        
        ts.update()
        
        # 写"快"字
        t.seth(0)
        t.fd(300)
        t.left(90)
        t.fd(150)
        t.pencolor(colors[r.randint(0, len(colors)-1)])
        Write("快", 120)
        
        ts.update()
        
        # 写"乐"字
        t.seth(0)
        t.fd(300)
        t.right(90)
        t.fd(150)
        t.pencolor(colors[r.randint(0, len(colors)-1)])
        Write("乐", 120)
    
        ts.update()
        tm.sleep(1)
        t.clear()
        tm.sleep(1)
        ts.tracer(0)

    ts.tracer(1)
    tm.sleep(3)
    
    # 清空画布
    t.clear()
    ts.bgcolor("black")
    tm.sleep(2)
    
    # 烟花效果
    for 烟花 in range(100):
        x = r.randint(10, 1000)
        t.penup()
        t.goto(x, -950)
        t.pendown()
        t.seth(90)
        t.pencolor(colors[r.randint(0, len(colors)-1)])
        walk =  r.randint(90, 750)
        t.penup()
        t.fd(walk)
        t.pendown()
        for 爆炸 in range(100):
            ts.tracer(0)
            t.seth(r.randint(0, 390))
            length = r.randint(35, 60)
            t.pencolor(colors[r.randint(0, len(colors)-1)])
            t.fd(length)
            t.bk(length)
            ts.tracer(1)
        t.seth(90)
        t.penup()
        t.bk(walk)
        t.pendown()
        ts.update()
        tm.sleep(0.03)
        # t.clear()

    HappyNewYear.after(2000)
    HappyNewYear.destroy()

    祝福语()

def 祝福语():
    def 显示大祝():
        祝Win = tk.Tk()
        祝Win.geometry("500x450+580+280")
        祝Win.title("祝福")
        祝Win.configure(bg='white')
        
        # 添加"祝"字
        tk.Label(祝Win, text="祝", fg="pink", 
                font=("Microsoft YaHei", 200), bg='white').place(x=105, y=20)
        
        祝Win.after(2000, 祝Win.destroy)
        祝Win.mainloop()
    
    def 显示多条祝福():
        祝福语列表 = ["新年学业双丰收，金榜题名步步高！",
                    "新春启智，学业有成，前程似锦！",
                    "新年新起点，学业创新高！",
                    "金榜题名迎新春，才思泉涌贺新年！",
                    "新年智慧开，考试门门优！",
                    "新春福气伴，学业节节升！",
                    "龙年跃龙门，学业跃新高！",
                    "新年新气象，学业新突破！",
                    "福满新春，慧满学业！",
                    "新年开鸿运，学业展宏图！",
                    "春风得意马蹄疾，学业有成步步稳！",
                    "新年添才气，考场创佳绩！",
                    "新春送福至，学业送喜来！",
                    "新年智慧涨，考试信心足！",
                    "龙年腾飞，学业腾达！",
                    "新年新目标，学业新成就！",
                    "新春纳才，学业纳福！",
                    "新年才华溢，学业成绩优！",
                    "福启新年，智启学业！",
                    "新年思路通，考试路路顺！",
                    "龙年行大运，学业行大道！",
                    "新年才思广，学业进步快！",
                    "新春智慧门开，学业喜报频传！",
                    "新年智力升级，成绩全面开花！",
                    "福气迎新年，才气冠学业！",
                    "新年开智慧花，结学业硕果！",
                    "龙年跃书山，学业跨学海！",
                    "新年新知识，学业新高度！",
                    "春风送福至，才思送分来！",
                    "新年智力爆发，考试轻松拿下！",
                    "新春智慧满格，学业成绩满分！",
                    "新年才华横溢，学业辉煌腾达！",
                    "福满新年，智满课堂！",
                    "新年学习力爆棚，考试成绩亮眼！",
                    "龙年才思如泉涌，学业进步似龙腾！",
                    "新年新思维，学业新跨越！",
                    "新春开智，学业开挂！",
                    "新年灵感不断，学业突破不停！",
                    "福启新岁，智启前程！",
                    "新年学习效率高，考试成绩创新高！",
                    "龙年智慧开，学业好运来！",
                    "新年知识储备足，考场发挥超常稳！",
                    "新春送才气，学业送喜气！",
                    "新年思维敏捷，学业捷报频传！",
                    "福到新年，智到学业！",
                    "新年学习动力足，成绩进步速度快！",
                    "龙年才思敏捷，学业突飞猛进！",
                    "新年智力投资，学业高额回报！",
                    "新春智慧加持，学业成绩加持！",
                    "新年新智慧，学业新辉煌！"]
        
        colors = ["red", "orange", "yellow", "green", "lime", "blue", "navy", "lightblue", 
                  "purple", "pink", "black", "#4CAF50", "#55FF55", "coral", "#FF6B6B",
                  "#FFD93D", "#6BCF7F", "#4D96FF", "#FF7B7B", "#FF8D29", "#6A67CE"]
        
        窗口列表 = []
        
        # 创建主窗口
        主窗口 = tk.Tk()
        主窗口.withdraw()  # 隐藏主窗口
        
        def 创建祝福窗口(序号):
            if 序号 >= 100:  # 只创建70个窗口
                return
            
            祝福Win = tk.Toplevel(主窗口)
            x = r.randint(0, 1400)
            y = r.randint(0, 1000)
            祝福Win.geometry(f"300x80+{x}+{y}")
            祝福Win.title(f"祝福{序号+1}")
            祝福Win.attributes('-topmost', True)  # 窗口置顶
            
            # 随机选择祝福语和颜色
            随机祝福 = r.choice(祝福语列表)
            随机颜色 = r.choice(colors)
            
            标签 = tk.Label(祝福Win, text=随机祝福, fg=随机颜色, 
                    font=("Microsoft YaHei", 12, "bold"), 
                    wraplength=280, justify="center")
            标签.pack(pady=20)
            
            窗口列表.append(祝福Win)
            
            # 0.1秒后创建下一个窗口
            主窗口.after(100, lambda: 创建祝福窗口(序号 + 1))
        
        # 开始创建窗口序列
        创建祝福窗口(0)
        
        主窗口.mainloop()
    
    # 先显示大"祝"字
    显示大祝()
    # 然后显示多条祝福
    显示多条祝福()

def close():
    root.destroy()

def StartButton():
    NewYearText = tk.Label(root, text="点一下有好运>>>", fg="lightblue", 
                    font=("Microsoft YaHei", 40)).place(x=40, y=50)
    NewYearButton = tk.Button(root, text=">>>  ？ <<<", bg="green", 
                        fg="white", command=GeatSeeStartPlace, width=20, height=1).place(x=170, y=145)
    closebutton = tk.Button(root, text="✖", fg="red", 
                    command=close, width=3, height=0).place(x=470, y=0)

def GiveRun():
    StartButton()

if __name__=="__main__":
    GiveRun()
    root.mainloop()