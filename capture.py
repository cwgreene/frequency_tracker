#!/usr/bin/env python
import argparse
import itertools
import sys

import colorama
import pyaudio
import numpy

FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100*4
CHUNK = 1024*4
BUFFERS = 5
RECORD_SECONDS = 5

def mkColor(color):
    def wrapcolor(*args, **kwargs):
        sep = kwargs.get("sep", " ")
        text = sep.join(map(str, args))
        return color + text + colorama.Fore.RESET
    return wrapcolor

red = mkColor(colorama.Fore.RED)
green = mkColor(colorama.Fore.GREEN)

def track(options):
    audio = pyaudio.PyAudio()
    rate = options.sample_rate if options.sample_rate else RATE

    stream = audio.open(format=pyaudio.paInt16,
            channels=CHANNELS,
            rate=rate,
            input=True,
            input_device_index=options.input_device_index,
            frames_per_buffer=CHUNK)

    for display in itertools.cycle(range(BUFFERS)):
        data = stream.read(CHUNK)
        data = numpy.fromstring(data, dtype=numpy.int16)
        if not display:
            a = data
        else:
            a = numpy.append(a, data)
        if (display + 1) % BUFFERS == 0:
            delta_t = (float(CHUNK)* BUFFERS)/rate
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

def list_devices():
    p = pyaudio.PyAudio()
    for i in range(p.get_device_count()):
        device = p.get_device_info_by_index(i)
        isInput = True if device["maxInputChannels"] else False
        color = green if isInput else red
        print i, device["name"], "isInput:", color(isInput)

def device_info(options):
    p = pyaudio.PyAudio()
    for key, val in p.get_device_info_by_index(options.info).items():
        print key, val

def main(args):
    parser = argparse.ArgumentParser()
    parser.add_argument("--list", action="store_true",
        help="list devices.")
    parser.add_argument("--info", type=int,
        help="get info on device with provided index.")
    parser.add_argument("--input-device-index", type=int,
        help="specify which device to use.")
    parser.add_argument("--sample-rate", type=int,
        help="specify the sample rate of the input device to use.")
    options = parser.parse_args(args)
    if options.list:
        list_devices()
    elif options.info != None:
        device_info(options)
    else:
        track(options)

if __name__ == "__main__":
    main(sys.argv[1:])
