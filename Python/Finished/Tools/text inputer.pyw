import tkinter as tk
from tkinter import messagebox  # 添加这行导入

class TextEditorApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("文本编辑器")
        self.root.geometry("600x400")
        
        # 创建主文本框
        self.create_text_widget()
        
        # 创建工具栏
        self.create_toolbar()
        
        # 运行主循环
        self.root.mainloop()
    
    def create_text_widget(self):
        """创建可编辑文本框"""
        # 创建滚动条
        scrollbar = tk.Scrollbar(self.root)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # 创建文本框
        self.text_box = tk.Text(
            self.root,
            wrap=tk.WORD,  # 按单词换行
            yscrollcommand=scrollbar.set,
            font=("Arial", 12),
            padx=10,
            pady=10
        )
        self.text_box.pack(expand=True, fill=tk.BOTH)
        
        # 绑定滚动条
        scrollbar.config(command=self.text_box.yview)
        
        # 添加示例文本
        self.text_box.insert(tk.END, "")
    
    def create_toolbar(self):
        """创建工具栏"""
        toolbar = tk.Frame(self.root)
        toolbar.pack(fill=tk.X)
        
        # 保存按钮
        save_btn = tk.Button(
            toolbar,
            text="保存",
            command=self.save_text,
            bg="#4CAF50",
            fg="white"
        )
        save_btn.pack(side=tk.LEFT, padx=5, pady=5)
        
        # 清除按钮
        clear_btn = tk.Button(
            toolbar,
            text="清除",
            command=self.clear_text,
            bg="#f44336",
            fg="white"
        )
        clear_btn.pack(side=tk.LEFT, padx=5, pady=5)
    
    def save_text(self):
        """保存文本内容"""
        content = self.text_box.get("1.0", tk.END)
        print("保存的内容：\n", content)
        messagebox.showinfo("保存", "内容已保存到控制台")  # 使用导入的messagebox
    
    def clear_text(self):
        """清除文本框内容"""
        self.text_box.delete("1.0", tk.END)

# 运行应用程序
if __name__ == "__main__":
    app = TextEditorApp()
