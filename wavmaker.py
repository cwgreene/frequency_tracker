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

def sin_samples(t, frequency, samplerate):
    return numpy.sin(2*numpy.pi*t*frequency/samplerate)

def impulse_samples(t, frequency, samplerate, load_factor):
    interval_length = samplerate/frequency
    intervals = t % interval_length
    off = intervals > load_factor*interval_length
    on = intervals <= load_factor*interval_length
    intervals[off] = 0
    intervals[on] = 1
    return intervals

def sawtooth_samples(t, frequency, samplerate):
    interval_length = samplerate/frequency
    intervals = t % interval_length
    return intervals / (interval_length*1.)

def create_samples(options):
    t = numpy.arange(0, options.samplerate*options.length)
    sample = numpy.zeros(len(t))
    for frequency in options.frequency:
        functions = {
            "sin": (sin_samples, [t, frequency, options.samplerate]),
            "impulse": (impulse_samples, [t, frequency, options.samplerate, options.load_factor]),
            "sawtooth": (sawtooth_samples, [t, frequency, options.samplerate])
        }
        function, args = functions[options.shape]
        sample += function(*args)
    return sample / len(options.frequency)

def make_wave_file(options):
    filename = options.output_file
    if filename == None:
        channel = ""
        if options.channel != "both":
            channel = "_%s" % options.channel
        frequencies = "_".join(map(str, options.frequency))
        filename = "test_%s_%s%s.wav" % (options.shape, frequencies, channel)
        print("Outputing to %s" % filename)
    wf = wave.open(filename, "w")
    wf.setframerate(options.samplerate)
    wf.setnchannels(2)
    wf.setsampwidth(2)

    samples = create_samples(options)
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
    parser.add_argument("--frequency", nargs='*', type=float, default=[440.])
    parser.add_argument("--output-file", default=None)
    parser.add_argument("--samplerate", default=44100, type=int)
    parser.add_argument("--length", type=float, default=1)
    parser.add_argument("--channel", choices=["left", "right", "both"], default="both")
    parser.add_argument("--shape", choices=["sin", "impulse", "sawtooth"], default="sin")
    parser.add_argument("--load-factor", type=float, default=.1)
    options = parser.parse_args(args)
    make_wave_file(options)

if __name__ == "__main__":
    main(sys.argv[1:])
