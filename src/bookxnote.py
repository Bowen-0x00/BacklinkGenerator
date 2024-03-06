import os
import configparser
import json
from utils.hotkey import press_hotkey_in_app
from utils.clipboard import get_image_from_clipboard, set_text_to_clipboard, get_text_from_clipboard
from utils.image import image_to_base64
from utils.regex import get_regex_group
from utils.message import message


def get_bookxnote_backlink(config):
    link: str = get_text_from_clipboard(press_hotkey_in_app, config, 'Bookxnote', 'hotkey-link')
    page = get_regex_group('.*page=(\d)+.*', link)
    link = f'[page: {page}]({link})'
    text = get_text_from_clipboard(press_hotkey_in_app, config, 'Bookxnote', 'hotkey-content')
    if text:
        json_str = json.dumps({'link': link,'text': text})
        set_text_to_clipboard(f'ymjr:text-link{json_str}')
    else:
        image = get_image_from_clipboard(not_set=True)
        image_base64 = image_to_base64(image)
        json_str = json.dumps({'link': link,'img': image_base64})
        set_text_to_clipboard(f'ymjr:image-link{json_str}')
        
        
if __name__ == "__main__":
    try:
        config_path: str = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'config.conf'))
        config = configparser.ConfigParser()
        config.read(config_path, encoding='utf-8')
        get_bookxnote_backlink(config)
    except Exception as e:
        print(e)
        message(e)