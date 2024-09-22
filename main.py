import pyaudio
import numpy as np
import matplotlib.pyplot as plt
from scipy.fftpack import rfft, irfft, fftfreq, fft

# Constants
BLOCK_SIZE = 1024
FORMAT = pyaudio.paFloat32
CHANNELS = 1
RATE = 44100

FRAMERATE_OFFSET = 1
# Initialize PyAudio
p = pyaudio.PyAudio()

# Open the audio stream
stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=int(RATE * FRAMERATE_OFFSET),
                input=True,
                output=True)

# Read and process audio data in a loop
while True:
    audio_data = stream.read(BLOCK_SIZE)
    
    audio_array = np.frombuffer(audio_data, dtype=np.float32)

    processed_data = audio_array
    processed_data = np.asarray(processed_data, dtype=np.float32)
    processed_data = processed_data.tobytes()
    
    stream.write(processed_data)
