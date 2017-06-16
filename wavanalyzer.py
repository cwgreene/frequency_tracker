import argparse
import sys
import wave

import numpy as np

def read_data(data):
    data = np.fromstring(data, dtype='int16')
    data = data.astype('double')
    data /= (2**15 - 1)
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
    nframes = wf.getnframes()
    frames = wf.readframes(nframes)
    frame_rate = wf.getframerate()
    t = np.arange(0, nframes, dtype='double')/(frame_rate)
    return frames, t

def main(args):
    parser = argparse.ArgumentParser()
    parser.add_argument("filename")
    parser.add_argument("--frequencies", nargs="*",
        type=float, default=[660])
    options = parser.parse_args(args)
    frames, t = read_wave(options.filename)
    channels = read_data(frames)
    for frequency in options.frequencies:
        print frequency, extract_sinusoid(t, frequency, channels[0])

if __name__ == "__main__":
    main(sys.argv[1:])

