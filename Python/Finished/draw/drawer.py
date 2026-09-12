import matplotlib.pyplot as plt
from matplotlib.widgets import TextBox, Button
import numpy as np

class HandwritingCanvas:
    def __init__(self):
        self.fig, self.ax = plt.subplots(figsize=(12, 6))
        self.canvas = self.ax.figure.canvas
        self.canvas.mpl_connect('button_press_event', self.on_button_press)
        self.canvas.mpl_connect('motion_notify_event', self.on_motion)
        self.canvas.mpl_connect('button_release_event', self.on_button_release)
        self.canvas.mpl_connect('key_press_event', self.on_key_press)
        self.canvas.mpl_connect('key_release_event', self.on_key_release)
        
        self.lines = []  # 存储所有的线条对象及其数据
        self.current_xs = []
        self.current_ys = []
        self.background = None
        self.eraser_mode = False
        self.current_color = 'black'  # 初始颜色
        
        # 设置初始轴范围
        self.ax.set_xlim(0, 100)
        self.ax.set_ylim(0, 100)
        
        # 设置窗口位置（左上角坐标）
        self.fig.canvas.manager.window.wm_geometry("+100+100")  # x=100, y=100
        
        # 确保每个方格都是正方形
        self.ax.set_aspect('equal', adjustable='box')
        
        # 显示网格
        self.ax.grid(True)
        
        # 初始化背景
        self.update_background()
        
        # 添加文本输入框
        ax_text_box = self.fig.add_axes([0.3, 0.02, 0.43, 0.04])  # [left, bottom, width, height]
        self.text_box = TextBox(ax_text_box, '', textalignment="left")
        self.text_box.on_submit(self.submit)
        
        # 添加颜色选择框
        self.color_buttons = []
        colors = ['red', 'orange', 'yellow', 'green', 'blue', 'indigo', 'violet']
        for i, color in enumerate(colors):
            ax_color = self.fig.add_axes([0.05, 0.8 - i * 0.1, 0.05, 0.05])
            button = Button(ax_color, '', color=color)
            button.on_clicked(lambda event, c=color: self.change_color(c))
            self.color_buttons.append(button)

    def update_background(self):
        self.background = self.canvas.copy_from_bbox(self.ax.bbox)

    def on_button_press(self, event):
        if event.button == 1:  # 左键按下
            self.current_xs = [event.xdata]
            self.current_ys = [event.ydata]
        elif event.button == 3:  # 右键按下
            self.dragging = True
            self.last_x = event.x
            self.last_y = event.y

    def on_motion(self, event):
        if event.button == 1 and len(self.current_xs) > 0:  # 左键拖动
            self.current_xs.append(event.xdata)
            self.current_ys.append(event.ydata)
            if not self.eraser_mode:
                self.draw_line()
            else:
                self.erase_area(event.xdata, event.ydata)
        elif event.button == 3 and hasattr(self, 'dragging') and self.dragging:  # 右键拖动
            dx = event.x - self.last_x
            dy = event.y - self.last_y
            self.last_x = event.x
            self.last_y = event.y
            
            # 移动整个图形
            trans = self.ax.transData.inverted()
            dx_data, dy_data = trans.transform((dx, dy)) - trans.transform((0, 0))
            
            # 调整方向以确保移动方向正确
            current_xlim = self.ax.get_xlim()
            current_ylim = self.ax.get_ylim()
            self.ax.set_xlim(current_xlim[0] - dx_data, current_xlim[1] - dx_data)
            self.ax.set_ylim(current_ylim[0] - dy_data, current_ylim[1] - dy_data)
            self.canvas.draw_idle()

    def on_button_release(self, event):
        if event.button == 1:  # 左键释放
            if len(self.current_xs) > 0 and not self.eraser_mode:
                line, = self.ax.plot(self.current_xs, self.current_ys, color=self.current_color, lw=2)
                self.lines.append({'line': line, 'xs': self.current_xs, 'ys': self.current_ys, 'color': self.current_color})
                self.current_xs = []
                self.current_ys = []
                self.canvas.draw_idle()
        elif event.button == 3:  # 右键释放
            self.dragging = False

    def draw_line(self):
        self.ax.clear()
        self.setup_axis_limits_and_grid()
        for data in self.lines:
            self.ax.plot(data['xs'], data['ys'], color=data['color'], lw=2)
        if len(self.current_xs) > 0:
            self.ax.plot(self.current_xs, self.current_ys, color=self.current_color, lw=2)
        
        # 更新背景
        self.update_background()
        
        # 重新绘制图形
        self.canvas.restore_region(self.background)
        self.ax.draw_artist(self.ax.patch)
        for line in self.ax.lines:
            self.ax.draw_artist(line)
        self.canvas.blit(self.ax.bbox)

    def erase_area(self, x, y):
        eraser_radius = 1.0
        new_lines = []
        for data in self.lines:
            xs, ys = np.array(data['xs']), np.array(data['ys'])
            distances = np.sqrt((xs - x)**2 + (ys - y)**2)
            mask = distances > eraser_radius
            if not np.all(mask):
                # 分割线段
                start_idx = 0
                segments = []
                while start_idx < len(xs):
                    end_idx = start_idx
                    while end_idx < len(xs) and mask[end_idx]:
                        end_idx += 1
                    if end_idx > start_idx:
                        segments.append((xs[start_idx:end_idx], ys[start_idx:end_idx]))
                    start_idx = end_idx + 1
                
                if segments:
                    for segment in segments:
                        new_line, = self.ax.plot(segment[0], segment[1], color=data['color'], lw=2)
                        new_lines.append({'line': new_line, 'xs': segment[0].tolist(), 'ys': segment[1].tolist(), 'color': data['color']})
            else:
                new_lines.append(data)
        
        self.lines = new_lines
        self.ax.clear()
        self.setup_axis_limits_and_grid()
        for data in self.lines:
            self.ax.plot(data['xs'], data['ys'], color=data['color'], lw=2)
        
        # 更新背景
        self.update_background()
        
        # 重新绘制图形
        self.canvas.restore_region(self.background)
        self.ax.draw_artist(self.ax.patch)
        for line in self.ax.lines:
            self.ax.draw_artist(line)
        self.canvas.blit(self.ax.bbox)

    def setup_axis_limits_and_grid(self):
        # 设置轴范围与窗口边界一致
        self.ax.set_xlim(0, 100)
        self.ax.set_ylim(0, 100)
        
        # 确保每个方格都是正方形
        self.ax.set_aspect('equal', adjustable='box')
        
        # 显示网格
        self.ax.grid(True)

    def submit(self, text):
        if text.strip().lower() == 'clean':
            self.lines = []
            self.current_xs = []
            self.current_ys = []
            self.ax.clear()
            self.setup_axis_limits_and_grid()
            self.canvas.draw_idle()
            # 清空文本输入框
            self.text_box.set_val("")
        elif text.strip().lower() == 'exit':
            plt.close(self.fig)

    def on_key_press(self, event):
        if event.key.lower() == 'm':
            self.eraser_mode = True

    def on_key_release(self, event):
        if event.key.lower() == 'm' or 'M':
            self.eraser_mode = False

    def change_color(self, color):
        self.current_color = color

if __name__ == "__main__":
    canvas = HandwritingCanvas()
    plt.show()


