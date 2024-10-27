from utils.hotkey import press_hotkey_in_app
from urllib.parse import urlencode
from utils.clipboard import get_image_from_clipboard, get_text_from_clipboard
from utils.path import convert_to_os_path
from base import Application
from utils.regex import get_regex_group

class Eagle(Application):
    def get_data(self):
        path: str = get_text_from_clipboard(press_hotkey_in_app, self.config, self.name, 'hotkey-copy')
        id = get_regex_group('\.library.*?images.*?([A-Z|0-9]+)\.info', path)
        link = f'eagle://item/{id}'
        self.data = {
            'type': 'image_path',
            'link': link,
            'data': path
        }
        
if __name__ == "__main__":
    import os
    import configparser
    from utils.message import notify
    try:
        config_path: str = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'config.conf'))
        config = configparser.ConfigParser()
        config.read(config_path, encoding='utf-8')
        eagle = Eagle(config, 'Eagle')
        eagle.get_data()
        print(eagle.data)
    except Exception as e:
        print(e)
        notify('FAIL', e)