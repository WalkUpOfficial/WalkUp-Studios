import System32
import os
import WalkUpPyAudio

print('Starting Main...')

def say(path):
    System32.mpv.mp3.music(path=os.path.dirname(System32.file.Self())+r'\volumes\\'+path)

homophonics = {
    '关闭一遍':'关闭音量', 
    '关闭音标':'关闭音量', 
    '关闭饮料':'关闭音量', 
    '开启饮料':'开启音量', 
    '开启模样':'开启音量', 
    '卡一起音量':'开启音量', 
    }

def compile(target=None):
    for i, a in homophonics.items():
        target = target.replace(i, a)
    
    print('Admissions result :', target)
    
    if '静音' in target or '关闭声音' in target or '关闭音量' in target:
        say('mute.mp3')
        System32.time.sleep(2)
        System32.vol.mute(True)
    
    elif '开启声音' in target or '取消静音' in target or '开启音量' in target:
        System32.vol.mute(False)
        say('open.mp3')

def ALL():
    System32.mpv.mp3.music(path=os.path.dirname(System32.file.Self())+r'\volumes\Hi.mp3')
    System32.time.sleep(1)
    result = WalkUpPyAudio.ConvertText(frames=WalkUpPyAudio.Record(time=4))
    compile(result)

System32.vol.keywords(key='你好Com', ToDo=ALL)