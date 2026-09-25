
import System32
import pyaudio
import wave
import os
from vosk import Model, KaldiRecognizer, SetLogLevel
import json
import sys

# Init
SetLogLevel(-1)

class Audio:
    def Record(time=3, Tip=False, channels = 1, rate = 16000, chunk = 1024):
        FORMAT = pyaudio.paInt16
        p = pyaudio.PyAudio()
        try:
            stream = p.open(format=FORMAT,
                            channels=channels,
                            rate=rate,
                            input=True,
                            frames_per_buffer=chunk)
            frames = []
            if Tip:
                print("开始录音...说话！")
            loop_count = int(rate / chunk * time)
            for i in range(loop_count):
                data = stream.read(chunk, exception_on_overflow=False)
                frames.append(data)
            if Tip:
                print("录音结束")
            stream.stop_stream()
            stream.close()
            return frames
        finally:
            p.terminate()

    def ConvertText(frames, model_path, channels=1, rate=16000):
        raw_data = b"".join(frames)
        temp_wav = "tmp.wav"
        wf = wave.open(temp_wav, 'wb')
        wf.setnchannels(channels)
        wf.setsampwidth(2)
        wf.setframerate(rate)
        wf.writeframes(raw_data)
        wf.close()

        wf_read = wave.open(temp_wav, "rb")
        model = Model(model_path)
        rec = KaldiRecognizer(model, wf_read.getframerate())
        rec.AcceptWaveform(wf_read.readframes(wf_read.getnframes()))
        res = rec.Result()
        wf_read.close()
        os.remove(temp_wav)

        raw_text = json.loads(res)["text"]
        clean_text = raw_text.replace(" ", "")
        return clean_text

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

s = input()

if '音量' in s:
    if '静音' in s:
        vol.mute()
        sys.exit(0)
    if '有':
        print(vol.get_vol())
        sys.exit(0)
    num = ''
    for i in s:
        if i.isdigit():
            num += i
        else:
            if num:
                break
    if num:
        vol.set_vol(int(num))