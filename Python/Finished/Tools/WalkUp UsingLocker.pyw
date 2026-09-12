import os
import tkinter as tk
from tkinter import filedialog, messagebox
import time
import threading

class UltraSimpleProtector:
    def __init__(self):
        self.files = []
        self.lock_start_time = 0
        self.lock_window = None
        self.lock()
    
    def unlock(self):
        ask = messagebox.askyesno('unlock', 'Do you want to unlock ?')
        if ask:
            for f in self.files:
                try:
                    f.close()
                except:
                    pass
            self.files.clear()
            
            if self.lock_window:
                self.lock_window.after(500, self.lock_window.destroy)
    
    def update_time(self):
        if self.lock_window and self.lock_start_time:
            elapsed = int(time.time() - self.lock_start_time)
            minutes = elapsed // 60000
            seconds = elapsed % 60000
            self.lock_window.title(f'WalkUp UsingLocker : Locked : {seconds:02d} s')
            self.lock_window.after(1000, self.update_time)
    
    def lock(self):
        choice = messagebox.askyesno("Select mode", "Lock a folder ?")
        
        if choice:
            path = filedialog.askdirectory(title="Select the directory to be locked")
            if path:
                try:
                    file_count = 0
                    for root, dirs, files in os.walk(path):
                        for file in files:
                            try:
                                file_path = os.path.join(root, file)
                                self.files.append(open(file_path, 'r+b'))
                                file_count += 1
                            except:
                                pass
                    
                    if file_count > 0:
                        pass
                    else:
                        messagebox.showwarning("Attention", f"The directory is locked, but no lockable files were found !")
                
                except Exception as e:
                    messagebox.showerror("Error", f"Lock failed : {e}")
                    return
        
        else:
            path = filedialog.askopenfilename(title="Select the file you want to lock")
            if path:
                try:
                    self.files.append(open(path, 'r+b'))
                except Exception as e:
                    messagebox.showerror("Error", f"Lock failed : {e}")
                    return
        
        if not self.files:
            return

        def u(event):
            if event.keysym in ['u', 'U']:
                self.unlock()

        time.sleep(1.5)
        
        self.lock_start_time = time.time()
        
        self.lock_window = tk.Tk()
        self.lock_window.title("WalkUp UsingLocker : Locked : 00 s")
        
        width, height = 400, 45
        screen_width = self.lock_window.winfo_screenwidth()
        screen_height = self.lock_window.winfo_screenheight()
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        self.lock_window.geometry(f'{width}x{height}+{x}+{y}')
        self.lock_window.resizable(False, False)
        
        self.lock_window.title('WalkUp UsingLocker')
        
        unlock_btn = tk.Button(
            self.lock_window, 
            text='unlock', 
            font=('Consolas', 18), 
            command=self.unlock,
            width=30, 
            height=1, 
            bg='red', 
            fg='white'
        )
        unlock_btn.place(x=0, y=0)
        
        self.update_time()
        self.lock_window.bind('<u>', u)
        self.lock_window.protocol("WM_DELETE_WINDOW", self.on_window_close)
        self.lock_window.mainloop()
    
    def on_window_close(self):
        if messagebox.askyesno("Confirm", "Do you want to unlock and exit ?"):
            self.unlock()
        else:
            self.lock_window.iconify()

if __name__ == "__main__":
    UltraSimpleProtector()