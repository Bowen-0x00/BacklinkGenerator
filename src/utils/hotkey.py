# import pyautogui
import keyboard
import time
keys_to_check = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 
                     'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 
                     'u', 'v', 'w', 'x', 'y', 'z', '1', '2', '3', '4', 
                     '5', '6', '7', '8', '9', '0', 'enter', 'space', 
                     'shift', 'ctrl', 'alt']

def wait_key_release():
    start_time = time.time()
    current_time = start_time 
    while current_time - start_time > 3.0:
        if any(map(keyboard.is_pressed, keys_to_check)):
            time.sleep(0.02)
            current_time = time.time()
            continue
        else:
            break
def press_and_release(hotkey):
    parsed = keyboard.parse_hotkey(hotkey)
    for step in parsed:
        for scan_codes in step:
            keyboard._os_keyboard.press(scan_codes[0])
            time.sleep(0.01)
        time.sleep(0.05)
        for scan_codes in reversed(step):
            keyboard._os_keyboard.release(scan_codes[0])
            time.sleep(0.01)

def press_hotkey_in_app(config, section: str, option: str):
    hotkey: str = config.get(section, option)
    wait_key_release()
    press_and_release(hotkey)
    # pyautogui.hotkey(*hotkey.split('+'))