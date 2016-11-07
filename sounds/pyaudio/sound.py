"""PyAudio Example: Play a WAVE file."""

import pyaudio
import wave
import sys
from threading import Thread

def play(sound):
	thread = Thread(target = playSound, args=(sound,))
	thread.start()

def playSound(sound):
	CHUNK = 1024
	
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
	
	stream.stop_stream()
	stream.close()
	
	p.terminate()

