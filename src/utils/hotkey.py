# import pyautogui
import keyboard
import time
keys_to_check = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 
                     'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 
                     'u', 'v', 'w', 'x', 'y', 'z', '1', '2', '3', '4', 
                     '5', '6', '7', '8', '9', '0', 'enter', 'space', 
                     'shift', 'ctrl', 'alt']

def wait_key_release():
    while True:
        if any(map(keyboard.is_pressed, keys_to_check)):
            time.sleep(0.1)
            continue
        else:
            break

def press_hotkey_in_app(config, section: str, option: str):
    hotkey: str = config.get(section, option)
    wait_key_release()
    keyboard.press_and_release(hotkey)
    # pyautogui.hotkey(*hotkey.split('+'))