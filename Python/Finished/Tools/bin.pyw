import tkinter as tk
from tkinter import ttk, messagebox
import time as tm
import threading
import queue
import os

class CyberToolGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("biner")
        window_w, window_h = 750, 500
        screen_w = root.winfo_screenwidth()
        screen_h = root.winfo_screenheight()
        x = screen_w // 2 - window_w // 2
        y = screen_h // 2 - window_h // 2
        self.root.geometry(f'{window_w}x{window_h}+{x}+{y}')

        tk.Label(self.root, text="bin", font=("Consolas", 14, "bold")).pack(pady=(20, 10))
        self.text_area = tk.Text(self.root, font=("Consolas", 12), height=12, width=80, wrap=tk.WORD)
        self.text_area.pack(pady=(0, 20), padx=20)

        ttk.Button(self.root, text="0011 0001", style="Cyber.TButton", command=self.encrypt_text).place(x=20, y=425, width=320, height=60)
        ttk.Button(self.root, text="0011 0000", style="Cyber.TButton", command=self.decrypt_text).place(x=window_w-345, y=425, width=320, height=60)

    def encrypt_text(self):
        plain_text = self.text_area.get("1.0", tk.END)
        if not plain_text.strip():
            messagebox.showwarning("[INFO/WARN]", "Please enter the text to encrypt!")
            return

        pan = tk.Toplevel(self.root)
        pan.title('Compiling...')
        window_w, window_h = 650, 370
        screen_w = self.root.winfo_screenwidth()
        screen_h = self.root.winfo_screenheight()
        x = screen_w // 2 - window_w // 2
        y = screen_h // 2 - window_h // 2
        pan.geometry(f'{window_w}x{window_h}+{x}+{y}')
        pan.resizable(False, False)
        pan.attributes('-topmost', True)

        show = tk.Text(pan, font=("Microsoft YaHei", 10), height=10, width=50, wrap=tk.WORD)
        show.place(x=20, y=20)
        progress_bar = ttk.Progressbar(pan, length=610, mode="determinate", maximum=100)
        progress_bar.place(x=10, y=window_h-50)

        q = queue.Queue()
        log_list = []

        def check_log():
            try:
                if log_list:
                    for msg in log_list:
                        show.insert(tk.END, msg + '\n')
                    show.see(tk.END)
                    log_list.clear()
            except tk.TclError:
                return
            if pan.winfo_exists():
                pan.after(10, check_log)

        def check_queue():
            try:
                status, data = q.get_nowait()
                if status == 'success':
                    pan.after(50, pan.destroy)
                    self.root.after(400, lambda: create_result_window(data))
                elif status == 'error':
                    messagebox.showerror("[ERROR]", data)
                    pan.after(50, pan.destroy)
            except queue.Empty:
                self.root.after(100, check_queue)

        def create_result_window(display_lines):
            try:
                self.res_win = tk.Toplevel(self.root)
                self.res_win.title('Compiled')
                win_w, win_h = 650, 370
                scr_w = self.root.winfo_screenwidth()
                scr_h = self.root.winfo_screenheight()
                pos_x = scr_w // 2 - win_w // 2
                pos_y = scr_h // 2 - win_h // 2
                self.res_win.geometry(f'{win_w}x{win_h}+{pos_x}+{pos_y}')
                self.res_win.resizable(False, False)
                self.res_win.attributes('-topmost', True)

                res_show = tk.Text(self.res_win, font=("Consolas", 11), height=11, width=50, wrap=tk.WORD)
                res_show.place(x=20, y=20)

                def print_next_line(index):
                    if index < len(display_lines):
                        res_show.insert(tk.END, display_lines[index] + '\n')
                        res_show.see(tk.END)
                        self.res_win.after(1, lambda: print_next_line(index + 1))
                print_next_line(0)

                ttk.Button(self.res_win, text="0110 0111  0110 0101", style="Cyber.TButton", command=self.copy_text).place(x=20, y=295, width=320, height=60)
                def uo():
                    full_text = "\n".join(display_lines)
                    self.root.after(5, lambda: self.text_area.delete("1.0", tk.END))
                    self.root.after(5, lambda: self.text_area.insert(tk.END, full_text))
                ttk.Button(self.res_win, text="0111 0100  0110 1111", style="Cyber.TButton", command=uo).place(x=window_w-345, y=295, width=320, height=60)
            except tk.TclError:
                return

        def compile_task():
            try:
                log_list.append("[SYS] Initializing encryption engine...")
                tm.sleep(0.1)
                log_list.append("[SYS] Engine initialized successfully.")
                log_list.append("[PROC] Reading plaintext from buffer...")
                log_list.append(f"[PROC] Plaintext loaded. Length: {len(plain_text)} chars.")
                byte_data = plain_text.encode('utf-8')
                total_bytes = len(byte_data)
                
                final_bin_result = []
                display_lines = []
                current_line_bin = ""

                log_list.append("[PROC] Starting byte-by-byte encoding...")
                lines = plain_text.split('\n')
                i = 0
        
                for line_index, line_content in enumerate(lines):
                    log_list.append(f'[CROSS] Processing Line {line_index + 1}: {repr(line_content)}')
                    line_bytes = line_content.encode('utf-8')
                    for byte_val in line_bytes:
                        char = chr(byte_val)
                        bin_str_raw = format(byte_val, '08b')
                        part1 = bin_str_raw[:4]
                        part2 = bin_str_raw[4:]
                        bin_str_formatted = f"{part1} {part2}"
                        
                        final_bin_result.append(bin_str_raw)
                        current_line_bin += bin_str_formatted + '  '
                        
                        percent = int(((i + 1) / total_bytes) * 100)
                        self.root.after(0, lambda v=percent: progress_bar.config(value=v))
                        
                        i += 1 
                        if len(current_line_bin) > 60:
                            display_lines.append(current_line_bin.strip())
                            current_line_bin = ""
                    
                    log_list.append(f'[CROSS] Finished Line {line_index + 1}')

                
                if current_line_bin:
                    display_lines.append(current_line_bin.strip())

                log_list.append("[PROC] All bytes processed.")
                log_list.append("[SYS] Writing encrypted data to main buffer...")
                formatted_bin = " ".join(final_bin_result)
                with open("compile.dll", "w", encoding="utf-8") as f:
                    f.write(formatted_bin)
                q.put(('success', display_lines))

            except Exception as e:
                q.put(('error', str(e)))

        check_log()
        self.root.after(100, check_queue)
        threading.Thread(target=compile_task, daemon=True).start()

    def decrypt_text(self, c=0):
        bin_text = self.text_area.get("1.0", tk.END).strip()
        if not bin_text:
            messagebox.showwarning("[INFO/WARN]", "Deciphering Failed! We will try to Deciphering again!")
            if c < 3:
                self.decrypt_text(c + 1)
            return

        pan = tk.Toplevel(self.root)
        pan.title('Decoding...')
        window_w, window_h = 650, 370
        screen_w = self.root.winfo_screenwidth()
        screen_h = self.root.winfo_screenheight()
        x = screen_w // 2 - window_w // 2
        y = screen_h // 2 - window_h // 2
        pan.geometry(f'{window_w}x{window_h}+{x}+{y}')
        pan.resizable(False, False)
        pan.attributes('-topmost', True)

        show = tk.Text(pan, font=("Microsoft YaHei", 10), height=10, width=50, wrap=tk.WORD)
        show.place(x=20, y=20)
        progress_bar = ttk.Progressbar(pan, length=610, mode="determinate", maximum=100)
        progress_bar.place(x=10, y=window_h-50)

        q = queue.Queue()
        log_list = []

        def check_log():
            try:
                if log_list:
                    for msg in log_list:
                        show.insert(tk.END, msg + '\n')
                    show.see(tk.END)
                    log_list.clear()
            except tk.TclError:
                return
            if pan.winfo_exists():
                pan.after(1, check_log)

        def check_queue():
            try:
                status, data = q.get_nowait()
                if status == 'success':
                    decrypted_text = data
                    self.root.after(5, lambda: self.text_area.delete("1.0", tk.END))
                    self.root.after(5, lambda: self.text_area.insert(tk.END, decrypted_text))
                    self.root.after(5, lambda: progress_bar.config(value=100))
                    pan.after(50, pan.destroy)
                elif status == 'error':
                    self.root.after(5, lambda: progress_bar.config(value=100))
                    pan.after(50, pan.destroy)
                    self.root.after(100, lambda: messagebox.showerror("[INFO/ERROR]", data))
            except queue.Empty:
                self.root.after(100, check_queue)

        def decode_task():
            try:
                log_list.append("[SYS] Initializing decryption engine...")
                log_list.append("[SYS] Engine initialized successfully.")
                log_list.append("[PROC] Reading binary buffer...")
                clean_bin = ''.join(filter(lambda x: x in '01', bin_text))
                
                if len(clean_bin) % 8 != 0:
                    log_list.append("[WARN] Bitstream length is not a multiple of 8. Padding with zeros.")
                    clean_bin = clean_bin.ljust((len(clean_bin)//8 + 1)*8, '0')
                
                total_bytes = len(clean_bin) // 8
                byte_data = bytearray()

                log_list.append("[PROC] Starting binary stream reconstruction...")
                
                for i in range(total_bytes):
                    chunk = clean_bin[i*8 : (i+1)*8]
                    log_list.append(f"[BIN] Parsing Byte {i+1}/{total_bytes}: {chunk}")
                    try:
                        byte_val = int(chunk, 2)
                        byte_data.append(byte_val)
                    except ValueError:
                        log_list.append(f"[WARN] Invalid binary code skipped: {chunk}")
                        pass
                    
                    percent = int(((i + 1) / total_bytes) * 100)
                    self.root.after(0, lambda v=percent: progress_bar.config(value=v))

                log_list.append("[PROC] Stream reconstruction completed.")
                log_list.append("[PROC] Starting UTF-8 text assembly...")
                decrypted_text = byte_data.decode('utf-8', errors='replace')
                q.put(('success', decrypted_text))

            except Exception as e:
                q.put(('error', str(e)))

        check_log()
        self.root.after(100, check_queue)
        threading.Thread(target=decode_task, daemon=True).start()

    def copy_text(self):
        raw_content = self.text_area.get("1.0", tk.END)
        content_to_copy = raw_content.rstrip('\n')

        if content_to_copy.strip():
            self.root.clipboard_clear()
            self.root.clipboard_append(content_to_copy)
        else:
            messagebox.showwarning("[INFO/WARN]", "Result area is empty!")

if __name__ == "__main__":
    root = tk.Tk()
    app = CyberToolGUI(root)
    root.mainloop()
    if os.path.exists('compile.dll'):
        os.remove('compile.dll')