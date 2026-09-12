import tkinter as tk

root = tk.Tk()

DPI = round(root.winfo_fpixels('1i') / 96)
root.title('Window')
w = 800
h = 500
root.geometry(f'{w * DPI}x{h * DPI}+{root.winfo_screenwidth() // 2 - w * DPI // 2}+{root.winfo_screenheight() // 2 - h * DPI // 2}')

pass

root.mainloop()