import argparse
import sys
import wave

import numpy

def uninterleave(data):
    data = numpy.fromstring(data, dtype='int16')
    return data.reshape((2,-1), order='F')

def extract_sinusoid(t, frequency, data):
    total_t = t[-1] - t[0]
    dt = t[1]-t[0]
    n = total_t * frequency
    s = np.dot(np.sin(np.pi*2*frequency*t)*dt, data)
    c = np.dot(np.cos(np.pi*2*frequency*t)*dt, data)
    A = (2*np.pi*frequency* np.sqrt(s**2 + c**2))/(n*np.pi)
    cphi = s*(2*np.pi*frequency)/(n*A*np.pi)
    sphi = c*(2*np.pi*frequency)/(n*A*np.pi)
    return A, np.arctan2(sphi, cphi)

def read_wave(filename):
    wf = wave.open(filename, "r")
    frames = wf.readframes(wf.getnframes())
    return frames

def main(args):
    parser = argparse.ArgumentParser()
    parser.add_argument("filename")
    options = parser.parse_args(args)
    data = uninterleave(read_wave(options.filename))
    print data

if __name__ == "__main__":
    main(sys.argv[1:])

