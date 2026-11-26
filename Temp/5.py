import turtle, math, colorsys

screen = turtle.Screen()
screen.bgcolor("black")
screen.colormode(1.0)
screen.tracer(0)

t = turtle.Turtle()
t.hideturtle()
t.pensize(2)
N, S = 1400, 60

for i in range(40):
    # 还原被乱码遮挡的数学逻辑（i/10 等）
    a = i / 10 + math.pi
    p = math.exp(math.cos(a)) - 2 * math.cos(4 * a) + math.sin(a / 12) ** 5
    # 还原坐标计算
    x = i + 60 * math.cos(p)
    y = i + 60 * math.sin(p)
    
    # 还原颜色设置：colorsys.hsv_to_rgb
    t.color(colorsys.hsv_to_rgb(i / 30, 1, 1))
    
    # 还原 goto 与绘制逻辑
    t.goto(10 * x, 10 * y)
    if i == 20:
        t.goto(10 * 60, 0)
        t.goto(10 * x, 10 * y)
        t.goto(0, 0)
    
    if i == 30:
        screen.update()

screen.exitonclick()  # 补全结尾，点击窗口退出
