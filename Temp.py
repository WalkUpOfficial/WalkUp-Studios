from pycaw.pycaw import AudioUtilities
import System32

device = AudioUtilities.GetSpeakers()
volume = device.EndpointVolume

def get_vol():
    return volume.GetMasterVolumeLevelScalar() * 100

def set_vol(val):
    val = max(0.0, min(100.0, val))
    val = val / 100.0
    volume.SetMasterVolumeLevelScalar(val, None)

def mute(state:bool):
    volume.SetMute(1 if state else 0, None)

s = input()
if '音量' in s:
    num = ''
    for i in s:
        if i.isdigit():
            num += i
        else:
            if num:
                break
    if num:
        set_vol(int(num))
