import pyaudio
import numpy as np
from scipy.fftpack import rfft, irfft, fftfreq
import threading
import time

# Создание флага остановки для управления потоком изменения голоса
stop_flag = threading.Event()
voice_thread = None
direct_thread = None

# Задайте индексы ваших устройств
INPUT_DEVICE_INDEX = 2  # Физический микрофон
OUTPUT_DEVICE_INDEX = 7  # Виртуальный микрофон

def voice_changer():
    global voice_thread, direct_thread
    if voice_thread is not None and voice_thread.is_alive():
        return

    if direct_thread is not None and direct_thread.is_alive():
        stop_flag.set()
        direct_thread.join()

    voice_thread = threading.Thread(target=_voice_changer, daemon=True)
    voice_thread.start()

def _voice_changer():
    global stop_flag
    stop_flag.clear()

    BLOCK_SIZE = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 44100
    LOWER_FACTOR = 0.8

    p = pyaudio.PyAudio()
    stream = None

    try:
        stream = p.open(format=FORMAT,
                        channels=CHANNELS,
                        rate=RATE,
                        input=True,
                        output=True,
                        input_device_index=INPUT_DEVICE_INDEX,
                        output_device_index=OUTPUT_DEVICE_INDEX)

        while not stop_flag.is_set():
            audio_data = stream.read(BLOCK_SIZE)
            audio_array = np.frombuffer(audio_data, dtype=np.int16)

            freq_data = rfft(audio_array)
            freqs = fftfreq(len(audio_array), 1.0 / RATE)

            shifted_freq_data = np.zeros_like(freq_data)
            for i, freq in enumerate(freqs):
                new_idx = int(i * LOWER_FACTOR)
                if new_idx < len(freq_data):
                    shifted_freq_data[new_idx] = freq_data[i]

            processed_data = irfft(shifted_freq_data)
            processed_data = np.asarray(processed_data, dtype=np.int16)
            processed_data = processed_data.tobytes()

            stream.write(processed_data)

    except Exception as e:
        print(f"Error during voice changing: {e}")

    finally:
        if stream is not None:
            stream.stop_stream()
            stream.close()
        p.terminate()

def direct_audio_pass():
    global stop_flag
    stop_flag.clear()

    BLOCK_SIZE = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 44100

    p = pyaudio.PyAudio()
    stream = None

    try:
        stream = p.open(format=FORMAT,
                        channels=CHANNELS,
                        rate=RATE,
                        input=True,
                        output=True,
                        input_device_index=INPUT_DEVICE_INDEX,
                        output_device_index=OUTPUT_DEVICE_INDEX)

        while not stop_flag.is_set():
            audio_data = stream.read(BLOCK_SIZE)
            stream.write(audio_data)

    except Exception as e:
        print(f"Error during direct audio pass: {e}")

    finally:
        if stream is not None:
            stream.stop_stream()
            stream.close()
        p.terminate()

def stop_voice_changer():
    global direct_thread
    stop_flag.set()
    if voice_thread is not None:
        voice_thread.join()

    direct_thread = threading.Thread(target=direct_audio_pass, daemon=True)
    direct_thread.start()
