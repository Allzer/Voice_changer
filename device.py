import pyaudio

p = pyaudio.PyAudio()

# Вывод списка доступных аудиоустройств
print("Available audio devices:")
for i in range(p.get_device_count()):
    dev = p.get_device_info_by_index(i)
    print(f"{i}: {dev['name']}")

p.terminate()
