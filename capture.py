#!/usr/bin/env python
import pyaudio
import numpy
import itertools

FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100*4
CHUNK = 1024*4
BUFFERS = 5
RECORD_SECONDS = 5

audio = pyaudio.PyAudio()

stream = audio.open(format=pyaudio.paInt16,
        channels=CHANNELS,
        rate=RATE,
        input=True,
        frames_per_buffer=CHUNK)

for display in itertools.cycle(range(BUFFERS)):
    data = stream.read(CHUNK)
    data = numpy.fromstring(data, dtype=numpy.int16)
    if not display:
        a = data
    else:
        a = numpy.append(a, data)
    if (display + 1) % BUFFERS == 0:
        delta_t = (float(CHUNK)* BUFFERS)/RATE
        a = a - numpy.mean(a)
        fft = numpy.fft.fft(a)
        fft[CHUNK/2:] = 0 # prevents alias from being detected
        afft = numpy.abs(fft)
        amax = numpy.argmax(afft)
        print "%.3f %.3f (%.3f-%.3f)" % (amax/delta_t,
            numpy.max(afft),
            (amax-1)/delta_t,
            (amax+1)/delta_t)

stream.stop_stream()
stream.close()
audio.terminate()