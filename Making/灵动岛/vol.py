from pycaw.pycaw import AudioUtilities

device = AudioUtilities.GetSpeakers()
volume = device.EndpointVolume

class vol:
    def get_vol():
        device = AudioUtilities.GetSpeakers()
        volume = device.EndpointVolume
        return volume.GetMasterVolumeLevelScalar() * 100

    def set_vol(val):
        val = max(0.0, min(100.0, val))
        val = val / 100.0
        device = AudioUtilities.GetSpeakers()
        volume = device.EndpointVolume
        volume.SetMasterVolumeLevelScalar(val, None)

    def mute(state:bool):
        device = AudioUtilities.GetSpeakers()
        volume = device.EndpointVolume
        volume.SetMute(1 if state else 0, None)