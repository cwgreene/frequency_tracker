# Frequency Tracking

## Setup:
Install pyaudio (relies on portaudio)

```
brew install portaudio
pip install pyaudio
```

## Testing
Install sox, and run

```
./capture.py
```

in one terminal, and in another:

```
play -n synth sin 440
```

and you should see frequency detected close to 440.