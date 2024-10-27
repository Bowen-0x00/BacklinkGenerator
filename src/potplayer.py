from utils.hotkey import press_hotkey_in_app
from urllib.parse import urlencode
from utils.clipboard import get_image_from_clipboard, get_text_from_clipboard
from utils.path import convert_to_os_path
from base import Application

class Potplayer(Application):
    def get_data(self):
        file_path: str = convert_to_os_path(get_text_from_clipboard(press_hotkey_in_app, self.config, self.name, 'hotkey-file-path'))
        time: str = get_text_from_clipboard(press_hotkey_in_app, self.config, self.name, 'hotkey-elapsed-time')
        image = get_image_from_clipboard(press_hotkey_in_app, self.config, self.name, 'hotkey-copy')
        params = {'app': 'potplayer', 'file':file_path, 'seek': time}
        self.origin_link = f'ymjr://open?{urlencode(params)}'
        link = f'[{time}]({self.origin_link})'
        self.data = {
            'type': 'image',
            'link': link,
            'data': image
        }

if __name__ == "__main__":
    import os
    import configparser
    from utils.message import notify
    try:
        config_path: str = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'config.conf'))
        config = configparser.ConfigParser()
        config.read(config_path, encoding='utf-8')
        potplayer = Potplayer(config, 'Potplayer')
        print(potplayer.construct_target('eagle'))
    except Exception as e:
        print(e)
        notify('FAIL', e)