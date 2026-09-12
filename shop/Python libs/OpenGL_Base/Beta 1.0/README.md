# OpenGL_Base v1.0

> A simple Python OpenGL wrapper library for beginners.
> 面向初学者的 Python OpenGL 简易封装库 | Beta v1.0
> Develop Team : WalkUp

## 📖 项目介绍

OpenGL_Base 在 PyOpenGL / GLUT 之上做了一层封装，简化2D、3D图形绘制。
内置绘图命令队列、帧率无关时间系统、图形标签动画控制，支持多后端：

- tkinter（pyopengltk，嵌入GUI窗口，推荐）
- glut 原生独立窗口
- pygame（预留接口，待实现）

✅ 特点：

1. 图形支持tag标记，调用`SetGraphic`动态控制旋转动画
2. `tick()` 获取delta_time，动画不受帧率影响
3. 内置颜色名解析，直接写`"red"`、`"blue"`，不用手动写RGB
4. 内置2D绘图：三角形、四边形、圆形、海龟绘图(Turtle)
5. 内置3D基础几何体：立方体、球体、圆柱、圆锥、正四面体

> ⚠️ 警告：本库兼容性一般，部分环境可能崩溃，请知悉。

## 📦 依赖安装

```bash
pip install PyOpenGL PyOpenGL_accelerate pyopengltk 
```

✨ 内置功能列表

OpenGL 核心静态方法

-  OpenGL.Info() ：打印库版本信息
-  OpenGL.Init(master, backend, width, height) ：初始化OpenGL上下文、窗口
-  OpenGL.tick(frame=60) ：获取帧间隔delta_time，单位秒
-  OpenGL.SetGraphic(tag, **kwargs) ：修改图形动画属性（旋转开关、转速、旋转轴）
-  OpenGL.resolve_color_list() ：颜色名字转RGB(0~1)
-  OpenGL.redirect(master) ：多窗口重定向
-  OpenGL.Render() ：手动渲染（tk后端一般自动渲染）

Graphics_2D 二维绘图

-  Triangle()  三角形
-  Square()  四边形
-  Circle()  圆形/正多边形，支持分段渐变颜色
- 海龟绘图 Turtle： forward  /  backward  /  left  /  right  / 抬落笔 / 填充

Graphics_3D 三维几何体

-  Cube()  立方体
-  Sphere()  球体
-  Cylinder()  圆柱体
-  Cone()  圆锥
-  Tetrahedron()  正四面体

🚀 最简示例（Tkinter后端，旋转立方体）

python

import tkinter as tk
from OpenGL_Base import OpenGL

root = tk.Tk()
root.title("Demo")

# 初始化tk后端，800×600窗口

OpenGL.Init(root, backend="tkinter", width=800, height=600)

# 绘制立方体，设置tag为cube1

OpenGL.Graphics_3D.Cube(tag="cube1")

# 开启旋转，Y轴旋转，每秒60度

OpenGL.SetGraphic("cube1", rotate_state=True, after=60, rot_y=1)

root.mainloop()
 

📝 动画控制说明

 OpenGL.SetGraphic(tag, rotate_state=True,while_rot=True,after=60,angle=0,rot_x=0,rot_y=1,rot_z=0) 

-  rotate_state ：是否开启旋转 bool
-  while_rot ：True=持续随时间旋转；False=固定angle角度
-  after ：每秒旋转度数
-  angle ：当前累计旋转角度
-  rot_x/rot_y/rot_z ：旋转轴向量
