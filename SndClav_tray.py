import sys
import os
import simpleaudio as sa
import threading
import ctypes
from pynput import keyboard
from PyQt6.QtWidgets import QApplication, QSystemTrayIcon, QMenu
from PyQt6.QtGui import QIcon, QAction

def resource_path(relative_path):
    """Корректный путь к ресурсам (для exe и исходников)"""
    try:
        if getattr(sys, 'frozen', False):
            return os.path.join(sys._MEIPASS, relative_path)
        return os.path.join(os.path.dirname(__file__), relative_path)
    except Exception as e:
        print(f"Ошибка пути: {e}")
        return relative_path

# Пути к файлам
engl3_path = resource_path("engl3.wav")
rus2_path = resource_path("rus2.wav")
icon_path = resource_path("icon.png")

def get_keyboard_layout():
    """Определяет текущую раскладку клавиатуры"""
    user32 = ctypes.WinDLL('user32', use_last_error=True)
    hwnd = user32.GetForegroundWindow()
    thread_id = user32.GetWindowThreadProcessId(hwnd, 0)
    layout_id = user32.GetKeyboardLayout(thread_id)
    return layout_id & 0xFFFF

def play_sound(layout_id):
    """Проигрывает звук в зависимости от раскладки"""
    def play():
        sound_file = rus2_path if layout_id == 0x0419 else engl3_path
        wave_obj = sa.WaveObject.from_wave_file(sound_file)
        wave_obj.play()
    threading.Thread(target=play, daemon=True).start()

def on_press(key):
    """Вызывается при нажатии клавиши"""
    layout_id = get_keyboard_layout()
    play_sound(layout_id)

class SystemTrayApp:
    def __init__(self):
        self.app = QApplication(sys.argv)

        if not QSystemTrayIcon.isSystemTrayAvailable():
            print("Системный трей недоступен!")
            sys.exit(1)

        self.tray_icon = QSystemTrayIcon(QIcon(icon_path), self.app)

        # Создание меню трея
        self.menu = QMenu()
        self.quit_action = QAction("Выход", self.menu)
        self.quit_action.triggered.connect(self.exit_app)
        self.menu.addAction(self.quit_action)

        # Проверим, если иконка null
        if self.tray_icon.icon().isNull():
            print(f"Не удалось добавить иконку в трей: {icon_path}")
        else:
            print("Иконка добавлена в трей успешно!")

        self.tray_icon.setContextMenu(self.menu)
        self.tray_icon.show()

        # Запускаем слушателя клавиатуры
        self.listener = keyboard.Listener(on_press=on_press)
        self.listener.start()

    def run(self):
        self.app.exec()

    def exit_app(self):
        self.tray_icon.hide()
        sys.exit()

if __name__ == "__main__":
    tray = SystemTrayApp()
    tray.run()
