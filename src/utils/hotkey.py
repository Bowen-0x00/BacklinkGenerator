# import pyautogui
import keyboard

def press_hotkey_in_app(config, section: str, option: str):
    hotkey: str = config.get(section, option)
    keyboard.press_and_release(hotkey)
    # pyautogui.hotkey(*hotkey.split('+'))