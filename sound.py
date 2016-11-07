"""PyAudio Example: Play a WAVE file."""

import pyaudio
import wave
import sys
from time import time
from threading import Thread


def play(sound, etime=99999):
    sound = "sounds/" + sound
    thread = Thread(target=doNothing, args=(sound, etime,))
    thread.start()
    return thread

def doNothing(a, b):
    pass

def playSound(sound, etime=99999):
    CHUNK = 1024
    begTime = time()

    wf = wave.open(sound, 'rb')

    p = pyaudio.PyAudio()

    stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                    channels=wf.getnchannels(),
                    rate=wf.getframerate(),
                    output=True)

    data = wf.readframes(CHUNK)

    while data != '':
        stream.write(data)
        data = wf.readframes(CHUNK)
        stime = time() - begTime
        if stime > etime:
            print("STOPPED THE SOUND")
            break

    stream.stop_stream()
    stream.close()

    p.terminate()
