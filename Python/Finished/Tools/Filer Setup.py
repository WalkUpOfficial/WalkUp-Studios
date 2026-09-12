import zipfile
import os
import tkinter as tk
from tkinter import messagebox, ttk
import shutil
import threading
import time
import tempfile

class Installer:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("安装")
        # tk.up_DPI()
        # 计算窗口居中位置
        width, height = 500, 300
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        self.root.geometry(f'{width}x{height}+{x}+{y}')
        
        # 设置图标（可选）
        try:
            self.root.iconbitmap('icon.ico')
        except:
            pass
        
        # 安装状态
        self.is_installing = False
        
        # 初始化UI
        self.setup_ui()
    
    def setup_ui(self):
        """设置用户界面"""
        # 标题
        title_label = tk.Label(
            self.root,
            text="文件资源管理器 1.2 安装程序",
            font=("微软雅黑", 16, "bold"),
            fg="blue"
        )
        title_label.pack(pady=20)
        
        # 版本信息
        version_label = tk.Label(
            self.root,
            text="version : 1.2",
            font=("微软雅黑", 10),
            fg="gray"
        )
        version_label.pack()
        
        # 状态显示
        self.status_label = tk.Label(
            self.root,
            text="准备安装",
            font=("微软雅黑", 10)
        )
        self.status_label.pack(pady=10)
        
        # 进度条
        self.progress_bar = ttk.Progressbar(
            self.root,
            length=400,
            mode='determinate'
        )
        self.progress_bar.pack(pady=10)
        self.progress_bar['value'] = 0
        
        # 安装按钮
        self.install_button = tk.Button(
            self.root,
            text="安装 - 文件资源管理器",
            bg="green",
            fg="white",
            font=("Microsoft YaHei", 12, "bold"),
            width=30,
            height=1,
            command=self.start_install
        )
        self.install_button.pack(pady=20)
    
    def update_status(self, message, progress=None):
        """更新状态标签和进度条"""
        self.status_label.config(text=message)
        if progress is not None:
            self.progress_bar['value'] = progress
        self.root.update()
    
    def extract_dependency_package(self):
        """解压依赖包"""
        try:
            # 获取当前脚本目录
            script_dir = os.path.dirname(os.path.abspath(__file__))
            dependency_path = os.path.join(script_dir, "文件资源控制器.DependencyPackage.zip")
            
            # 检查依赖包文件是否存在
            if not os.path.exists(dependency_path):
                return False, "错误: 找不到依赖包文件"
            
            # 创建临时目录
            temp_dir = r"C:\WalkUp\Temp"
            try:
                os.makedirs(temp_dir, exist_ok=True)
            except Exception as e:
                return False, f"无法创建临时目录: {str(e)}"
            
            # 解压依赖包
            try:
                with zipfile.ZipFile(dependency_path, 'r') as dependency_ref:
                    # 获取压缩包中的文件列表
                    file_list = dependency_ref.namelist()
                    total_files = len(file_list)
                    
                    for i, file in enumerate(file_list):
                        # 解压单个文件
                        dependency_ref.extract(file, temp_dir)
                        
                        # 添加缓冲时间
                        time.sleep(0.0002)
                        
                        # 更新进度
                        progress = 5 + (i + 1) / total_files * 20
                        self.root.after(0, lambda p=progress: self.update_status(f"正在解压依赖包... {i+1}/{total_files}", p))
                
                # 查找解压后的主目录
                extracted_path = None
                # 先尝试这个路径
                possible_paths = [
                    os.path.join(temp_dir, "文件资源控制器.DependencyPackage"),
                    os.path.join(temp_dir, "GameBar.DependencyPackage"),
                    temp_dir  # 如果直接解压在根目录
                ]
                
                for path in possible_paths:
                    if os.path.exists(path):
                        extracted_path = path
                        break
                
                if extracted_path is None:
                    # 如果没找到，尝试查找包含"DependencyPackage"的文件夹
                    for item in os.listdir(temp_dir):
                        item_path = os.path.join(temp_dir, item)
                        if os.path.isdir(item_path) and "DependencyPackage" in item:
                            extracted_path = item_path
                            break
                
                if extracted_path is None:
                    return False, "错误: 无法找到解压后的依赖包目录"
                
                # 调试信息：列出解压目录的内容
                print(f"解压目录: {extracted_path}")
                print("目录内容:")
                for root, dirs, files in os.walk(extracted_path):
                    level = root.replace(extracted_path, '').count(os.sep)
                    indent = ' ' * 4 * level
                    print(f'{indent}{os.path.basename(root)}/')
                    subindent = ' ' * 4 * (level + 1)
                    for file in files:
                        print(f'{subindent}{file}')
                
                # 检查必需的文件
                version_file = os.path.join(extracted_path, "version.txt")
                if not os.path.exists(version_file):
                    # 尝试在子目录中查找
                    found_version = False
                    for root, dirs, files in os.walk(extracted_path):
                        if "version.txt" in files:
                            version_file = os.path.join(root, "version.txt")
                            found_version = True
                            break
                    
                    if not found_version:
                        return False, f"错误: 依赖包中缺少 version.txt 文件\n\n提取目录: {extracted_path}\n目录内容: {os.listdir(extracted_path)}"
                
                resource_path = None
                # 查找"文件资源控制器资源"文件或文件夹
                for root, dirs, files in os.walk(extracted_path):
                    if "文件资源控制器资源" in dirs or "文件资源控制器资源" in files:
                        resource_path = os.path.join(root, "文件资源控制器资源")
                        break
                
                if resource_path is None or not os.path.exists(resource_path):
                    return False, f"错误: 依赖包中缺少'文件资源控制器资源'\n\n解压目录: {extracted_path}"
                
                # 检查版本
                with open(version_file, "r", encoding="utf-8") as f:
                    version = f.read().strip()
                
                if version != "1.2":
                    return False, f"版本不匹配: 需要1.2, 实际{version}"
                
                return True, extracted_path
                
            except zipfile.BadZipFile:
                return False, "错误: 依赖包文件已损坏"
            except Exception as e:
                return False, f"解压失败: {str(e)}"
                
        except Exception as e:
            return False, f"解压过程中发生错误: {str(e)}"
    
    def start_install(self):
        """开始安装"""
        if self.is_installing:
            return
        
        # 开始安装
        self.is_installing = True
        self.install_button.config(state=tk.DISABLED, bg="gray", text="安装中...")
        self.update_status("开始安装...", 0)
        
        # 在新线程中执行安装
        thread = threading.Thread(target=self.install_thread, daemon=True)
        thread.start()
    
    def install_thread(self):
        """安装线程"""
        try:
            # 步骤1: 解压依赖包
            self.root.after(0, lambda: self.update_status("正在提取依赖包里的文件...", 5))
            success, result = self.extract_dependency_package()
            
            if not success:
                self.root.after(0, lambda: messagebox.showerror("提取失败", result))
                self.install_failed()
                return
            
            extracted_path = result
            self.root.after(0, lambda: self.update_status("依赖包提取完成", 25))
            
            # 步骤2: 创建安装目录
            self.root.after(0, lambda: self.update_status("正在创建安装目录...", 30))
            install_dir = r"C:\WalkUp\文件资源管理器 1.2"
            
            try:
                os.makedirs(install_dir, exist_ok=True)
            except Exception as e:
                self.root.after(0, lambda: messagebox.showerror("错误", f"无法创建安装目录: {str(e)}"))
                self.install_failed()
                return
            
            # 步骤3: 复制资源文件
            self.root.after(0, lambda: self.update_status("正在提取资源文件...", 40))
            
            # 查找"文件资源控制器资源"的路径
            src_resource = None
            for root, dirs, files in os.walk(extracted_path):
                if "文件资源控制器资源" in dirs:
                    src_resource = os.path.join(root, "文件资源控制器资源")
                    break
                elif "文件资源控制器资源" in files:
                    src_resource = os.path.join(root, "文件资源控制器资源")
                    break
            
            if src_resource is None:
                self.root.after(0, lambda: messagebox.showerror("错误", "找不到资源文件"))
                self.install_failed()
                return
            
            # 目标路径
            dst_resource = r"C:\WalkUp\文件资源管理器 1.2"
            
            # 如果目标已存在，先删除
            if os.path.exists(dst_resource):
                try:
                    if os.path.isdir(dst_resource):
                        shutil.rmtree(dst_resource)
                    else:
                        os.remove(dst_resource)
                except Exception as e:
                    print(f"警告: 无法删除旧资源: {e}")
            
            # 复制资源
            try:
                if os.path.isdir(src_resource):
                    shutil.copytree(src_resource, dst_resource)
                else:
                    shutil.copy2(src_resource, dst_resource)
            except Exception as e:
                self.root.after(0, lambda: messagebox.showerror("错误", f"复制资源文件失败: {str(e)}"))
                self.install_failed()
                return
            
            self.root.after(0, lambda: self.update_status("资源文件复制完成", 60))
            
            # 步骤4: 创建快捷方式
            self.root.after(0, lambda: self.update_status("正在创建快捷方式...", 70))
            
            # 查找可执行文件
            exe_path = None
            for root_dir, dirs, files in os.walk(dst_resource):
                for file in files:
                    if file.endswith('.exe'):
                        exe_path = os.path.join(root_dir, file)
                        break
                if exe_path:
                    break
            
            if exe_path:
                # 使用VBScript创建快捷方式
                shortcut_path = os.path.join(os.path.expanduser('~'), 'Desktop', '文件资源管理器.lnk')
                
                vbs_script = f'''Set oWS = WScript.CreateObject("WScript.Shell")
sLinkFile = "{shortcut_path}"
Set oLink = oWS.CreateShortcut(sLinkFile)
oLink.TargetPath = "{exe_path}"
oLink.WorkingDirectory = "{os.path.dirname(exe_path)}"
oLink.Description = "文件资源管理器 1.2"
oLink.Save'''
                
                vbs_path = os.path.join(tempfile.gettempdir(), "create_shortcut.vbs")
                try:
                    with open(vbs_path, "w", encoding="gbk") as f:
                        f.write(vbs_script)
                    
                    os.system(f'cscript //nologo "{vbs_path}"')
                except Exception as e:
                    print(f"创建快捷方式失败: {e}")
                finally:
                    if os.path.exists(vbs_path):
                        try:
                            os.remove(vbs_path)
                        except:
                            pass
            
            self.root.after(0, lambda: self.update_status("快捷方式创建完成", 85))
            
            # 步骤5: 清理临时文件
            self.root.after(0, lambda: self.update_status("正在清理临时文件...", 90))
            temp_dir = r"C:\WalkUp\Temp"
            if os.path.exists(temp_dir):
                try:
                    shutil.rmtree(temp_dir)
                except Exception as e:
                    print(f"警告: 无法清理临时目录: {e}")
            
            os.mkdir(r"C:\WalkUp\Temp")
            
            # 安装完成
            self.root.after(0, self.install_complete)
            
        except Exception as e:
            self.root.after(0, lambda: messagebox.showerror("安装错误", f"安装过程中发生错误:\n{str(e)}"))
            self.install_failed()
    
    def install_failed(self):
        """安装失败"""
        self.is_installing = False
        self.update_status("安装失败", 0)
        self.install_button.config(state=tk.NORMAL, bg="green", text="重新安装")
    
    def install_complete(self):
        """安装完成"""
        self.is_installing = False
        self.update_status("安装完成！", 100)
        
        messagebox.showinfo("安装完成", "文件资源管理器 1.2 安装成功！")

        time.sleep(0.5)
        
        self.root.destroy()
    
    def run(self):
        """运行应用"""
        self.root.mainloop()

if __name__ == "__main__":
    app = Installer()
    app.run()