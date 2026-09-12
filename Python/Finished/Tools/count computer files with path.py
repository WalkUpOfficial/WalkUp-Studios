import os
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import threading
import time
from pathlib import Path
import concurrent.futures
import queue
import pickle
from dataclasses import dataclass
from typing import List, Dict, Optional
import json
import atexit

@dataclass
class FileInfo:
    """文件信息数据类"""
    id: int
    path: str
    size: int
    mtime: float
    extension: str
    is_selected: bool = False

class FileScannerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("高速文件扫描器")
        self.root.geometry("900x700")
        
        # 扫描控制
        self.is_scanning = False
        self.is_ready = False
        self.shutting_down = False
        self.scan_thread = None
        self.display_thread = None
        self.file_counter = 0
        self.selected_files = {}  # 存储选择的文件
        
        # 数据存储
        self.all_files = []  # 存储所有文件信息
        self.file_cache = []  # 文件缓存
        self.file_queue = queue.Queue()  # 文件队列
        self.cache_limit = 1000000  # 最大缓存文件数
        self.display_limit = 1000000  # 最大显示文件数
        self.batch_size = 100000  # 批量处理大小
        
        # 扫描统计
        self.scan_start_time = 0
        self.scan_speed = 0
        self.total_scanned = 0
        
        # 注册退出清理函数
        atexit.register(self.cleanup_on_exit)
        
        # 绑定窗口关闭事件
        self.root.protocol("WM_DELETE_WINDOW", self.safe_close)
        
        # 创建界面
        self.create_widgets()
        
        # 启动后台扫描
        self.start_background_scan()
    
    def create_widgets(self):
        """创建界面"""
        # 主框架
        main_frame = tk.Frame(self.root, padx=10, pady=10)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # 标题
        title_label = tk.Label(main_frame, text="高速文件扫描器", 
                              font=("Microsoft YaHei", 16, "bold"))
        title_label.pack(pady=(0, 10))
        
        # 控制按钮框架
        control_frame = tk.Frame(main_frame)
        control_frame.pack(fill=tk.X, pady=(0, 10))
        
        # 显示按钮
        self.show_btn = tk.Button(control_frame, text="📁 显示文件", 
                                  command=self.show_files,
                                  bg="#2196F3", fg="white",
                                  font=("Microsoft YaHei", 10), width=12)
        self.show_btn.pack(side=tk.LEFT, padx=5)
        
        # 刷新按钮
        self.refresh_btn = tk.Button(control_frame, text="🔄 刷新", 
                                     command=self.refresh_scan,
                                     bg="#4CAF50", fg="white",
                                     font=("Microsoft YaHei", 10), width=10)
        self.refresh_btn.pack(side=tk.LEFT, padx=5)
        
        # 打开选中文件按钮
        self.open_selected_btn = tk.Button(control_frame, text="📂 打开选中", 
                                          command=self.open_selected_files,
                                          bg="#2196F3", fg="white",
                                          font=("Microsoft YaHei", 10), width=12)
        self.open_selected_btn.pack(side=tk.LEFT, padx=5)
        
        # 卸载选中按钮
        self.uninstall_selected_btn = tk.Button(control_frame, text="🗑️ 卸载选中", 
                                                command=self.uninstall_selected_files,
                                                bg="#FF9800", fg="white",
                                                font=("Microsoft YaHei", 10), width=12)
        self.uninstall_selected_btn.pack(side=tk.LEFT, padx=5)
        
        # 全选按钮
        self.select_all_btn = tk.Button(control_frame, text="✓ 全选", 
                                        command=self.select_all_files,
                                        bg="#9C27B0", fg="white",
                                        font=("Microsoft YaHei", 10), width=8)
        self.select_all_btn.pack(side=tk.LEFT, padx=5)
        
        # 反选按钮
        self.invert_selection_btn = tk.Button(control_frame, text="↔ 反选", 
                                             command=self.invert_selection,
                                             bg="#673AB7", fg="white",
                                             font=("Microsoft YaHei", 10), width=8)
        self.invert_selection_btn.pack(side=tk.LEFT, padx=5)
        
        # 安全关闭按钮
        self.close_btn = tk.Button(control_frame, text="🔒 安全关闭", 
                                   command=self.safe_close,
                                   bg="#f44336", fg="white",
                                   font=("Microsoft YaHei", 10), width=12)
        self.close_btn.pack(side=tk.LEFT, padx=5)
        
        # 统计信息框架
        info_frame = tk.Frame(main_frame)
        info_frame.pack(fill=tk.X, pady=(0, 10))
        
        # 扫描状态
        self.status_var = tk.StringVar(value="正在预扫描...")
        tk.Label(info_frame, text="状态:", font=("Microsoft YaHei", 9)).pack(side=tk.LEFT, padx=2)
        self.status_display = tk.Label(info_frame, textvariable=self.status_var,
                                      font=("Microsoft YaHei", 9), bg="#e8f5e8", 
                                      relief=tk.SUNKEN, width=20, anchor=tk.W)
        self.status_display.pack(side=tk.LEFT, padx=2)
        
        # 文件计数
        self.count_var = tk.StringVar(value="文件数: 0")
        count_label = tk.Label(info_frame, textvariable=self.count_var,
                               font=("Microsoft YaHei", 9, "bold"),
                               bg="#e3f2fd", relief=tk.RIDGE, width=15)
        count_label.pack(side=tk.LEFT, padx=5)
        
        # 速度显示
        self.speed_var = tk.StringVar(value="速度: 0 文件/秒")
        speed_label = tk.Label(info_frame, textvariable=self.speed_var,
                               font=("Microsoft YaHei", 9),
                               bg="#fff3e0", relief=tk.RIDGE, width=20)
        speed_label.pack(side=tk.LEFT, padx=5)
        
        # 已扫描文件
        self.scanned_var = tk.StringVar(value="已扫描: 0")
        scanned_label = tk.Label(info_frame, textvariable=self.scanned_var,
                                font=("Microsoft YaHei", 9),
                                bg="#e8f5e8", relief=tk.RIDGE, width=15)
        scanned_label.pack(side=tk.LEFT, padx=5)
        
        # 驱动器信息
        self.drive_var = tk.StringVar(value="")
        drive_label = tk.Label(info_frame, textvariable=self.drive_var,
                               font=("Microsoft YaHei", 9),
                               bg="#e0f2f1", relief=tk.RIDGE, width=20)
        drive_label.pack(side=tk.LEFT, padx=5)
        
        # 缓存状态
        self.cache_var = tk.StringVar(value="缓存: 0")
        cache_label = tk.Label(info_frame, textvariable=self.cache_var,
                               font=("Microsoft YaHei", 9),
                               bg="#f3e5f5", relief=tk.RIDGE, width=15)
        cache_label.pack(side=tk.LEFT, padx=5)
        
        # 已选择文件
        self.selected_var = tk.StringVar(value="已选: 0")
        selected_label = tk.Label(info_frame, textvariable=self.selected_var,
                                  font=("Microsoft YaHei", 9),
                                  bg="#f3e5f5", relief=tk.RIDGE, width=15)
        selected_label.pack(side=tk.LEFT, padx=5)
        
        # 扫描结果框架
        result_frame = tk.LabelFrame(main_frame, text="文件列表 (点击'显示文件'加载)", 
                                    padx=5, pady=5)
        result_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        # 创建Treeview
        self.create_treeview(result_frame)
        
        # 底部按钮框架
        bottom_frame = tk.Frame(main_frame)
        bottom_frame.pack(fill=tk.X)
        
        # 导出列表按钮
        export_btn = tk.Button(bottom_frame, text="📤 导出列表", 
                               command=self.export_file_list,
                               bg="#607D8B", fg="white",
                               font=("Microsoft YaHei", 10), width=12)
        export_btn.pack(side=tk.RIGHT, padx=5)
        
        # 清空列表按钮
        clear_btn = tk.Button(bottom_frame, text="🗑️ 清空列表", 
                              command=self.clear_file_list,
                              bg="#795548", fg="white",
                              font=("Microsoft YaHei", 10), width=12)
        clear_btn.pack(side=tk.RIGHT, padx=5)
        
        # 加载更多按钮
        self.load_more_btn = tk.Button(bottom_frame, text="📥 加载更多", 
                                      command=self.load_more_files,
                                      bg="#009688", fg="white",
                                      font=("Microsoft YaHei", 10), width=12)
        self.load_more_btn.pack(side=tk.RIGHT, padx=5)
        
        # 进度条
        self.progress = ttk.Progressbar(bottom_frame, mode='indeterminate', length=200)
        self.progress.pack(side=tk.LEFT, padx=5)
        
    def safe_close(self):
        """安全关闭程序"""
        if self.shutting_down:
            return
            
        # 如果有扫描正在进行，询问用户
        if self.is_scanning:
            response = messagebox.askyesnocancel("安全关闭", 
                "扫描正在进行中，您确定要关闭程序吗？\n\n"
                "选择'是'：停止扫描并关闭\n"
                "选择'否'：继续扫描\n"
                "选择'取消'：返回程序")
            
            if response is None:  # 取消
                return
            elif response:  # 是
                self.shutting_down = True
                self.status_var.set("正在停止扫描...")
                self.close_btn.config(state="disabled", text="正在关闭...")
                
                # 停止扫描
                self.is_scanning = False
                
                # 等待扫描线程结束
                if self.scan_thread and self.scan_thread.is_alive():
                    self.scan_thread.join(timeout=3.0)
                
                # 等待显示线程结束
                if self.display_thread and self.display_thread.is_alive():
                    self.display_thread.join(timeout=1.0)
                
                # 关闭窗口
                self.root.quit()
            else:  # 否
                return
        else:
            # 确认关闭
            response = messagebox.askyesno("确认关闭", "确定要关闭程序吗？")
            if response:
                self.shutting_down = True
                self.status_var.set("正在关闭...")
                self.close_btn.config(state="disabled", text="正在关闭...")
                
                # 直接关闭窗口
                self.root.quit()
    
    def cleanup_on_exit(self):
        """程序退出时的清理工作"""
        if self.shutting_down:
            print("程序正在安全关闭...")
        else:
            # 非正常关闭，尝试清理
            self.is_scanning = False
            
        # 清理临时文件等资源
        self.cleanup_resources()
    
    def cleanup_resources(self):
        """清理资源"""
        try:
            # 停止进度条
            if self.progress:
                self.progress.stop()
            
            # 清空缓存，释放内存
            self.all_files.clear()
            self.file_cache.clear()
            self.selected_files.clear()
            
            # 尝试清理临时文件
            temp_files = ['scan_cache.pkl', 'file_list.json']
            for temp_file in temp_files:
                if os.path.exists(temp_file):
                    try:
                        os.remove(temp_file)
                    except:
                        pass
                        
        except Exception as e:
            print(f"清理资源时出错: {e}")
    
    def create_treeview(self, parent):
        """创建Treeview控件"""
        # 创建框架包含Treeview和滚动条
        tree_frame = tk.Frame(parent)
        tree_frame.pack(fill=tk.BOTH, expand=True)
        
        # 垂直滚动条
        v_scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL)
        v_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # 水平滚动条
        h_scrollbar = ttk.Scrollbar(tree_frame, orient=tk.HORIZONTAL)
        h_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
        
        # 创建Treeview
        self.tree = ttk.Treeview(tree_frame, 
                                 yscrollcommand=v_scrollbar.set,
                                 xscrollcommand=h_scrollbar.set,
                                 selectmode="extended",  # 允许多选
                                 height=20)
        self.tree.pack(fill=tk.BOTH, expand=True)
        
        # 配置滚动条
        v_scrollbar.config(command=self.tree.yview)
        h_scrollbar.config(command=self.tree.xview)
        
        # 定义列
        self.tree["columns"] = ("序号", "路径", "大小", "修改时间", "类型")
        
        # 格式化列
        self.tree.column("#0", width=50, stretch=False)  # 选择列
        self.tree.column("序号", width=60, anchor=tk.CENTER)
        self.tree.column("路径", width=500)
        self.tree.column("大小", width=100, anchor=tk.E)
        self.tree.column("修改时间", width=150)
        self.tree.column("类型", width=100)
        
        # 创建表头
        self.tree.heading("#0", text="全选", command=lambda: self.toggle_all_checkboxes())
        self.tree.heading("序号", text="序号")
        self.tree.heading("路径", text="文件路径")
        self.tree.heading("大小", text="大小")
        self.tree.heading("修改时间", text="修改时间")
        self.tree.heading("类型", text="类型")
        
        # 创建自定义的复选框样式
        self.setup_checkbox_styles()
        
        # 绑定选择事件
        self.tree.bind('<ButtonRelease-1>', self.on_tree_click)
        
    def setup_checkbox_styles(self):
        """设置复选框样式"""
        # 创建选中和未选中的标签样式
        style = ttk.Style()
        
        # 为选中的行设置样式
        style.configure("selected.Treeview", 
                       background="#e3f2fd",  # 浅蓝色背景
                       foreground="black")
        
        # 为未选中的行设置样式
        style.configure("unselected.Treeview", 
                       background="white", 
                       foreground="black")
    
    def start_background_scan(self):
        """启动后台扫描"""
        self.is_scanning = True
        self.scan_start_time = time.time()
        self.progress.start(10)
        
        # 在后台线程中扫描
        self.scan_thread = threading.Thread(target=self.background_scan_thread)
        self.scan_thread.daemon = True
        self.scan_thread.start()
        
        # 启动缓存更新定时器
        self.root.after(1000, self.update_scan_stats)
    
    def background_scan_thread(self):
        """后台扫描线程"""
        try:
            all_drives = self.get_all_drives()
            self.root.after(0, lambda: self.status_var.set(f"正在扫描 {len(all_drives)} 个驱动器..."))
            
            # 创建线程池扫描多个驱动器
            with concurrent.futures.ThreadPoolExecutor(max_workers=min(len(all_drives), 4)) as executor:
                # 提交所有驱动器的扫描任务
                future_to_drive = {executor.submit(self.scan_drive_fast, drive): drive for drive in all_drives}
                
                for future in concurrent.futures.as_completed(future_to_drive):
                    if not self.is_scanning:  # 检查是否需要停止
                        break
                    
                    drive = future_to_drive[future]
                    try:
                        file_paths, count = future.result()
                        
                        # 将文件信息存储到缓存
                        for file_path in file_paths:
                            if not self.is_scanning:  # 再次检查是否需要停止
                                break
                                
                            if len(self.file_cache) < self.cache_limit:
                                try:
                                    stat = os.stat(file_path)
                                    file_info = FileInfo(
                                        id=len(self.all_files) + 1,
                                        path=file_path,
                                        size=stat.st_size,
                                        mtime=stat.st_mtime,
                                        extension=os.path.splitext(file_path)[1] or "文件"
                                    )
                                    self.all_files.append(file_info)
                                    self.file_cache.append(file_info)
                                except:
                                    continue
                        
                        # 更新统计
                        self.total_scanned += count
                        
                    except Exception as e:
                        print(f"扫描驱动器 {drive} 时出错: {e}")
            
            if self.is_scanning:
                self.is_ready = True
                elapsed = time.time() - self.scan_start_time
                speed = self.total_scanned / elapsed if elapsed > 0 else 0
                
                # 更新状态
                self.root.after(0, self.update_scan_complete, speed)
                
        except Exception as e:
            if not self.shutting_down:  # 如果不是在关闭过程中，才显示错误
                print(f"后台扫描出错: {e}")
                self.root.after(0, lambda: self.status_var.set(f"扫描出错: {e}"))
    
    def update_scan_stats(self):
        """更新扫描统计"""
        if self.is_scanning and not self.shutting_down:
            # 计算速度
            elapsed = time.time() - self.scan_start_time
            if elapsed > 0:
                self.scan_speed = self.total_scanned / elapsed
                
                # 更新界面
                self.root.after(0, lambda: self.speed_var.set(f"速度: {self.scan_speed:.0f} 文件/秒"))
                self.root.after(0, lambda: self.scanned_var.set(f"已扫描: {self.total_scanned}"))
                self.root.after(0, lambda: self.cache_var.set(f"缓存: {len(self.file_cache)}"))
                
                # 继续更新
                self.root.after(1000, self.update_scan_stats)
    
    def update_scan_complete(self, speed):
        """扫描完成更新"""
        if not self.shutting_down:
            self.is_scanning = False
            self.progress.stop()
            self.status_var.set("扫描完成")
            self.speed_var.set(f"速度: {speed:.0f} 文件/秒")
            self.scanned_var.set(f"已扫描: {self.total_scanned}")
            self.cache_var.set(f"缓存: {len(self.file_cache)}")
            self.show_btn.config(state="normal", bg="#4CAF50", text="📁 显示文件")
    
    def get_all_drives(self):
        """获取所有驱动器"""
        drives = []
        for drive in range(65, 91):
            drive_letter = chr(drive) + ':\\'
            if os.path.exists(drive_letter):
                drives.append(drive_letter)
        return drives
    
    def scan_drive_fast(self, drive):
        """快速扫描驱动器"""
        file_paths = []
        count = 0
        
        try:
            drive_path = Path(drive)
            
            # 使用rglob快速扫描
            for file_path in drive_path.rglob("*"):
                if not self.is_scanning or self.shutting_down:  # 检查是否需要停止
                    break
                
                # 检查是否是文件
                if file_path.is_file():
                    # 检查是否应该跳过
                    if self.should_skip_path(str(file_path)):
                        continue
                    
                    file_paths.append(str(file_path))
                    count += 1
                    
                    # 每扫描1000个文件更新一次状态
                    if count % 1000 == 0:
                        self.root.after(0, lambda d=drive, c=count: self.update_drive_info(d, c))
        
        except Exception as e:
            if not self.shutting_down:  # 如果不是在关闭过程中，才记录错误
                print(f"扫描驱动器 {drive} 时出错: {e}")
        
        return file_paths, count
    
    def should_skip_path(self, path):
        """检查是否应该跳过路径"""
        lower_path = path.lower()
        skip_keywords = ["\\Windows\\", "\\system volume information\\","\\$recycle.bin\\", "\\recovery\\", "\\perflogs\\","\\boot\\"]
        
        for keyword in skip_keywords:
            if keyword in lower_path:
                return True
        
        return False
    
    def update_drive_info(self, drive, count):
        """更新驱动器信息"""
        if not self.shutting_down:
            self.drive_var.set(f"正在扫描: {drive}")
            self.scanned_var.set(f"已扫描: {count}")
    
    def show_files(self):
        """显示文件"""
        if not self.file_cache or self.shutting_down:
            messagebox.showinfo("提示", "暂无文件可显示")
            return
        
        # 禁用按钮，防止重复点击
        self.show_btn.config(state="disabled", text="正在加载...")
        
        # 清空现有列表
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # 在后台线程中加载文件
        self.display_thread = threading.Thread(target=self.load_files_to_treeview)
        self.display_thread.daemon = True
        self.display_thread.start()
    
    def load_files_to_treeview(self):
        """加载文件到Treeview"""
        start_time = time.time()
        
        # 分批加载文件
        display_count = min(self.display_limit, len(self.file_cache))
        batch_size = 1000
        
        for i in range(0, display_count, batch_size):
            if self.shutting_down:  # 检查是否正在关闭
                break
                
            batch = self.file_cache[i:i+batch_size]
            self.root.after(0, self.add_batch_to_treeview, batch, i)
            time.sleep(0.01)  # 小延迟，避免界面卡死
        
        elapsed = time.time() - start_time
        speed = display_count / elapsed if elapsed > 0 else 0
        
        # 更新界面
        if not self.shutting_down:
            self.root.after(0, self.update_display_complete, display_count, speed)
    
    def add_batch_to_treeview(self, batch, start_index):
        """批量添加文件到Treeview"""
        if self.shutting_down:
            return
            
        for i, file_info in enumerate(batch):
            try:
                # 格式化信息
                size = self.format_size(file_info.size)
                mtime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(file_info.mtime))
                file_type = file_info.extension or "文件"
                
                # 检查文件是否在选中列表中
                is_selected = file_info.path in self.selected_files
                tag = "selected" if is_selected else "unselected"
                text = "✓" if is_selected else ""
                
                # 插入到Treeview
                item = self.tree.insert("", "end", 
                                       text=text,  # 在第一列显示✓或空
                                       values=(start_index + i + 1, file_info.path, 
                                               size, mtime, file_type),
                                       tags=(tag,))
                
            except Exception as e:
                continue
        
        # 更新计数
        if not self.shutting_down:
            self.count_var.set(f"文件数: {len(self.tree.get_children())}")
    
    def update_display_complete(self, count, speed):
        """显示完成更新"""
        if not self.shutting_down:
            self.show_btn.config(state="normal", text="📁 显示文件")
            self.status_var.set(f"已显示 {count} 个文件")
    
    def format_size(self, size_bytes):
        """格式化文件大小"""
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if size_bytes < 1024.0:
                return f"{size_bytes:.1f} {unit}"
            size_bytes /= 1024.0
        return f"{size_bytes:.1f} PB"
    
    def load_more_files(self):
        """加载更多文件"""
        if not self.file_cache or self.shutting_down:
            return
        
        # 获取当前已显示的文件数
        current_count = len(self.tree.get_children())
        
        # 计算要加载的下一批文件
        start_idx = current_count
        end_idx = min(start_idx + self.batch_size, len(self.file_cache))
        
        if start_idx >= end_idx:
            messagebox.showinfo("提示", "已加载所有文件")
            return
        
        # 加载下一批文件
        batch = self.file_cache[start_idx:end_idx]
        self.add_batch_to_treeview(batch, start_idx)
    
    def refresh_scan(self):
        """刷新扫描"""
        if self.is_scanning or self.shutting_down:
            messagebox.showinfo("提示", "扫描正在进行中，请稍候")
            return
        
        # 清空现有数据
        self.all_files.clear()
        self.file_cache.clear()
        self.selected_files.clear()
        self.total_scanned = 0
        
        # 清空Treeview
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # 重启扫描
        self.start_background_scan()
    
    def toggle_all_checkboxes(self):
        """切换所有复选框状态"""
        if not self.tree.get_children() or self.shutting_down:
            return
        
        # 获取当前状态
        first_item = self.tree.get_children()[0]
        current_text = self.tree.item(first_item, "text")
        
        if current_text == "✓":
            new_text = ""
            new_tag = "unselected"
        else:
            new_text = "✓"
            new_tag = "selected"
        
        # 更新所有项目
        for item in self.tree.get_children():
            file_path = self.tree.item(item)["values"][1]
            
            # 更新显示
            self.tree.item(item, text=new_text, tags=(new_tag,))
            
            # 更新选中状态
            if new_text == "✓":
                self.selected_files[file_path] = self.tree.item(item)["values"]
            else:
                if file_path in self.selected_files:
                    del self.selected_files[file_path]
        
        self.selected_var.set(f"已选: {len(self.selected_files)}")
    
    def on_tree_click(self, event):
        """处理Treeview点击事件"""
        if self.shutting_down:
            return
            
        region = self.tree.identify_region(event.x, event.y)
        
        if region == "cell":
            column = self.tree.identify_column(event.x)
            if column == "#0":  # 点击了复选框列
                item = self.tree.identify_row(event.y)
                if item:
                    self.toggle_checkbox(item)
                    
    def toggle_checkbox(self, item):
        """切换单个复选框状态"""
        if self.shutting_down:
            return
            
        current_text = self.tree.item(item, "text")
        file_path = self.tree.item(item)["values"][1]
        
        if current_text == "✓":
            # 取消选中
            self.tree.item(item, text="", tags=("unselected",))
            if file_path in self.selected_files:
                del self.selected_files[file_path]
        else:
            # 选中
            self.tree.item(item, text="✓", tags=("selected",))
            self.selected_files[file_path] = self.tree.item(item)["values"]
        
        self.selected_var.set(f"已选: {len(self.selected_files)}")
    
    def open_selected_files(self):
        """打开选中文件所在的文件夹"""
        if not self.selected_files or self.shutting_down:
            messagebox.showwarning("警告", "请先选择文件")
            return
        
        opened = 0
        for file_path in self.selected_files.keys():
            try:
                # 打开文件所在的文件夹并选中文件
                if os.path.exists(file_path):
                    # 使用explorer打开文件夹并选中文件
                    if os.path.isfile(file_path):
                        # 对于文件，打开其所在的文件夹并选中文件
                        folder_path = os.path.dirname(file_path)
                        # Windows命令：explorer /select,"文件路径"
                        os.system(f'explorer /select,"{file_path}"')
                    else:
                        # 对于文件夹，直接打开文件夹
                        os.startfile(file_path)
                    opened += 1
            except Exception as e:
                print(f"无法打开文件夹: {file_path}: {e}")
        
        messagebox.showinfo("完成", f"已打开 {opened} 个文件夹")
    
    def uninstall_selected_files(self):
        """卸载选中的文件"""
        if not self.selected_files or self.shutting_down:
            messagebox.showwarning("警告", "请先选择文件")
            return
        
        response = messagebox.askyesno("确认", f"确定要删除 {len(self.selected_files)} 个文件吗？此操作不可撤销！")
        if not response:
            return
        
        deleted = 0
        failed = []
        
        for file_path in list(self.selected_files.keys()):
            try:
                if os.path.isfile(file_path):
                    os.remove(file_path)
                elif os.path.isdir(file_path):
                    import shutil
                    shutil.rmtree(file_path)
                
                # 从Treeview中移除
                for item in self.tree.get_children():
                    if self.tree.item(item)["values"][1] == file_path:
                        self.tree.delete(item)
                        break
                
                # 从选中列表中移除
                if file_path in self.selected_files:
                    del self.selected_files[file_path]
                
                # 从缓存中移除
                for i, file_info in enumerate(self.file_cache):
                    if file_info.path == file_path:
                        self.file_cache.pop(i)
                        break
                
                deleted += 1
                
            except Exception as e:
                failed.append(f"{file_path}: {e}")
        
        self.selected_var.set(f"已选: {len(self.selected_files)}")
        self.cache_var.set(f"缓存: {len(self.file_cache)}")
        self.count_var.set(f"文件数: {len(self.tree.get_children())}")
        
        result_msg = f"已删除 {deleted} 个文件"
        if failed:
            result_msg += f"\n\n删除失败:\n" + "\n".join(failed[:5])
            if len(failed) > 5:
                result_msg += f"\n... 还有 {len(failed)-5} 个失败"
        
        messagebox.showinfo("结果", result_msg)
    
    def select_all_files(self):
        """全选所有文件"""
        if self.shutting_down:
            return
            
        for item in self.tree.get_children():
            self.tree.item(item, text="✓", tags=("selected",))
            file_path = self.tree.item(item)["values"][1]
            self.selected_files[file_path] = self.tree.item(item)["values"]
        
        self.selected_var.set(f"已选: {len(self.selected_files)}")
    
    def invert_selection(self):
        """反选"""
        if self.shutting_down:
            return
            
        for item in self.tree.get_children():
            current_text = self.tree.item(item, "text")
            file_path = self.tree.item(item)["values"][1]
            
            if current_text == "✓":
                # 取消选中
                self.tree.item(item, text="", tags=("unselected",))
                if file_path in self.selected_files:
                    del self.selected_files[file_path]
            else:
                # 选中
                self.tree.item(item, text="✓", tags=("selected",))
                self.selected_files[file_path] = self.tree.item(item)["values"]
        
        self.selected_var.set(f"已选: {len(self.selected_files)}")
    
    def export_file_list(self):
        """导出文件列表"""
        if not self.tree.get_children() or self.shutting_down:
            messagebox.showwarning("警告", "没有文件可导出")
            return
        
        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("文本文件", "*.txt"), ("所有文件", "*.*"), ("JSON 文件", "*.json")],
            title="保存文件列表"
        )
        
        if not file_path:
            return
        
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write("文件扫描列表\n")
                f.write("=" * 50 + "\n\n")
                f.write(f"扫描时间: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"文件总数: {len(self.tree.get_children())}\n")
                f.write(f"选中文件: {len(self.selected_files)}\n")
                f.write("=" * 50 + "\n\n")
                
                for item in self.tree.get_children():
                    values = self.tree.item(item)["values"]
                    is_selected = "✓" if self.tree.item(item, "text") == "✓" else ""
                    f.write(f"[{is_selected}] 序号: {values[0]}\n")
                    f.write(f"    路径: {values[1]}\n")
                    f.write(f"    大小: {values[2]}\n")
                    f.write(f"    修改时间: {values[3]}\n")
                    f.write(f"    类型: {values[4]}\n")
                    f.write("-" * 30 + "\n")
            
            messagebox.showinfo("成功", f"文件列表已导出到:\n{file_path}")
        except Exception as e:
            messagebox.showerror("错误", f"导出失败: {e}")
    
    def clear_file_list(self):
        """清空文件列表"""
        if not self.tree.get_children() or self.shutting_down:
            return
        
        response = messagebox.askyesno("确认", "确定要清空文件列表吗？")
        if response:
            for item in self.tree.get_children():
                self.tree.delete(item)
            
            self.selected_files = {}
            self.selected_var.set("已选: 0")
            self.count_var.set("文件数: 0")

def main():
    root = tk.Tk()
    app = FileScannerApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()