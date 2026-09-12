import re

def find_text_in_multiline(multiline_string, search_text, 
                          case_sensitive=True, use_regex=False,
                          show_content=False):
    """
    在多行字符串中搜索文本并返回行号
    
    参数:
    multiline_string (str): 多行字符串
    search_text (str): 要搜索的文本
    case_sensitive (bool): 是否区分大小写，默认为True
    use_regex (bool): 是否使用正则表达式，默认为False
    show_content (bool): 是否返回行内容，默认为False
    
    返回:
    list: 包含匹配行号或(行号, 内容)元组的列表
    """
    lines = multiline_string.split('\n')
    results = []
    
    # 预处理搜索文本
    if not case_sensitive and not use_regex:
        search_text = search_text.lower()
    
    # 编译正则表达式
    if use_regex:
        flags = re.IGNORECASE if not case_sensitive else 0
        pattern = re.compile(search_text, flags)
    
    for i, line in enumerate(lines, start=1):
        # 跳过空行
        if not line.strip():
            continue
            
        # 检查是否匹配
        matched = False
        
        if use_regex:
            if pattern.search(line):
                matched = True
        else:
            if case_sensitive:
                if search_text in line:
                    matched = True
            else:
                if search_text in line.lower():
                    matched = True
        
        # 记录结果
        if matched:
            if show_content:
                results.append((i, line.strip()))
            else:
                results.append(i)
    
    return results

# 使用示例
if __name__ == "__main__":
    multiline_text = """
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os as c
import threading
import time
import platform
import subprocess

class FileSearchApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Ale - Ace - 文件搜索工具")
        self.root.deiconify()
        self.root.attributes('-fullscreen', True)
        self.root.configure(bg='white')
        
        # 设置窗口图标（可选）
        try:
            self.root.iconbitmap("search_icon.ico")
        except:
            pass
        
        # 创建界面
        self.create_widgets()
        
        # 搜索状态
        self.searching = False
        self.found_files = []
    
    def create_widgets(self):
        # 顶部标题
        self.title_label = tk.Label(self.root, text="文件搜索工具", 
                                  font=("Microsoft YaHei", 20, "bold"))
                           
        self.title_label.pack(pady=10)

        self.title = tk.Label(self.root, text="Ale - Ace有限公司", 
                                  font=("Microsoft YaHei", 10, "bold"))
                           
        self.title_label.pack(pady=20)
        
        # 搜索框
        search_frame = tk.Frame(self.root)
        search_frame.pack(pady=10, fill=tk.X, padx=20)
        
        tk.Label(search_frame, text="文件名:", font=("Microsoft YaHei", 12)).pack(side=tk.LEFT)
        
        self.filename_var = tk.StringVar()
        self.filename_entry = tk.Entry(search_frame, textvariable=self.filename_var,
                                      font=("Microsoft YaHei", 12), width=30)
        self.filename_entry.pack(side=tk.LEFT, padx=5)
        
        # 添加回车键搜索功能
        self.filename_entry.bind("<Return>", lambda event: self.start_search())
        
        tk.Label(search_frame, text="搜索路径:", font=("Microsoft YaHei", 12)).pack(side=tk.LEFT, padx=(10,0))
        
        self.path_var = tk.StringVar()
        self.path_var.set(c.path.join(c.path.expanduser("~"), "C:/"))  # 默认C盘
        self.path_entry = tk.Entry(search_frame, textvariable=self.path_var,
                                 font=("Microsoft YaHei", 12), width=30)
        self.path_entry.pack(side=tk.LEFT, padx=5)
        
        browse_btn = tk.Button(search_frame, text="浏览系统选择路径", 
                             command=self.browse_directory,
                             font=("Microsoft YaHei", 10))
        browse_btn.pack(side=tk.LEFT)
        
        # 状态标签
        self.status_label = tk.Label(self.root, text="准备就绪", 
                                   font=("Microsoft YaHei", 12), fg="gray")
        self.status_label.pack(pady=5)
        
        # 进度条框架（添加留白）
        progress_frame = tk.Frame(self.root)
        progress_frame.pack(pady=(10, 5), fill=tk.X, padx=10)  # 上下留白
        
        # 进度条标题
        progress_label = tk.Label(progress_frame, text="搜索进度:", 
                                 font=("Microsoft YaHei", 10), fg="gray")
        progress_label.pack(anchor=tk.W, pady=(0, 5))  # 下方留白
        
        # 进度条容器（添加内边距）
        progress_container = tk.Frame(progress_frame, padx=10, pady=10)  # 四周留白
        progress_container.pack(fill=tk.X)
        
        # 自定义绿色进度条
        self.progress_canvas = tk.Canvas(progress_container, width=1000, height=30, 
                                       bg="white", highlightthickness=0)
        self.progress_canvas.pack()
        
        # 百分比标签（放在进度条右侧）
        self.percent_label = tk.Label(progress_container, text="0%", 
                                    font=("Microsoft YaHei", 12))
        self.percent_label.place(in_=self.progress_canvas, relx=1.0, x=15, rely=0.5, anchor=tk.W)  # 右侧留白
        
        # 初始化进度条
        self.update_progress_bar(0)
        
        # 结果列表
        result_frame = tk.Frame(self.root)
        result_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # 添加结果标签
        result_label = tk.Label(result_frame, text="搜索结果:", font=("Microsoft YaHei", 12))
        result_label.pack(anchor=tk.W, pady=(0, 5))  # 下方留白
        
        # 结果列表框
        listbox_frame = tk.Frame(result_frame)
        listbox_frame.pack(fill=tk.BOTH, expand=True)
        
        self.result_list = tk.Listbox(listbox_frame, font=("Microsoft YaHei", 11))
        self.result_list.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        scrollbar = ttk.Scrollbar(listbox_frame, command=self.result_list.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.result_list.config(yscrollcommand=scrollbar.set)
        
        # 添加双击打开文件夹功能
        self.result_list.bind("<Double-Button-1>", self.open_selected_folder)
        
        # 按钮框架（添加留白）
        button_frame = tk.Frame(self.root, pady=10)  # 上下留白
        button_frame.pack()
        
        self.search_btn = tk.Button(button_frame, text="开始搜索", 
                                  font=("Microsoft YaHei", 14),
                                  bg="#4CAF50", fg="white",
                                  command=self.start_search,
                                  padx=20, pady=5)
        self.search_btn.pack(side=tk.LEFT, padx=10)
        
        self.stop_btn = tk.Button(button_frame, text="停止搜索", 
                                font=("Microsoft YaHei", 14),
                                bg="#F44336", fg="white",
                                command=self.stop_search,
                                padx=20, pady=5)
        self.stop_btn.pack(side=tk.LEFT, padx=10)
        self.stop_btn.config(state=tk.DISABLED)
        
        # 打开文件夹按钮
        self.open_btn = tk.Button(button_frame, text="打开文件所在文件夹", 
                                font=("Microsoft YaHei", 14),
                                bg="#2196F3", fg="white",
                                command=self.open_selected_folder,
                                padx=20, pady=5)
        self.open_btn.pack(side=tk.LEFT, padx=10)
        
        # 添加统计信息（添加留白）
        self.stats_frame = tk.Frame(self.root, pady=3)  # 上下留白
        self.stats_frame.pack()
        
        self.stats_label = tk.Label(self.stats_frame, text="找到 0 个文件", 
                                  font=("Microsoft YaHei", 10), fg="gray")
        self.stats_label.pack()
    
    def browse_directory(self):
        path = filedialog.askdirectory()
        if path:
            self.path_var.set(path)
    
    def update_progress_bar(self, percent):
        # 清除旧内容
        self.progress_canvas.delete("progress")
        
        # 固定使用绿色
        color = "#55FF55"  # 绿色
        
        # 绘制进度条（添加左右留白）
        canvas_width = self.progress_canvas.winfo_width()
        progress_width = (canvas_width - 20) * percent / 100  # 左右各留10像素
        self.progress_canvas.create_rectangle(
            10, 5, 10 + progress_width, 25,  # 上下各留5像素
            fill=color, outline="", tags="progress"
        )
        
        # 更新百分比
        self.percent_label.config(text=f"{percent}%")
        self.root.update()
    
    def start_search(self):
        if self.searching:
            return
            
        # 获取输入
        filename = self.filename_var.get().strip()
        search_path = self.path_var.get()
        
        if not filename:
            messagebox.showerror("错误", "请输入文件名")
            return
            
        if not c.path.exists(search_path):
            messagebox.showerror("错误", "搜索路径不存在")
            return
        
        # 重置界面
        self.result_list.delete(0, tk.END)
        self.found_files = []
        self.update_progress_bar(0)
        self.status_label.config(text=f"正在搜索: {filename}", fg="blue")
        self.stats_label.config(text="找到 0 个文件")
        
        # 禁用按钮
        self.search_btn.config(state=tk.DISABLED)
        self.stop_btn.config(state=tk.NORMAL)
        self.searching = True
        
        # 在新线程中执行搜索
        threading.Thread(target=self.search_files, 
                         args=(search_path, filename),
                         daemon=True).start()
    
    def stop_search(self):
        self.searching = False
        self.status_label.config(text="搜索已停止", fg="orange")
        self.search_btn.config(state=tk.NORMAL)
        self.stop_btn.config(state=tk.DISABLED)
    
    def search_files(self, root_dir, filename):
        total_dirs = 0
        processed_dirs = 0
        
        # 先统计目录数量（用于进度计算）
        for root, dirs, files in c.walk(root_dir):
            if not self.searching:
                return
            total_dirs += 1
        
        # 实际搜索
        for root, dirs, files in c.walk(root_dir):
            if not self.searching:
                return
                
            processed_dirs += 1
            
            # 更新进度
            progress = (processed_dirs / total_dirs) * 100
            self.root.after(0, self.update_progress_bar, progress)
            
            # 更新状态
            self.root.after(0, self.status_label.config, 
                          {"text": f"正在搜索: {root}"})
            
            # 检查文件
            if filename in files:
                file_path = c.path.join(root, filename)
                self.found_files.append(file_path)
                self.root.after(0, self.result_list.insert, tk.END, file_path)
                self.root.after(0, self.stats_label.config, 
                              {"text": f"找到 {len(self.found_files)} 个文件"})
            
            # 添加延迟，避免界面卡死
            time.sleep(0.01)
        
        # 搜索完成
        self.root.after(0, self.search_complete)
    
    def search_complete(self):
        self.searching = False
        self.status_label.config(text=f"搜索完成！找到 {len(self.found_files)} 个文件", fg="blue")
        self.search_btn.config(state=tk.NORMAL)
        self.stop_btn.config(state=tk.DISABLED)
        
        if not self.found_files:
            self.result_list.insert(tk.END, "未找到匹配文件")
    
    def open_selected_folder(self, event=None):
        selection = self.result_list.curselection()
        if not selection:
            messagebox.showinfo("提示", "请先选择一个文件")
            return
            
        file_path = self.result_list.get(selection[0])
        folder_path = c.path.dirname(file_path)
        
        if not c.path.exists(folder_path):
            messagebox.showerror("错误", "文件夹不存在")
            return
        
        try:
            # 根据操作系统打开文件夹
            system = platform.system()
            if system == "Windows":
                # Windows系统
                c.startfile(folder_path)
            elif system == "Darwin":
                # macOS系统
                subprocess.run(["open", folder_path])
            else:
                # Linux系统
                subprocess.run(["xdg-open", folder_path])
                
        except Exception as e:
            messagebox.showerror("错误", f"无法打开文件夹: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = FileSearchApp(root)
    root.mainloop()

"""

    look_for = "self.title_label"

    print(f"\n搜索目标 : [   {look_for}   ]")
    
    # 简单搜索
    print("\n简单搜索:",end="")
    line_numbers = find_text_in_multiline(multiline_text, look_for)
    print(f"匹配行号:{line_numbers}")
    
    # 显示内容
    print("\n显示内容:")
    results = find_text_in_multiline(multiline_text, look_for, show_content=True)
    for line_num, content in results:
        print(f"第[{line_num}]行:[    {content}    ]")
    
    # 区分大小写
    print("\n区分大小写:",end="")
    line_numbers = find_text_in_multiline(multiline_text, look_for, case_sensitive=True)
    print(f"匹配行号:{line_numbers}")
    
    # 正则表达式搜索
    print("\n正则表达式搜索:",end="")
    line_numbers = find_text_in_multiline(multiline_text, look_for, use_regex=True)
    print(f"匹配行号:{line_numbers}")

    
