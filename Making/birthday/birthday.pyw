import time as tm
from System32 import file, mpv

def run(name): file.startup(file.Self_dir()+"\\"+name+"Runner.pyw")

# "E:\文件\WalkUp\mpv\mp3\花柚Flower、LumynX - HOVE (Slowed).mp3"
# "E:\文件\音频\生日快乐.mp3"
# "E:\文件\WalkUp\mpv\mp3\灰澈 - 星茶会.mp3"
mpv.sound_music(r"E:\文件\音频\生日快乐.mp3")
run("星茶会")
tm.sleep(3.5)
run("Plate")
tm.sleep(1)
run("Cake")
tm.sleep(3)
run('Love')
tm.sleep(12)
run('black_screen')
tm.sleep(2)
# mpv.sound_music(r"E:\文件\音频\生日快乐 -short.mp3")
tm.sleep(1)
run("MakeWish")
tm.sleep(16)
run("blesses")

tm.sleep(25)