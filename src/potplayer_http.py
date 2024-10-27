from utils.hotkey import press_hotkey_in_app
from urllib.parse import urlencode
from utils.clipboard import get_image_from_clipboard, get_text_from_clipboard
from utils.path import convert_to_os_path
from potplayer import Potplayer
from utils.image import image_to_base64
import requests
class Potplayer_http(Potplayer):
    def construct_target(self, target):
        self.get_data()
        if target == 'ob':
            self.data['data'] = image_to_base64(self.data['data']) if self.data['type'] == 'image' else self.data['data']
            url = self.config.get(self.name, 'url')
            response = requests.post(url, json=self.data)
            if response.status_code == 200:
                notify('Success', 'Image post successfully!')
            else:
                raise requests.exceptions.HTTPError(f'requst fail! code: {response.status_code}')
        else:
            super().construct_target()

if __name__ == "__main__":
    import os
    import configparser
    from utils.message import notify
    try:
        config_path: str = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'config.conf'))
        config = configparser.ConfigParser()
        config.read(config_path, encoding='utf-8')
        potplayer = Potplayer_http(config, 'Potplayer')
        print(potplayer.construct_target('ob'))
    except Exception as e:
        print(e)
        notify('FAIL', e)