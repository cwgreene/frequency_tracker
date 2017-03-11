"""
Plays a wave file. Makes running test wavefiles
easier and more cross platform. Only needs pyaudio.
"""
import sys
import wave

import argparse
import pyaudio

CHUNK = 1024

def main(args):
    """
    Plays a wavefile

    args - command line arguments
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("file")
    options = parser.parse_args(args)
    wavefile = wave.open(options.file, 'rb')

    audio = pyaudio.PyAudio()

    output = audio.open(
        format=audio.get_format_from_width(wavefile.getsampwidth()),
        channels=wavefile.getnchannels(),
        rate=wavefile.getframerate(),
        output=True)

    data = wavefile.readframes(CHUNK)

    while len(data) > 0:
        output.write(data)
        data = wavefile.readframes(CHUNK)

    output.stop_stream()
    output.close()

    audio.terminate()

if __name__ == "__main__":
    main(sys.argv)
