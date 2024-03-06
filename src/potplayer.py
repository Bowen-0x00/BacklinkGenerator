import os
import configparser
import json
from utils.hotkey import press_hotkey_in_app
from utils.image import image_to_base64
from urllib.parse import urlencode
from utils.clipboard import get_image_from_clipboard, set_text_to_clipboard, get_text_from_clipboard
from utils.path import convert_to_os_path
from utils.message import message

def get_potplayer_backlink_obj(config):
    file_path: str = convert_to_os_path(get_text_from_clipboard(press_hotkey_in_app, config, 'Potplayer', 'hotkey-file-path'))
    time: str = get_text_from_clipboard(press_hotkey_in_app, config, 'Potplayer', 'hotkey-elapsed-time')
    image = get_image_from_clipboard(press_hotkey_in_app, config, 'Potplayer', 'hotkey-copy')
    image_base64 = image_to_base64(image)
    params = {'app': 'potplayer', 'file':file_path, 'seek': time}
    link = f'[{time}](ymjr://open?{urlencode(params)})'
    return {'link': link,'img': image_base64}

def get_potplayer_backlink(config):
    json_str = json_str = json.dumps(get_potplayer_backlink_obj(config))
    result = f'ymjr:image-link{json_str}'
    set_text_to_clipboard(result)

if __name__ == "__main__":
    try:
        config_path: str = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'config.conf'))
        config = configparser.ConfigParser()
        config.read(config_path, encoding='utf-8')
        get_potplayer_backlink(config)
    except Exception as e:
        print(e)
        message(e)