import time
from RealtimeSTT import AudioToTextRecorder
from RealtimeTTS import TextToAudioStream, SystemEngine
from pynput import keyboard
from colors import *

is_running = False

def load_stt():
    global recorder
    recorder = AudioToTextRecorder(spinner=False, realtime_model_type="large-v2", wakeword_backend="pvporcupine", language="en", wake_words="hey google, ok google, jarvis", on_recording_start=_on_recording_start, on_recording_stop=_on_recording_stop, no_log_file=True)
    print(BRIGHT_GREEN + "stt ready!" + RESET)

def load_tts():
    global stream
    engine = SystemEngine()
    stream = TextToAudioStream(engine)
    print(BRIGHT_GREEN + "tts ready!" + RESET)

def start_keyboard():
    global listener
    listener = keyboard.Listener(on_press=_on_press,on_release=_on_release)
    listener.start()
    print(BRIGHT_GREEN + "keyboard ready!" + RESET)

def stop_keyboard():
    listener.stop()

def _on_press(key):
    global is_running
    if key == keyboard.Key.insert and is_running == False:
        recorder.start()

def _on_release(key):
    global is_running
    if key == keyboard.Key.insert and is_running == True:
        recorder.stop()

def _on_recording_start():
    global is_running
    if is_running == False:
        is_running = True
        print(BRIGHT_YELLOW + "Recording started!" + RESET)

def _on_recording_stop():
    global is_running
    if is_running == True:
        is_running = False
        print(BRIGHT_YELLOW + "Recording stopped! Transcribing..." + RESET)

def playback_response(answer: str):
    stream.feed(answer).play_async()
    while stream.is_playing():
        time.sleep(0.1)