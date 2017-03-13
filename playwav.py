"""
Plays a wave file. Makes running test wavefiles
easier and more cross platform. Only needs pyaudio.
"""
import sys
import wave

import argparse
import pyaudio

CHUNK = 1024

def playfile(wavefile, audio, forever=False):
    """
    plays an opened wavefile (wave.open) using audio interface.BaseException

    wavefile - wave file opened with wave.open
    audio - pyaudio interface
    forever - (default False) whether to loop forever.
    """
    output = audio.open(
        format=audio.get_format_from_width(wavefile.getsampwidth()),
        channels=wavefile.getnchannels(),
        rate=wavefile.getframerate(),
        output=True)


    while True:
        data = wavefile.readframes(CHUNK)
        while len(data) > 0:
            output.write(data)
            data = wavefile.readframes(CHUNK)
        if not forever:
            break
        wavefile.rewind()

    output.stop_stream()
    output.close()

def main(args):
    """
    Plays a wavefile

    args - command line arguments
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("file")
    parser.add_argument("--loop", action="store_true")
    options = parser.parse_args(args)
    wavefile = wave.open(options.file, 'rb')

    audio = pyaudio.PyAudio()
    playfile(wavefile, audio, options.loop)
    audio.terminate()

if __name__ == "__main__":
    main(sys.argv[1:])
