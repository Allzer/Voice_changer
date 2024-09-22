import pyaudio
import numpy as np
from scipy.fftpack import rfft, irfft, fftfreq

def voice_changer():
    BLOCK_SIZE = 1024
    FORMAT = pyaudio.paFloat32
    CHANNELS = 1
    RATE = 44100

    LOWER_FACTOR = 0.8

    p = pyaudio.PyAudio()

    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    output=True)

    while True:
        audio_data = stream.read(BLOCK_SIZE)
        
        audio_array = np.frombuffer(audio_data, dtype=np.float32)
        
        freq_data = rfft(audio_array)
        freqs = fftfreq(len(audio_array), 1.0 / RATE)
        
        shifted_freq_data = np.zeros_like(freq_data)
        for i, freq in enumerate(freqs):
            new_idx = int(i * LOWER_FACTOR)
            if new_idx < len(freq_data):
                shifted_freq_data[new_idx] = freq_data[i]
        
        processed_data = irfft(shifted_freq_data)
        
        processed_data = np.asarray(processed_data, dtype=np.float32)
        processed_data = processed_data.tobytes()
        
        stream.write(processed_data)