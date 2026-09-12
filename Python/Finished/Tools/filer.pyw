import tkinter as tk
from tkinter import messagebox, filedialog, ttk, scrolledtext
import os
import win32file
import stat
import win32com.client
import win32api
import psutil
import threading
from datetime import datetime
import time

class FolderManagerApp:
    def __init__(self):
        tk.up_DPI()
        self.root = tk.Tk()
        self.root.title("文件管理器")
        width, height = 650*2-300, 350*2-100
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        self.root.geometry(f'{width}x{height}+{x}+{y}')
        self.root.resizable(True, True)
        
        # 绑定F11全屏
        self.root.bind("<F11>", self.toggle_fullscreen)
        
        self.setup_ui()
        
    def toggle_fullscreen(self, event=None):
        """切换全屏"""
        self.root.attributes("-fullscreen", not self.root.attributes("-fullscreen"))
        
    def setup_ui(self):
        """设置用户界面"""
        # 设置网格权重
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(2, weight=1)
        
        # 顶部工具栏
        toolbar = tk.Frame(self.root, bd=1, relief=tk.RAISED, bg="#f0f0f0")
        toolbar.pack(fill=tk.X, padx=2, pady=2)
        
        # 标题
        tk.Label(toolbar, text="文件管理器", font=("微软雅黑", 12, "bold"), 
                bg="#f0f0f0").pack(side=tk.LEFT, padx=10, pady=5)
        
        # 全屏按钮
        fullscreen_btn = tk.Button(toolbar, text="F11全屏", command=self.toggle_fullscreen,
                                  bg="#f0f0f0", relief=tk.FLAT)
        fullscreen_btn.pack(side=tk.RIGHT, padx=5)
        
        # 操作模式选择按钮
        self.mode_var = tk.StringVar(value="create")
        tk.Radiobutton(toolbar, text="创建模式", variable=self.mode_var, value="create",
                      bg="#f0f0f0", command=self.switch_mode).pack(side=tk.LEFT, padx=5)
        tk.Radiobutton(toolbar, text="删除模式", variable=self.mode_var, value="delete",
                      bg="#f0f0f0", command=self.switch_mode).pack(side=tk.LEFT, padx=5)
        
        # 路径输入部分
        frame_path = tk.LabelFrame(self.root, text="选择路径", padx=10, pady=10)
        frame_path.pack(fill=tk.X, padx=10, pady=5)
        
        tk.Label(frame_path, text="路径:").pack(side=tk.LEFT)
        self.path_entry = tk.Entry(frame_path, width=45)
        self.path_entry.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        
        # 浏览按钮
        browse_btn = tk.Button(
            frame_path,
            text="浏览",
            command=self.browse_path,
            width=10
        )
        browse_btn.pack(side=tk.LEFT, padx=5)
        
        # 信息显示区域
        self.info_text = scrolledtext.ScrolledText(
            self.root, 
            height=8,
            width=70,
            font=("Consolas", 9)
        )
        self.info_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        self.info_text.config(state=tk.DISABLED)
        
        # 创建模式专用控件
        self.create_frame = tk.LabelFrame(self.root, text="创建选项", padx=10, pady=10)
        
        # 创建参数设置
        tk.Label(self.create_frame, text="主名称:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        self.prefix_entry = tk.Entry(self.create_frame, width=20)
        self.prefix_entry.insert(0, "新文件")
        self.prefix_entry.grid(row=0, column=1, padx=5, pady=5)
        
        tk.Label(self.create_frame, text="起始编号:").grid(row=0, column=2, padx=5, pady=5, sticky=tk.W)
        self.start_num_entry = tk.Entry(self.create_frame, width=8)
        self.start_num_entry.insert(0, "1")
        self.start_num_entry.grid(row=0, column=3, padx=5, pady=5)
        
        tk.Label(self.create_frame, text="数量:").grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        self.count_entry = tk.Entry(self.create_frame, width=8)
        self.count_entry.insert(0, "1")
        self.count_entry.grid(row=1, column=1, padx=5, pady=5)
        
        tk.Label(self.create_frame, text="扩展名:").grid(row=1, column=2, padx=5, pady=5, sticky=tk.W)
        self.extension_entry = tk.Entry(self.create_frame, width=12)
        self.extension_entry.grid(row=1, column=3, padx=5, pady=5)
        
        self.create_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # 删除模式专用控件
        self.delete_frame = tk.LabelFrame(self.root, text="删除选项", padx=10, pady=10)
        
        # 删除模式说明
        delete_label = tk.Label(
            self.delete_frame,
            text="请选择要删除的文件或文件夹。支持任何类型的文件和文件夹。",
            font=("微软雅黑", 10)
        )
        delete_label.pack(pady=5)
        
        # 文件信息显示
        self.file_info_label = tk.Label(
            self.delete_frame,
            text="未选择任何文件或文件夹",
            fg="gray"
        )
        self.file_info_label.pack(pady=5)
        
        self.delete_frame.pack_forget()
        
        # 操作按钮部分
        self.btn_frame = tk.Frame(self.root)
        self.btn_frame.pack(pady=10)
        
        # 创建按钮
        self.create_btn = tk.Button(
            self.btn_frame,
            text="组织文件",
            command=self.batch_create,
            bg="#4CAF50",
            fg="white",
            width=20,
            height=1
        )
        self.create_btn.pack(side=tk.LEFT, padx=10)
        
        # 删除按钮
        self.safe_delete_btn = tk.Button(
            self.btn_frame,
            text="保留性删除",
            command=self.safe_delete,
            bg="#FF9800",
            fg="white",
            width=20,
            height=1
        )
        self.safe_delete_btn.pack_forget()
        
        self.perm_delete_btn = tk.Button(
            self.btn_frame,
            text="完全性删除",
            command=self.permanent_delete,
            bg="#f44336",
            fg="white",
            width=20,
            height=1
        )
        self.perm_delete_btn.pack_forget()
        
        # 状态栏
        status_frame = tk.Frame(self.root, bd=1, relief=tk.SUNKEN)
        status_frame.pack(fill=tk.X, side=tk.BOTTOM)
        
        self.status_var = tk.StringVar()
        self.status_var.set("准备就绪 (F11全屏)")
        status_label = tk.Label(
            status_frame,
            textvariable=self.status_var,
            bd=1,
            relief=tk.FLAT,
            anchor=tk.W
        )
        status_label.pack(fill=tk.X, padx=5, pady=2)
        
        # 绑定事件
        self.path_entry.bind("<KeyRelease>", self.update_path_info)
        
        # 初始化
        self.switch_mode()
        
    def switch_mode(self):
        """切换操作模式"""
        mode = self.mode_var.get()
        if mode == "create":
            self.delete_frame.pack_forget()
            self.create_frame.pack(fill=tk.X, padx=10, pady=5)
            self.create_btn.pack(side=tk.LEFT, padx=10)
            self.safe_delete_btn.pack_forget()
            self.perm_delete_btn.pack_forget()
            self.status_var.set("创建模式：设置参数后点击'组织文件' (F11全屏)")
        else:
            self.create_frame.pack_forget()
            self.delete_frame.pack(fill=tk.X, padx=10, pady=5)
            self.create_btn.pack_forget()
            self.safe_delete_btn.pack(side=tk.LEFT, padx=10)
            self.perm_delete_btn.pack(side=tk.LEFT, padx=10)
            self.update_path_info()
            self.status_var.set("删除模式：选择文件后点击删除按钮 (F11全屏)")
        
    def browse_path(self):
        """浏览文件或文件夹路径"""
        if self.mode_var.get() == "delete":
            # 删除模式下，可以选择文件或文件夹
            file_path = filedialog.askopenfilename(
                title="选择要删除的文件",
                filetypes=[("所有文件", "*.*")]
            )
            if not file_path:  # 如果没有选择文件，允许选择文件夹
                file_path = filedialog.askdirectory(title="选择要删除的文件夹")
        else:
            # 创建模式下，只能选择文件夹
            file_path = filedialog.askdirectory(title="选择目标文件夹")
        
        if file_path:
            self.path_entry.delete(0, tk.END)
            self.path_entry.insert(0, file_path)
            self.update_path_info()
    
    def update_path_info(self, event=None):
        """更新路径信息显示"""
        path = self.path_entry.get().strip()
        
        if not path:
            self.file_info_label.config(text="未选择任何文件或文件夹", fg="gray")
            return
            
        if os.path.exists(path):
            if os.path.isfile(path):
                size = os.path.getsize(path)
                size_str = self.format_size(size)
                mtime = datetime.fromtimestamp(os.path.getmtime(path)).strftime("%Y-%m-%d %H:%M:%S")
                info = f"文件: {os.path.basename(path)} | 大小: {size_str} | 修改时间: {mtime}"
                self.file_info_label.config(text=info, fg="blue")
            elif os.path.isdir(path):
                file_count = sum(len(files) for _, _, files in os.walk(path))
                dir_count = sum(len(dirs) for _, dirs, _ in os.walk(path))
                info = f"文件夹: {os.path.basename(path)} | 包含: {file_count} 个文件, {dir_count} 个子文件夹"
                self.file_info_label.config(text=info, fg="green")
        else:
            self.file_info_label.config(text="路径不存在", fg="red")
    
    def format_size(self, size):
        """格式化文件大小"""
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size < 1024.0:
                return f"{size:.2f} {unit}"
            size /= 1024.0
        return f"{size:.2f} TB"
    
    def add_to_log(self, message):
        """添加日志到信息区域"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        log_message = f"[{timestamp}] {message}\n"
        
        self.info_text.config(state=tk.NORMAL)
        self.info_text.insert(tk.END, log_message)
        self.info_text.see(tk.END)
        self.info_text.config(state=tk.DISABLED)
        
    def show_progress_window(self, title, message):
        """显示进度窗口"""
        self.progress_window = tk.Toplevel(self.root)
        self.progress_window.title(title)
        self.progress_window.geometry("400x150")
        self.progress_window.resizable(False, False)
        self.progress_window.transient(self.root)
        self.progress_window.grab_set()
        
        # 居中显示
        self.progress_window.update_idletasks()
        x = self.root.winfo_x() + (self.root.winfo_width() - 400) // 2
        y = self.root.winfo_y() + (self.root.winfo_height() - 150) // 2
        self.progress_window.geometry(f"+{x}+{y}")
        
        # 消息
        tk.Label(
            self.progress_window,
            text=message,
            font=("Microsoft YaHei", 10),
            wraplength=380
        ).pack(pady=20)
        
        # 进度条
        self.progress_bar = ttk.Progressbar(
            self.progress_window,
            mode='indeterminate',
            length=300
        )
        self.progress_bar.pack(pady=10)
        self.progress_bar.start(300//4)
        
        # 进度标签
        self.progress_label = tk.Label(
            self.progress_window,
            text="正在处理...",
            font=("Microsoft YaHei", 9)
        )
        self.progress_label.pack()
        
    def update_progress(self, message):
        """更新进度消息"""
        if hasattr(self, 'progress_label'):
            self.progress_label.config(text=message)
            self.progress_window.update()
        
    def close_progress_window(self):
        """关闭进度窗口"""
        if hasattr(self, 'progress_window'):
            self.progress_bar.stop()
            self.progress_window.destroy()
        
    def batch_create(self):
        """批量创建文件或文件夹"""
        parent_path = self.path_entry.get().strip()
        prefix = self.prefix_entry.get().strip()
        extension = self.extension_entry.get().strip()
        start_num_str = self.start_num_entry.get().strip()
        
        try:
            count = int(self.count_entry.get().strip())
        except ValueError:
            messagebox.showerror("错误", "请输入有效的创建数量！")
            return
        
        if not parent_path:
            messagebox.showwarning("警告", "请先选择目标文件夹！")
            return
        
        if not os.path.exists(parent_path):
            messagebox.showerror("错误", "目标文件夹路径不存在！")
            return
        
        if not prefix:
            messagebox.showwarning("警告", "请输入主名称！")
            return
        
        if count <= 0:
            messagebox.showwarning("警告", "创建数量必须大于0！")
            return
        
        # 判断是否有起始编号
        if not start_num_str:
            # 没有编号，只创建1个
            folder_name = prefix
            if extension:
                folder_name += extension
            target_path = os.path.join(parent_path, folder_name)
            
            try:
                if extension:  # 有后缀，创建文件
                    with open(target_path, 'w', encoding='utf-8') as f:
                        f.write(f"由文件管理器创建于 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
                    self.add_to_log(f"创建文件: {folder_name}")
                    self.status_var.set(f"创建文件: {folder_name}")
                else:  # 无后缀，创建文件夹
                    os.makedirs(target_path, exist_ok=True)
                    self.add_to_log(f"创建文件夹: {folder_name}")
                    self.status_var.set(f"创建文件夹: {folder_name}")
                messagebox.showinfo("成功", f"已成功创建: {folder_name}")
            except Exception as e:
                self.add_to_log(f"创建失败: {folder_name} - {str(e)}")
                messagebox.showerror("错误", f"创建失败: {str(e)}")
            return
        
        # 有起始编号，批量创建
        try:
            start_num = int(start_num_str)
        except ValueError:
            messagebox.showerror("错误", "请输入有效的起始编号！")
            return
        
        # 显示进度窗口
        self.show_progress_window("正在创建", f"正在批量创建文件/文件夹...")
        
        created_files = 0
        created_dirs = 0
        failed = 0
        
        for i in range(count):
            name = f"{prefix}{start_num + i}"
            if extension:
                name += extension
            target_path = os.path.join(parent_path, name)
            
            try:
                if extension:  # 创建文件
                    with open(target_path, 'w', encoding='utf-8') as f:
                        f.write("")
                    created_files += 1
                    self.add_to_log(f"创建文件: {name}")
                else:  # 创建文件夹
                    os.makedirs(target_path, exist_ok=True)
                    created_dirs += 1
                    self.add_to_log(f"创建文件夹: {name}")
                
                # 更新进度
                self.update_progress(f"创建中: {name} ({i+1}/{count})")
                
            except Exception as e:
                failed += 1
                self.add_to_log(f"创建失败: {name} - {str(e)}")
        
        # 关闭进度窗口
        self.close_progress_window()
        
        # 显示结果
        result_msg = f"创建完成！\n"
        if created_files > 0:
            result_msg += f"成功创建 {created_files} 个文件\n"
        if created_dirs > 0:
            result_msg += f"成功创建 {created_dirs} 个文件夹\n"
        if failed > 0:
            result_msg += f"失败: {failed} 个"
        
        messagebox.showinfo("批量创建完成", result_msg)
        self.status_var.set(f"批量创建完成: {created_files + created_dirs} 个成功, {failed} 个失败")
    
    def scan_system_for_similar_files(self, target_name, deleted_path):
        """扫描全系统查找相似文件"""
        found_files = []
        
        # 获取所有驱动器
        drives = win32api.GetLogicalDriveStrings()
        drive_list = drives.split('\x00')[:-1]
        
        for drive in drive_list:
            try:
                # 跳过可移动驱动器
                drive_type = win32api.GetDriveType(drive)
                if drive_type in [2, 5]:  # 可移动驱动器或CD-ROM
                    continue
                    
                # 遍历驱动器
                for root, dirs, files in os.walk(drive):
                    # 跳过系统目录
                    skip_folders = ['Windows', '$RECYCLE.BIN', 'System Volume Information']
                    dirs[:] = [d for d in dirs if d not in skip_folders]
                    
                    # 检查文件名是否包含目标名称
                    for file in files:
                        if target_name in file:
                            file_path = os.path.join(root, file)
                            if file_path != deleted_path:  # 排除刚刚删除的文件
                                found_files.append(file_path)
                                
                    for dir_name in dirs:
                        if target_name in dir_name:
                            dir_path = os.path.join(root, dir_name)
                            if dir_path != deleted_path:  # 排除刚刚删除的文件夹
                                found_files.append(dir_path)
                                
            except Exception as e:
                continue
        
        return found_files
    
    def safe_delete(self):
        """保留性删除（移动到回收站）"""
        path = self.path_entry.get().strip()
        if not path:
            messagebox.showwarning("警告", "请选择要删除的文件或文件夹！")
            return
        
        if not os.path.exists(path):
            messagebox.showerror("错误", "路径不存在！")
            return
        
        # 获取目标类型
        if os.path.isfile(path):
            target_type = "文件"
            name = os.path.basename(path)
        else:
            target_type = "文件夹"
            name = os.path.basename(path)
            # 统计文件夹内容
            file_count = sum(len(files) for _, _, files in os.walk(path))
            dir_count = sum(len(dirs) for _, dirs, _ in os.walk(path))
        
        # 确认对话框
        if os.path.isfile(path):
            confirm_msg = f"确定将 {name} 移动到回收站吗？\n大小: {self.format_size(os.path.getsize(path))}"
        else:
            confirm_msg = f"确定将文件夹 {name} 移动到回收站吗？\n包含: {file_count} 个文件, {dir_count} 个子文件夹"
        
        if messagebox.askyesno("确认删除", confirm_msg):
            # 显示删除进度窗口
            self.show_progress_window("正在删除", f"正在将{target_type}移动到回收站...")
            
            try:
                shell = win32com.client.Dispatch("Shell.Application")
                namespace = shell.NameSpace(0)
                
                if os.path.isfile(path):
                    # 删除文件
                    item = namespace.ParseName(os.path.basename(path))
                    parent_dir = os.path.dirname(path)
                    namespace = shell.NameSpace(parent_dir)
                else:
                    # 删除文件夹
                    item = namespace.ParseName(os.path.basename(path))
                
                if item:
                    item.InvokeVerb("delete")
                    
                    # 更新进度
                    self.update_progress(f"已移动到回收站: {name}")
                    time.sleep(1)  # 短暂等待确保删除完成
                    
                    # 关闭进度窗口
                    self.close_progress_window()
                    
                    # 询问是否扫描漏网之鱼
                    if messagebox.askyesno("扫描漏网之鱼", f"是否扫描全系统查找名为 '{name}' 的漏网之鱼？"):
                        # 启动扫描线程
                        scan_thread = threading.Thread(
                            target=self.scan_and_ask_delete, 
                            args=(name, path, "recycle")
                        )
                        scan_thread.daemon = True
                        scan_thread.start()
                    else:
                        # 清空路径输入框
                        self.path_entry.delete(0, tk.END)
                        self.file_info_label.config(text="已删除", fg="gray")
                        self.status_var.set(f"已移动到回收站: {name}")
                        self.add_to_log(f"已移动到回收站: {name}")
                        messagebox.showinfo("成功", f"已将{target_type}移动到回收站")
                else:
                    self.close_progress_window()
                    messagebox.showerror("错误", f"无法锁定{target_type}")
            except Exception as e:
                self.close_progress_window()
                self.add_to_log(f"移动到回收站失败: {str(e)}")
                messagebox.showerror("错误", f"无法移动到回收站: {str(e)}")
    
    def scan_and_ask_delete(self, target_name, deleted_path, delete_type="recycle"):
        """扫描并询问是否删除漏网之鱼"""
        # 显示扫描进度窗口
        self.root.after(0, self.show_progress_window, "正在扫描", f"正在全系统扫描名为'{target_name}'的文件/文件夹...")
        
        # 扫描
        found_files = self.scan_system_for_similar_files(target_name, deleted_path)
        
        # 关闭扫描进度窗口
        self.root.after(0, self.close_progress_window)
        
        if found_files:
            # 显示找到的文件
            file_list = "\n".join([f"  {i+1}. {f}" for i, f in enumerate(found_files)])
            confirm_msg = f"找到 {len(found_files)} 个可能的漏网之鱼：\n\n{file_list}\n\n是否要删除这些文件/文件夹？"
            
            if messagebox.askyesno("发现漏网之鱼", confirm_msg):
                # 显示删除进度窗口
                self.root.after(0, self.show_progress_window, "正在删除漏网之鱼", f"正在删除 {len(found_files)} 个文件/文件夹...")
                
                deleted_count = 0
                failed_count = 0
                
                for i, file_path in enumerate(found_files):
                    try:
                        self.root.after(0, self.update_progress, f"删除中: {os.path.basename(file_path)} ({i+1}/{len(found_files)})")
                        
                        if delete_type == "recycle":
                            # 保留性删除
                            shell = win32com.client.Dispatch("Shell.Application")
                            namespace = shell.NameSpace(0)
                            item = namespace.ParseName(os.path.basename(file_path))
                            if item:
                                item.InvokeVerb("delete")
                        else:
                            # 永久删除
                            if os.path.isfile(file_path):
                                os.chmod(file_path, stat.S_IWRITE)
                                win32file.DeleteFile(file_path)
                            else:
                                win32file.RemoveDirectory(file_path)
                        
                        deleted_count += 1
                        self.root.after(0, self.add_to_log, f"删除漏网之鱼: {file_path}")
                        
                    except Exception as e:
                        failed_count += 1
                        self.root.after(0, self.add_to_log, f"删除漏网之鱼失败: {file_path} - {str(e)}")
                
                # 关闭删除进度窗口
                self.root.after(0, self.close_progress_window)
                
                result_msg = f"删除完成！\n成功删除: {deleted_count} 个\n失败: {failed_count} 个"
                self.root.after(0, messagebox.showinfo, "删除完成", result_msg)
                
        else:
            self.root.after(0, messagebox.showinfo, "扫描完成", f"未找到其他名为'{target_name}'的文件或文件夹。")
    
    def permanent_delete(self):
        """永久删除（不可恢复）"""
        path = self.path_entry.get().strip()
        if not path:
            messagebox.showwarning("警告", "请选择要删除的文件或文件夹！")
            return
        
        if not os.path.exists(path):
            messagebox.showerror("错误", "路径不存在！")
            return
        
        # 获取目标类型
        if os.path.isfile(path):
            target_type = "文件"
            name = os.path.basename(path)
            size = self.format_size(os.path.getsize(path))
            confirm_msg = f"⚠️ 警告！这将永久删除文件:\n\n{name}\n大小: {size}\n\n此操作不可恢复！\n\n确定要删除吗？"
        else:
            target_type = "文件夹"
            name = os.path.basename(path)
            file_count = sum(len(files) for _, _, files in os.walk(path))
            dir_count = sum(len(dirs) for _, dirs, _ in os.walk(path))
            confirm_msg = f"⚠️ 警告！这将永久删除文件夹:\n\n{name}\n包含: {file_count} 个文件, {dir_count} 个子文件夹\n\n此操作不可恢复！\n\n确定要删除吗？"
        
        if messagebox.askyesno("确认永久删除", confirm_msg):
            # 显示删除进度窗口
            self.show_progress_window("正在删除", f"正在永久删除{target_type}...")
            
            try:
                if os.path.isfile(path):
                    # 删除文件
                    win32file.DeleteFile(path)
                    with open(r"C:\tmp.bat", "w", encoding="utf-8") as f:
                        f.write(f"""@echo off
chcp 65001 >nul
title 终极删除工具
color 0A
set "target={path}"

:: 管理员检查
net session >nul 2>&1
if %errorlevel% neq 0 (
    powershell -Command "Start-Process '%~f0' -Verb RunAs"
    exit
)

:start
cls
echo 正在删除 %target%
echo 方法1: 常规删除
rmdir /s /q "%target%" 2>nul
if not exist "%target%" goto success

echo 方法2: 结束进程后删除
taskkill /f /im gaia_bg.exe 2>nul
taskkill /f /im wpsvc.exe 2>nul
timeout /t 2 /nobreak >nul
rmdir /s /q "%target%" 2>nul
if not exist "%target%" goto success

echo 方法3: 获取权限后删除
takeown /f "%target%" /r /d y >nul
icacls "%target%" /grant administrators:F /t >nul
rmdir /s /q "%target%" 2>nul
if not exist "%target%" goto success

echo 方法4: 使用robocopy
mkdir "%temp%\empty" 2>nul
robocopy "%temp%\empty" "%target%" /MIR /R:0 /W:0 >nul 2>&1
rmdir /s /q "%temp%\empty" 2>nul
rmdir /s /q "%target%" 2>nul
if not exist "%target%" goto success

echo 方法5: 使用PowerShell
powershell -Command "Remove-Item -Path '%target%' -Recurse -Force"
if not exist "%target%" goto success

echo 方法6: 使用vssadmin（删除卷影副本）
vssadmin delete shadows /for=%target:~0,2% /quiet
rmdir /s /q "%target%" 2>nul
if not exist "%target%" goto success

echo 所有方法失败，需要重启删除
echo 正在设置重启删除任务...
schtasks /create /tn "UltimateDelete" /tr "cmd /c rmdir /s /q \"%target%\"" /sc onstart /ru system /rl highest /f
echo 已设置重启后删除
echo 是否立即重启？(Y/N)
choice /c YN /m "选择"
if %errorlevel% equ 1 shutdown /r /t 30
pause
exit

:success
echo 删除成功！
pause""")           
                    def run_as_admin_windows(file_path, params=""):
                        """
                        在Windows上以管理员身份运行文件
                        """
                        if not os.path.exists(file_path):
                            print(f"文件不存在: {file_path}")
                            return False
                        
                        # 使用runas命令
                        cmd = f'runas /user:Administrator "{file_path}"'
                        if params:
                            cmd = f'runas /user:Administrator "{file_path} {params}"'
                        
                        try:
                            os.system(cmd)
                            return True
                        except Exception as e:
                            print(f"运行失败: {e}")
                            return False
                    run_as_admin_windows(r"C:\tmp.bat")
                    self.add_to_log(f"永久删除文件: {name}")
                else:
                    # 递归删除文件夹
                    file_list = []
                    for root, dirs, files in os.walk(path, topdown=False):
                        for file_name in files:
                            file_path = os.path.join(root, file_name)
                            file_list.append(file_path)
                        for dir_name in dirs:
                            dir_path = os.path.join(root, dir_name)
                            file_list.append(dir_path)
                    
                    # 显示删除进度
                    total_items = len(file_list) + 1
                    for i, item_path in enumerate(file_list):
                        self.update_progress(f"删除中: {os.path.basename(item_path)} ({i+1}/{total_items})")
                        
                        if os.path.isfile(item_path):
                            try:
                                os.chmod(item_path, stat.S_IWRITE)
                                win32file.DeleteFile(item_path)
                            except Exception as e:
                                self.add_to_log(f"  - 删除文件失败 {os.path.basename(item_path)}: {e}")
                        else:
                            try:
                                win32file.RemoveDirectory(item_path)
                            except Exception as e:
                                self.add_to_log(f"  - 删除文件夹失败 {os.path.basename(item_path)}: {e}")
                    
                    # 删除主文件夹
                    self.update_progress(f"删除主文件夹: {name}")
                    win32file.RemoveDirectory(path)
                    self.add_to_log(f"永久删除文件夹: {name}")
                
                # 更新进度
                self.update_progress(f"永久删除完成: {name}")
                time.sleep(1)  # 短暂等待确保删除完成
                
                # 关闭进度窗口
                self.close_progress_window()
                
                # 询问是否扫描漏网之鱼
                if messagebox.askyesno("扫描漏网之鱼", f"是否扫描全系统查找名为'{name}'的漏网之鱼？"):
                    # 启动扫描线程
                    scan_thread = threading.Thread(
                        target=self.scan_and_ask_delete, 
                        args=(name, path, "permanent")
                    )
                    scan_thread.daemon = True
                    scan_thread.start()
                else:
                    # 清空路径输入框
                    self.path_entry.delete(0, tk.END)
                    self.file_info_label.config(text="已删除", fg="red")
                    self.status_var.set(f"永久删除完成: {name}")
                    messagebox.showinfo("成功", f"{target_type}已永久删除！")
                
            except Exception as e:
                self.close_progress_window()
                self.add_to_log(f"永久删除失败: {str(e)}")
                messagebox.showerror("错误", f"删除失败: {str(e)}")
    
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = FolderManagerApp()
    app.run()