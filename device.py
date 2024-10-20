import pyaudio

def list_audio_devices():
    p = pyaudio.PyAudio()
    for i in range(p.get_device_count()):
        info = p.get_device_info_by_index(i)
        print(f"Device {i}: {info['name']}, Channels: {info['maxInputChannels']}, {info['maxOutputChannels']}")
    p.terminate()

list_audio_devices()
