from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import time as tm
import math
from tkinter import messagebox

# ===================== 全局库状态变量 =====================
# GLUT窗口ID
window = 0
# 多窗口管理，保存各个master的字符串标识
windows = []
# tkinter OpenGLFrame实例对象
_internal_tk_frame = None
# 绘制命令队列，所有图形绘制函数把draw_cmd压入这里，每一帧统一执行
_draw_list = []
# tk OpenGL上下文是否初始化完成标记
_tk_gl_ready = False
# tk循环调度锁，防止重复注册after回调
_tk_loop_scheduled = False
# tick时间戳：上一帧的系统时间，用于计算delta_time，实现帧率无关动画
_last_tick_time = 0.0

def Info():
    """
    库信息打印函数
    打印库名称、版本、开发团队、兼容性警告
    """
    print('This lib is designed for beginners of OpenGL.')
    tm.sleep(0.08)
    print('This lib has relatively poor compatibility.')
    tm.sleep(0.08)
    print('MayBe will crash.')
    tm.sleep(0.08)
    print('Please understand.')
    tm.sleep(0.08)
    print('Name : OpenGL_Base')
    tm.sleep(0.08)
    print('Version : 1.0')
    tm.sleep(0.08)
    print('Development Team : WalkUp')

# 图形tag管理字典，key为自定义字符串tag，value存储图形全部参数+attributes旋转属性
Set_Graphic = dict()


class OpenGL:
    """
    OpenGL_Base主类
    封装后端切换、颜色解析、窗口初始化、SetGraphic动画控制、tick时间系统
    """
    # 当前使用的后端："tkinter" / "self"(glut原生窗口) / "pygame"
    backend = None

    # 颜色名字映射表，字符串颜色名转OpenGL RGB(0~1)元组
    COLOR_MAP = {
        "red": (1.0, 0.0, 0.0),
        "green": (0.0, 1.0, 0.0),
        "blue": (0.0, 0.0, 1.0),
        "white": (1.0, 1.0, 1.0),
        "black": (0.0, 0.0, 0.0),
        "yellow": (1.0, 1.0, 0.0),
        "cyan": (0.0, 1.0, 1.0),
        "magenta": (1.0, 0.0, 1.0),
        "orange": (1.0, 0.5, 0.0),
        "purple": (0.6, 0.0, 1.0),
        "pink": (1.0, 0.3, 0.6)
    }

    @staticmethod
    def SetGraphic(target,**kwargs):
        """
        修改已经创建tag图形的动画属性
        调用格式：OpenGL.SetGraphic(tag字符串, rotate_state=True,while_rot=True,after=60,angle=0,rot_x=0,rot_y=1,rot_z=0)
        :param target: 图形创建时传入的tag字符串
        :param kwargs: 可传入键：rotate_state,while_rot,after,angle,rot_x,rot_y,rot_z
            rotate_state: bool 是否开启旋转
            while_rot: bool True=持续随时间旋转；False=固定angle角度
            after: float 每秒旋转多少度，帧率无关
            angle: float 当前累计旋转角度
            rot_x,rot_y,rot_z: 旋转轴向量
        """
        if target not in Set_Graphic:
            return
        attr = Set_Graphic[target]["attributes"]
        for k,v in kwargs.items():
            if k in attr:
                attr[k] = v

    @staticmethod
    def tick(frame=60):
        """
        获取帧时间差delta_time，实现帧率无关动画
        调用格式 delta = OpenGL.tick(frame=60)
        :param frame: 目标帧率，仅第一次生效
        :return: delta_time 单位秒，两帧之间时间间隔
        """
        global _last_tick_time
        now = tm.time()
        if _last_tick_time == 0.0:
            delta = 1.0 / frame
        else:
            delta = now - _last_tick_time
        _last_tick_time = now
        return delta

    @staticmethod
    def resolve_color_list(color_input):
        """
        颜色列表解析工具，把字符串颜色名转为RGB元组，原样保留元组输入
        调用格式 out_list = OpenGL.resolve_color_list(["red",(0,1,0)])
        :param color_input: list[str | tuple] 颜色字符串或者rgb元组
        :return: list[tuple] 解析完成的rgb(0~1)列表
        """
        out = []
        for c in color_input:
            if isinstance(c, str) and c.lower() in OpenGL.COLOR_MAP:
                out.append(OpenGL.COLOR_MAP[c.lower()])
            else:
                out.append(c)
        return out

    @staticmethod
    def redirect(master):
        """
        多窗口重定向，记录master对象，设置全局window索引
        :param master: tk根对象或者其他窗口宿主
        :return: window索引编号
        """
        global window, windows
        key = str(master)
        if key not in windows:
            windows.append(key)
        window = windows.index(key)
        return window

    @staticmethod
    def Init(master, backend="tkinter", width=800, height=600):
        """
        初始化OpenGL上下文，选择后端，创建绘图窗口
        调用格式 OpenGL.Init(master,backend="tkinter",width=800,height=600)
        :param master: tk根实例，glut后端可随便传占位
        :param backend: "tkinter" / "self" / "pygame"
        :param width: 窗口宽度像素
        :param height: 窗口高度像素
        """
        global _internal_tk_frame, _tk_gl_ready, _tk_loop_scheduled, _draw_list, _last_tick_time
        OpenGL.redirect(master)
        OpenGL.backend = backend
        _draw_list.clear()
        Set_Graphic.clear()
        _tk_gl_ready = False
        _tk_loop_scheduled = False
        _last_tick_time = 0.0

        if backend == "self":
            # GLUT原生独立窗口后端
            glutInit()
            glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)
            win_id = glutCreateWindow("OpenGL_Base")
            global window
            window = win_id

        elif backend == "tkinter":
            # tkinter + pyopengltk嵌入后端
            import tkinter as tk
            from pyopengltk import OpenGLFrame

            class InnerOglFrame(OpenGLFrame):
                def initgl(self):
                    """OpenGL初始化回调，只执行一次"""
                    global _tk_gl_ready
                    glClearColor(0.0, 0.0, 0.0, 1.0)
                    glEnable(GL_DEPTH_TEST)
                    _tk_gl_ready = True

                def redraw(self):
                    """每一帧渲染回调，pyopengltk animate=1自动调用"""
                    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
                    glLoadIdentity()
                    w = self.winfo_width()
                    h = self.winfo_height()
                    if h < 1:
                        return
                    aspect = w / h
                    # 设置透视投影
                    glMatrixMode(GL_PROJECTION)
                    glLoadIdentity()
                    gluPerspective(45.0, aspect, 0.1, 100.0)
                    glMatrixMode(GL_MODELVIEW)
                    glTranslatef(0, 0, -5)
                    # 获取时间差，驱动所有旋转动画
                    delta = OpenGL.tick(frame=60)
                    # 执行全部压入队列的绘制命令
                    for fn in _draw_list:
                        fn(delta)

            _internal_tk_frame = InnerOglFrame(master, width=width, height=height)
            _internal_tk_frame.pack(fill=tk.BOTH, expand=True)
            _internal_tk_frame.animate = 1

        elif backend == "pygame":
            # pygame后端预留
            glClearColor(0.0, 0.0, 0.0, 1.0)
            glEnable(GL_DEPTH_TEST)
            glMatrixMode(GL_PROJECTION)
            glLoadIdentity()
            gluPerspective(45.0, width / height, 0.1, 100.0)
            glMatrixMode(GL_MODELVIEW)
        else:
            pass

    @staticmethod
    def Render(master=None, masterType="tkinter", auto_loop=True):
        """
        手动渲染接口；tk模式下pyopengltk animate=1已经自动渲染，此函数用于兼容其他后端
        :param master: 宿主窗口
        :param masterType: "self"/"tkinter"/"pygame"
        :param auto_loop: 是否开启tk的after循环调度
        """
        global _internal_tk_frame, _tk_gl_ready, _tk_loop_scheduled
        if master is not None:
            OpenGL.redirect(master)

        if masterType == "self":
            glutSetWindow(window)
            glutSwapBuffers()

        elif masterType == "tkinter":
            if _internal_tk_frame is not None and _tk_gl_ready:
                _internal_tk_frame._display()
                if auto_loop and not _tk_loop_scheduled:
                    _tk_loop_scheduled = True
                    root_win = _internal_tk_frame.master
                    def _tick():
                        global _tk_loop_scheduled
                        _tk_loop_scheduled = False
                        OpenGL.Render(master, masterType="tkinter", auto_loop=True)
                    root_win.after(16, _tick)

        elif masterType == "pygame":
            pass

    class Graphics_2D:
        """2D图形工具类：三角形、正方形、圆形 + 海龟绘图"""
        @staticmethod
        def Triangle(master=None, coordinates=((0, 1), (-1, -1), (1, -1)), color=[(1,0,0), (0,1,0), (0,0,1)], tag=None):
            """
            绘制2D三角形
            调用格式 OpenGL.Graphics_2D.Triangle(master=None,coordinates=((0,1),(-1,-1),(1,-1)),color=["red","green","blue"],tag="tri1")
            :param master: tk宿主，可选
            :param coordinates: 三个顶点坐标元组
            :param color: 每个顶点对应颜色列表，支持颜色字符串或者rgb元组
            :param tag: 字符串标记，传入后可使用SetGraphic控制旋转动画
            """
            out_color = OpenGL.resolve_color_list(color)
            attributes = {
                "rotate_state":False,
                "while_rot":True,
                "after":60,
                "angle":0.0,
                "rot_x":0,
                "rot_y":0,
                "rot_z":1
            }
            if tag is not None:
                Set_Graphic[tag] = {
                    "type":"Triangle",
                    "coordinates":coordinates,
                    "color":color,
                    "attributes":attributes
                }
            if master is not None:
                OpenGL.redirect(master)
            def draw_cmd(delta_time):
                glPushMatrix()
                if tag is not None and tag in Set_Graphic:
                    attr = Set_Graphic[tag]["attributes"]
                    if attr["rotate_state"]:
                        if attr["while_rot"]:
                            attr["angle"] += attr["after"] * delta_time
                        glRotatef(attr["angle"], attr["rot_x"], attr["rot_y"], attr["rot_z"])
                glBegin(GL_TRIANGLES)
                for idx, data in enumerate(coordinates):
                    if out_color and idx < len(out_color):
                        glColor3f(*out_color[idx])
                    glVertex2f(data[0], data[1])
                glEnd()
                glPopMatrix()
            _draw_list.append(draw_cmd)

        @staticmethod
        def Square(master=None, coordinates=((-1, 1), (1, 1), (1, -1), (-1, -1)),
                   color=[(1, 0, 0), (0, 1, 0), (0, 0, 1), (1, 1, 0)], tag=None):
            """
            绘制2D四边形（正方形）
            调用格式 OpenGL.Graphics_2D.Square(coordinates=((-1,1),(1,1),(1,-1),(-1,-1)),color=["red","green","blue","yellow"],tag="sq1")
            :param master: tk宿主
            :param coordinates: 4个顶点坐标
            :param color: 4顶点颜色列表
            :param tag: 动画控制标签
            """
            out_color = OpenGL.resolve_color_list(color)
            attributes = {
                "rotate_state":False,
                "while_rot":True,
                "after":60,
                "angle":0.0,
                "rot_x":0,
                "rot_y":0,
                "rot_z":1
            }
            if tag is not None:
                Set_Graphic[tag] = {
                    "type":"Square",
                    "coordinates":coordinates,
                    "color":color,
                    "attributes":attributes
                }
            if master is not None:
                OpenGL.redirect(master)
            def draw_cmd(delta_time):
                glPushMatrix()
                if tag is not None and tag in Set_Graphic:
                    attr = Set_Graphic[tag]["attributes"]
                    if attr["rotate_state"]:
                        if attr["while_rot"]:
                            attr["angle"] += attr["after"] * delta_time
                        glRotatef(attr["angle"], attr["rot_x"], attr["rot_y"], attr["rot_z"])
                glBegin(GL_QUADS)
                for idx, data in enumerate(coordinates):
                    if out_color and idx < len(out_color):
                        glColor3f(*out_color[idx])
                    glVertex2f(data[0], data[1])
                glEnd()
                glPopMatrix()
            _draw_list.append(draw_cmd)

        @staticmethod
        def Circle(master=None, cx=0, cy=0, radius=1, segments=36, sides=None, color=None, angle_ranges=None, tag=None):
            """
            2D圆/正多边形，支持角度区间渐变
            调用格式 OpenGL.Graphics_2D.Circle(cx=0,cy=0,radius=1,segments=36,sides=6,color=None,angle_ranges=[(0,120,"red"),(120,240,"green"),(240,360,"blue")],tag="c1")
            :param master: tk宿主
            :param cx,cy: 圆心坐标
            :param radius: 半径
            :param segments: 细分段数，sides=None生效
            :param sides: 不为None代表正N边形，覆盖segments
            :param color: 纯色模式颜色列表
            :param angle_ranges: 角度渐变区间 [(deg0,deg1,colorname),...]
            :param tag: 动画标签
            """
            DEFAULT_ANGLE = [(0, 120, "red"), (120, 240, "green"), (240, 360, "blue")]
            if color is None and angle_ranges is None:
                angle_ranges = DEFAULT_ANGLE
            out_color = OpenGL.resolve_color_list(color) if color is not None else None
            attributes = {
                "rotate_state":False,
                "while_rot":True,
                "after":60,
                "angle":0.0,
                "rot_x":0,
                "rot_y":0,
                "rot_z":1
            }
            if tag is not None:
                Set_Graphic[tag] = {
                    "type":"Circle",
                    "cx":cx,"cy":cy,"radius":radius,"segments":segments,"sides":sides,
                    "color":color,"angle_ranges":angle_ranges,
                    "attributes":attributes
                }
            if master is not None:
                OpenGL.redirect(master)
            def draw_cmd(delta_time):
                vert_count = sides if sides is not None else segments
                proc_ranges = []
                key_points = []
                use_direct_key = False
                glPushMatrix()
                if tag is not None and tag in Set_Graphic:
                    attr = Set_Graphic[tag]["attributes"]
                    if attr["rotate_state"]:
                        if attr["while_rot"]:
                            attr["angle"] += attr["after"] * delta_time
                        glRotatef(attr["angle"], attr["rot_x"], attr["rot_y"], attr["rot_z"])
                if angle_ranges is not None:
                    if isinstance(angle_ranges, tuple):
                        items = list(angle_ranges)
                        cnt = len(items)
                        step = 360.0 / cnt
                        for i, cname in enumerate(items):
                            d0 = i * step
                            d1 = (i + 1) * step
                            proc_ranges.append((d0, d1, cname))
                    elif all(isinstance(item, str) for item in angle_ranges):
                        cnt = len(angle_ranges)
                        step = 360.0 / cnt
                        for i, cname in enumerate(angle_ranges):
                            d0 = i * step
                            d1 = (i + 1) * step
                            proc_ranges.append((d0, d1, cname))
                    else:
                        proc_ranges = angle_ranges
                        all_two_tuple = True
                        for it in proc_ranges:
                            if not (isinstance(it,(tuple,list)) and len(it)==2 and all(isinstance(x,str) for x in it)):
                                all_two_tuple=False
                                break
                        if all_two_tuple:
                            seg_count = len(proc_ranges)
                            seg_step = 360.0 / seg_count
                            key_points = []
                            for idx,(c1,c2) in enumerate(proc_ranges):
                                d0 = idx * seg_step
                                d1 = (idx+1)*seg_step
                                r1,g1,b1 = OpenGL.resolve_color_list([c1])[0]
                                r2,g2,b2 = OpenGL.resolve_color_list([c2])[0]
                                key_points.append((math.radians(d0), r1,g1,b1))
                                key_points.append((math.radians(d1), r2,g2,b2))
                            use_direct_key = True
                        elif len(proc_ranges)==1 and isinstance(proc_ranges[0],(tuple,list)) and all(isinstance(x,str) for x in proc_ranges[0]):
                            flat = list(proc_ranges[0])
                            cnt = len(flat)
                            step = 360.0 / cnt
                            proc_ranges.clear()
                            for i,cname in enumerate(flat):
                                d0 = i*step
                                d1 = (i+1)*step
                                proc_ranges.append((d0,d1,cname))
                    if not use_direct_key:
                        key_points = []
                        for deg0,deg1,cname in proc_ranges:
                            r,g,b = OpenGL.resolve_color_list([cname])[0]
                            key_points.append((math.radians(deg1), r,g,b))
                        key_points.insert(0,(0.0,*key_points[-1][1:]))
                    glBegin(GL_TRIANGLE_FAN)
                    if out_color:
                        glColor3f(*out_color[0])
                    else:
                        glColor3f(1.0,1.0,1.0)
                    glVertex2f(cx, cy)
                    for i in range(vert_count + 1):
                        ang = 2.0 * math.pi * i / vert_count
                        rr = gg = bb = 0.0
                        for k_idx in reversed(range(len(key_points)-1)):
                            a0,r0,g0,b0 = key_points[k_idx]
                            a1,r1,g1,b1 = key_points[k_idx+1]
                            if a0 <= ang <= a1:
                                t = (ang - a0)/(a1 - a0)
                                rr = r0 + t*(r1-r0)
                                gg = g0 + t*(g1-g0)
                                bb = b0 + t*(b1-b0)
                                break
                        glColor3f(rr,gg,bb)
                        x = cx + radius * math.cos(ang)
                        y = cy + radius * math.sin(ang)
                        glVertex2f(x,y)
                    glEnd()
                else:
                    glBegin(GL_TRIANGLE_FAN)
                    if out_color:
                        glColor3f(*out_color[0])
                    else:
                        glColor3f(1.0,1.0,1.0)
                    glVertex2f(cx, cy)
                    for i in range(vert_count + 1):
                        angle = 2.0 * math.pi * i / vert_count
                        x = cx + radius * math.cos(angle)
                        y = cy + radius * math.sin(angle)
                        idx = i+1
                        if idx < len(out_color):
                            glColor3f(*out_color[idx])
                        glVertex2f(x, y)
                    glEnd()
                glPopMatrix()
            _draw_list.append(draw_cmd)

        @staticmethod
        def Turtle_SetCoordinate(x, y):
            """海龟绘图：设置海龟坐标"""
            Graphics_2D._turtle_x = float(x)
            Graphics_2D._turtle_y = float(y)

        @staticmethod
        def Turtle_forward(step):
            """海龟绘图：向前走step像素单位，pendown时画线"""
            import math
            rad = math.radians(Graphics_2D._turtle_angle)
            nx = Graphics_2D._turtle_x + step * math.cos(rad)
            ny = Graphics_2D._turtle_y + step * math.sin(rad)
            if Graphics_2D._turtle_pen_down:
                def draw_cmd():
                    glColor3f(*Graphics_2D._turtle_color)
                    glBegin(GL_LINES)
                    glVertex2f(Graphics_2D._turtle_x, Graphics_2D._turtle_y)
                    glVertex2f(nx, ny)
                    glEnd()
                _draw_list.append(draw_cmd)
            if Graphics_2D._turtle_filling:
                Graphics_2D._turtle_fill_buffer.append((nx, ny))
            Graphics_2D._turtle_x, Graphics_2D._turtle_y = nx, ny

        @staticmethod
        def Turtle_backward(step):
            """海龟绘图：向后移动step"""
            Graphics_2D.Turtle_forward(-step)

        @staticmethod
        def Turtle_left(angle):
            """海龟绘图：左转angle度"""
            Graphics_2D._turtle_angle += angle

        @staticmethod
        def Turtle_right(angle):
            """海龟绘图：右转angle度"""
            Graphics_2D._turtle_angle -= angle

        @staticmethod
        def Turtle_penup():
            """海龟绘图：抬笔，移动不画线"""
            Graphics_2D._turtle_pen_down = False

        @staticmethod
        def Turtle_pendown():
            """海龟绘图：落笔，移动绘制线段"""
            Graphics_2D._turtle_pen_down = True

        @staticmethod
        def Turtle_setcolor(color):
            """海龟绘图：设置画笔颜色，支持字符串名字"""
            c = OpenGL.resolve_color_list([color])[0]
            Graphics_2D._turtle_color = c

        @staticmethod
        def Turtle_BeginFill():
            """海龟绘图：开始填充，记录路径点"""
            Graphics_2D._turtle_filling = True
            Graphics_2D._turtle_fill_buffer.clear()
            Graphics_2D._turtle_fill_buffer.append((Graphics_2D._turtle_x, Graphics_2D._turtle_y))

        @staticmethod
        def Turtle_EndFill(color=None):
            """
            海龟绘图：结束填充，绘制填充多边形
            :param color: 填充颜色；不传使用画笔当前颜色
            """
            Graphics_2D._turtle_filling = False
            pts = Graphics_2D._turtle_fill_buffer
            if len(pts) < 3:
                return
            if color is None:
                fill_col = Graphics_2D._turtle_color
            else:
                fill_col = OpenGL.resolve_color_list([color])[0]
            def draw_cmd():
                glColor3f(*fill_col)
                glBegin(GL_POLYGON)
                for px, py in pts:
                    glVertex2f(px, py)
                glEnd()
            _draw_list.append(draw_cmd)


    class Graphics_3D:
        """3D图形工具类：立方体、球体、圆柱、圆锥、四面体"""
        @staticmethod
        def Cube(master=None, vertices=None, color=None, tag=None):
            """
            3D立方体
            调用格式 OpenGL.Graphics_3D.Cube(vertices=None,color=["red","green","blue"],tag="cube1")
            :param master: tk宿主
            :param vertices: 8个顶点列表，None使用默认立方体
            :param color: 6个面的颜色列表
            :param tag: 动画控制标签
            """
            if vertices is None:
                vertices = [
                    (-1, -1, -1), (1, -1, -1), (1, 1, -1), (-1, 1, -1),
                    (-1, -1, 1),  (1, -1, 1),  (1, 1, 1),  (-1, 1, 1)
                ]
            if color is None:
                color = [
                    (1,0,0),
                    (0,1,0),
                    (0,0,1),
                    (1,1,0),
                    (1,0,1),
                    (0,1,1)
                ]
            out_color = OpenGL.resolve_color_list(color)
            attributes = {
                "rotate_state":False,
                "while_rot":True,
                "after":60,
                "angle":0.0,
                "rot_x":0,
                "rot_y":1,
                "rot_z":0
            }
            faces = [
                [0,1,2,3],
                [4,5,6,7],
                [0,1,5,4],
                [2,3,7,6],
                [0,3,7,4],
                [1,2,6,5]
            ]
            if tag is not None:
                Set_Graphic[tag] = {
                    "type":"Cube",
                    "vertices":vertices,
                    "color":color,
                    "attributes":attributes
                }
            if master is not None:
                OpenGL.redirect(master)
            def draw_cmd(delta_time):
                glPushMatrix()
                if tag is not None and tag in Set_Graphic:
                    attr = Set_Graphic[tag]["attributes"]
                    if attr["rotate_state"]:
                        if attr["while_rot"]:
                            attr["angle"] += attr["after"] * delta_time
                        glRotatef(attr["angle"], attr["rot_x"], attr["rot_y"], attr["rot_z"])
                for face_idx, face in enumerate(faces):
                    glBegin(GL_QUADS)
                    c = out_color[face_idx] if face_idx < len(out_color) else (1.0,1.0,1.0)
                    glColor3f(*c)
                    for v_idx in face:
                        glVertex3f(*vertices[v_idx])
                    glEnd()
                glPopMatrix()
            _draw_list.append(draw_cmd)

        @staticmethod
        def Sphere(master=None, cx=0, cy=0, cz=0, radius=1, segments=24, rings=24, color=[(1,1,1)], tag=None):
            """
            3D球体
            调用格式 OpenGL.Graphics_3D.Sphere(cx=0,cy=0,cz=0,radius=1,segments=24,rings=24,color=["white"],tag="sph1")
            :param cx,cy,cz: 球心坐标
            :param radius: 半径
            :param segments: 水平分段
            :param rings: 垂直分段
            :param color: 颜色列表
            :param tag: 动画标签
            """
            out_color = OpenGL.resolve_color_list(color)
            attributes = {
                "rotate_state":False,
                "while_rot":True,
                "after":60,
                "angle":0.0,
                "rot_x":0,
                "rot_y":1,
                "rot_z":0
            }
            if tag is not None:
                Set_Graphic[tag] = {
                    "type":"Sphere",
                    "cx":cx,"cy":cy,"cz":cz,"radius":radius,"segments":segments,"rings":rings,
                    "color":color,"attributes":attributes
                }
            if master is not None:
                OpenGL.redirect(master)
            def draw_cmd(delta_time):
                glPushMatrix()
                glTranslatef(cx, cy, cz)
                if tag is not None and tag in Set_Graphic:
                    attr = Set_Graphic[tag]["attributes"]
                    if attr["rotate_state"]:
                        if attr["while_rot"]:
                            attr["angle"] += attr["after"] * delta_time
                        glRotatef(attr["angle"], attr["rot_x"], attr["rot_y"], attr["rot_z"])
                glColor3f(*out_color[0])
                for r in range(rings):
                    theta1 = math.pi * r / rings
                    theta2 = math.pi * (r+1) / rings
                    for s in range(segments):
                        phi1 = 2 * math.pi * s / segments
                        phi2 = 2 * math.pi * (s+1) / segments
                        def vert(th,ph):
                            x = radius*math.sin(th)*math.cos(ph)
                            y = radius*math.cos(th)
                            z = radius*math.sin(th)*math.sin(ph)
                            return (x,y,z)
                        v1=vert(theta1,phi1)
                        v2=vert(theta1,phi2)
                        v3=vert(theta2,phi2)
                        v4=vert(theta2,phi1)
                        glBegin(GL_QUADS)
                        glVertex3f(*v1)
                        glVertex3f(*v2)
                        glVertex3f(*v3)
                        glVertex3f(*v4)
                        glEnd()
                glPopMatrix()
            _draw_list.append(draw_cmd)

        @staticmethod
        def Cylinder(master=None, cx=0, cy=0, cz=0, radius=1, height=2, segments=24, color=[(0,1,1)], tag=None):
            """
            3D圆柱体
            调用格式 OpenGL.Graphics_3D.Cylinder(cx=0,cy=0,cz=0,radius=1,height=2,segments=24,color=["cyan"],tag="cyl1")
            """
            out_color = OpenGL.resolve_color_list(color)
            attributes = {
                "rotate_state":False,
                "while_rot":True,
                "after":60,
                "angle":0.0,
                "rot_x":0,
                "rot_y":1,
                "rot_z":0
            }
            if tag is not None:
                Set_Graphic[tag] = {
                    "type":"Cylinder",
                    "cx":cx,"cy":cy,"cz":cz,"radius":radius,"height":height,"segments":segments,
                    "color":color,"attributes":attributes
                }
            if master is not None:
                OpenGL.redirect(master)
            def draw_cmd(delta_time):
                glPushMatrix()
                glTranslatef(cx, cy, cz)
                if tag is not None and tag in Set_Graphic:
                    attr = Set_Graphic[tag]["attributes"]
                    if attr["rotate_state"]:
                        if attr["while_rot"]:
                            attr["angle"] += attr["after"] * delta_time
                        glRotatef(attr["angle"], attr["rot_x"], attr["rot_y"], attr["rot_z"])
                glColor3f(*out_color[0])
                h_half = height / 2.0
                # 侧面
                for s in range(segments):
                    a1 = 2*math.pi*s/segments
                    a2 = 2*math.pi*(s+1)/segments
                    x1,y1 = radius*math.cos(a1),radius*math.sin(a1)
                    x2,y2 = radius*math.cos(a2),radius*math.sin(a2)
                    glBegin(GL_QUADS)
                    glVertex3f(x1, -h_half, y1)
                    glVertex3f(x2, -h_half, y2)
                    glVertex3f(x2, h_half, y2)
                    glVertex3f(x1, h_half, y1)
                    glEnd()
                # 上底面
                glBegin(GL_TRIANGLE_FAN)
                glVertex3f(0, h_half, 0)
                for s in range(segments+1):
                    a = 2*math.pi*s/segments
                    x,y = radius*math.cos(a),radius*math.sin(a)
                    glVertex3f(x, h_half, y)
                glEnd()
                # 下底面
                glBegin(GL_TRIANGLE_FAN)
                glVertex3f(0, -h_half, 0)
                for s in reversed(range(segments+1)):
                    a = 2*math.pi*s/segments
                    x,y = radius*math.cos(a),radius*math.sin(a)
                    glVertex3f(x, -h_half, y)
                glEnd()
                glPopMatrix()
            _draw_list.append(draw_cmd)

        @staticmethod
        def Cone(master=None, cx=0, cy=0, cz=0, radius=1, height=2, segments=24, color=[(1,0,1)], tag=None):
            """
            3D圆锥
            调用格式 OpenGL.Graphics_3D.Cone(cx=0,cy=0,cz=0,radius=1,height=2,segments=24,color=["magenta"],tag="cone1")
            """
            out_color = OpenGL.resolve_color_list(color)
            attributes = {
                "rotate_state":False,
                "while_rot":True,
                "after":60,
                "angle":0.0,
                "rot_x":0,
                "rot_y":1,
                "rot_z":0
            }
            if tag is not None:
                Set_Graphic[tag] = {
                    "type":"Cone",
                    "cx":cx,"cy":cy,"cz":cz,"radius":radius,"height":height,"segments":segments,
                    "color":color,"attributes":attributes
                }
            if master is not None:
                OpenGL.redirect(master)
            def draw_cmd(delta_time):
                glPushMatrix()
                glTranslatef(cx, cy, cz)
                if tag is not None and tag in Set_Graphic:
                    attr = Set_Graphic[tag]["attributes"]
                    if attr["rotate_state"]:
                        if attr["while_rot"]:
                            attr["angle"] += attr["after"] * delta_time
                        glRotatef(attr["angle"], attr["rot_x"], attr["rot_y"], attr["rot_z"])
                glColor3f(*out_color[0])
                h_half = height/2.0
                tip_y = h_half
                base_y = -h_half
                # 锥侧面
                for s in range(segments):
                    a1 = 2*math.pi*s/segments
                    a2 = 2*math.pi*(s+1)/segments
                    x1,z1 = radius*math.cos(a1),radius*math.sin(a1)
                    x2,z2 = radius*math.cos(a2),radius*math.sin(a2)
                    glBegin(GL_TRIANGLES)
                    glVertex3f(0, tip_y, 0)
                    glVertex3f(x1, base_y, z1)
                    glVertex3f(x2, base_y, z2)
                    glEnd()
                # 圆锥底面
                glBegin(GL_TRIANGLE_FAN)
                glVertex3f(0, base_y, 0)
                for s in reversed(range(segments+1)):
                    a = 2*math.pi*s/segments
                    x,z = radius*math.cos(a),radius*math.sin(a)
                    glVertex3f(x, base_y, z)
                glEnd()
                glPopMatrix()
            _draw_list.append(draw_cmd)

        @staticmethod
        def Tetrahedron(master=None, scale=1, color=[(1,0,0),(0,1,0),(0,0,1),(1,1,1)], tag=None):
            """
            3D正四面体
            调用格式 OpenGL.Graphics_3D.Tetrahedron(scale=1,color=["red","green","blue","white"],tag="tet1")
            """
            out_color = OpenGL.resolve_color_list(color)
            verts = [
                (1, 1, 1),
                (-1,-1,1),
                (-1,1,-1),
                (1,-1,-1)
            ]
            faces = [
                [0,1,2],
                [0,2,3],
                [0,3,1],
                [1,3,2]
            ]
            attributes = {
                "rotate_state":False,
                "while_rot":True,
                "after":60,
                "angle":0.0,
                "rot_x":0,
                "rot_y":1,
                "rot_z":0
            }
            if tag is not None:
                Set_Graphic[tag] = {
                    "type":"Tetrahedron",
                    "scale":scale,"color":color,"attributes":attributes
                }
            if master is not None:
                OpenGL.redirect(master)
            def draw_cmd(delta_time):
                glPushMatrix()
                glScalef(scale,scale,scale)
                if tag is not None and tag in Set_Graphic:
                    attr = Set_Graphic[tag]["attributes"]
                    if attr["rotate_state"]:
                        if attr["while_rot"]:
                            attr["angle"] += attr["after"] * delta_time
                        glRotatef(attr["angle"], attr["rot_x"], attr["rot_y"], attr["rot_z"])
                for fi,face in enumerate(faces):
                    glBegin(GL_TRIANGLES)
                    c = out_color[fi] if fi<len(out_color) else (1,1,1)
                    glColor3f(*c)
                    for vi in face:
                        glVertex3f(*verts[vi])
                    glEnd()
                glPopMatrix()
            _draw_list.append(draw_cmd)