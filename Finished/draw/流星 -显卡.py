import tkinter as tk
from OpenGL.GL import *
from pyopengltk import OpenGLFrame

# 1. 定义一个 OpenGL 画布类
class GLCanvas(OpenGLFrame):
    def initgl(self):
        # 初始化：设置背景色为深灰
        glClearColor(0.1, 0.1, 0.1, 1.0)

    def redraw(self):
        # 每一帧的渲染逻辑：
        glClear(GL_COLOR_BUFFER_BIT)  # 清空屏幕
        
        # 画一个黄色的三角形
        glBegin(GL_TRIANGLES)
        glColor3f(1.0, 1.0, 0.0)  # 黄色
        glVertex2f(0.0, 0.5)      # 顶点1：上方
        glVertex2f(-0.5, -0.5)    # 顶点2：左下
        glVertex2f(0.5, -0.5)     # 顶点3：右下
        glEnd()

        self.tkSwapBuffers()      # 刷新显示

# 2. 创建 Tkinter 窗口
root = tk.Tk()
root.title("极简 Tkinter + OpenGL")

# 3. 把 OpenGL 画布放进去
gl_canvas = GLCanvas(root, width=400, height=400)
gl_canvas.pack()

# 4. 启动 Tkinter 主循环
root.mainloop()