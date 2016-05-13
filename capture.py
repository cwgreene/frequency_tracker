import pyaudio
import numpy
import itertools

FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 48000
CHUNK = 1024*8
RECORD_SECONDS = 5

audio = pyaudio.PyAudio()

stream = audio.open(format=pyaudio.paInt16,
        channels=CHANNELS,
        rate=RATE,
        input=True,
        frames_per_buffer=CHUNK)

for display in itertools.cycle([False, True]):
    data = stream.read(CHUNK)
    a = numpy.fromstring(data, dtype=numpy.int16)
    delta_t = float(CHUNK)/RATE
    a = a - numpy.mean(a)
    fft = numpy.fft.fft(a)
    fft[CHUNK/2:] = 0
    print "%.3f" % (numpy.argmax(numpy.abs(fft))/delta_t)

stream.stop_stream()
stream.close()
audio.terminate()