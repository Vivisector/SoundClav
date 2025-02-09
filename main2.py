from pynput import keyboard
import simpleaudio as sa
import ctypes
import threading

# Функция для определения текущей раскладки клавиатуры
def get_keyboard_layout():
    user32 = ctypes.WinDLL('user32', use_last_error=True)
    hwnd = user32.GetForegroundWindow()
    thread_id = user32.GetWindowThreadProcessId(hwnd, 0)
    layout_id = user32.GetKeyboardLayout(thread_id)
    return layout_id & 0xFFFF

# Функция для воспроизведения звука в отдельном потоке
def play_sound(layout_id):
    def play():
        if layout_id == 0x0419:  # Русская раскладка
            wave_obj = sa.WaveObject.from_wave_file('rus2.wav')
        else:  # Английская раскладка
            wave_obj = sa.WaveObject.from_wave_file('engl3.wav')
        play_obj = wave_obj.play()
        play_obj.wait_done()
    # Запуск звука в отдельном потоке
    threading.Thread(target=play).start()

# Обработчик нажатия клавиш
def on_press(key):
    layout_id = get_keyboard_layout()
    play_sound(layout_id)

# Запуск слушателя клавиатуры
with keyboard.Listener(on_press=on_press) as listener:
    listener.join()