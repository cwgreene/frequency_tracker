#!/usr/bin/env python
import pyaudio
import wave
import numpy
import struct
import argparse
import sys

def interleave(*args):
    result = numpy.vstack(args)
    result = result.ravel(order='F')
    return result

def normalize(samples):
    scalar = 2**15 - 1
    samples = scalar * samples
    samples = samples.astype(numpy.int16)
    return samples

def make_wave_file(options):
    filename = options.output_file
    if filename == None:
        channel = ""
        if options.channel != "both":
            channel = "_%s" % options.channel
        filename = "test%s%s.wav" % (options.frequency, channel)
        wf = wave.open(filename, "w")
    wf.setframerate(options.samplerate)
    wf.setnchannels(2)
    wf.setsampwidth(2)

    t = numpy.arange(0,options.samplerate)
    samples = numpy.sin(2*numpy.pi*t*float(options.frequency)/options.samplerate)
    output = {}
    output["left"] = samples
    output["right"] = samples
    if options.channel != "both":
        output[options.channel] = numpy.zeros(len(samples))
    samples = interleave(output["right"], output["left"])
    samples = normalize(samples)
    wf.writeframes(samples)

def main(args):
    parser = argparse.ArgumentParser()
    parser.add_argument("--frequency", default=440)
    parser.add_argument("--output-file", default=None)
    parser.add_argument("--samplerate", default=44100)
    parser.add_argument("--channel", choices=["left", "right", "both"], default="both")
    options = parser.parse_args(args)
    make_wave_file(options)

if __name__ == "__main__":
    main(sys.argv[1:])
