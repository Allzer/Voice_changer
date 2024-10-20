import keyboard
import threading
from main import voice_changer, stop_voice_changer

start = 0

# Функция для обработки нажатия клавиши F7
def toggle_start(event):
    global start
    if start == 0:
        print("Starting voice changer")
        start = 1
        threading.Thread(target=voice_changer, daemon=True).start()
    else:
        print("Stopping voice changer")
        start = 0
        stop_voice_changer()

# Устанавливаем обработчик для нажатия клавиши F7
keyboard.on_press_key("F7", toggle_start)

# Бесконечный цикл для поддержания программы в активном состоянии
keyboard.wait('esc')  # Программа завершится при нажатии Esc
