import json
from utils.clipboard import get_text_from_clipboard, set_text_to_clipboard, get_image_from_clipboard
from utils.image import image_to_base64
from functools import wraps
from utils.message import notify
from utils.hotkey import press_hotkey_in_app
from utils.regex import get_regex_group
import requests
import os
import base64
from PIL import Image
import io
from datetime import datetime
from anki import AnkiNoteUpdater

def notify_on_empty_data(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        result = func(self, *args, **kwargs)
        if not self.data or 'type' not in self.data or not self.data['type']:
            notify('Fail', 'Fail to get data!')
        return result
    return wrapper

class Application:
    def __init__(self, config, name):
        self.config = config
        self.name = name
        self.data = None
        self.content = None
        self.text = None
        self.link = None

    def get_link(self, hotkey = 'hotkey-link') -> str:
        link: str = get_text_from_clipboard(press_hotkey_in_app, self.config, self.name, hotkey)
        self.origin_link = link
        return link
    
    def get_text(self) -> str:
        text = get_text_from_clipboard(press_hotkey_in_app, self.config, self.name, 'hotkey-content')
        return text

    def get_image(self):
        image = get_image_from_clipboard(not_set=True)
        return image

    def get_page(self, link: str) -> str:
        page = get_regex_group('.*page=(\d+).*', link)
        return page
    
    def is_text(self):
        return not self.content.startswith('[image]')
    
    @notify_on_empty_data
    def get_data(self):
        self.get_link()
        page = self.get_page(self.origin_link)
        link = f'[page: {page}]({self.origin_link})'
        self.link = link
        data = None
        type = None
        if self.is_text():
            text = self.text if self.text else self.get_text()
            data = text
            type = 'text'
        else:
            image = self.get_image()
            data = image
            type = 'image_path' if isinstance(image, str) else 'image'
        self.data = {
            'type': type,
            'data': data,
            'link': link
        }

    def construct_target(self, target, args=None):
        self.get_data()
        if target == 'ob':
            if self.data and self.data['type']:
                self.data['data'] = image_to_base64(self.data['data']) if self.data['type'] == 'image' else self.data['data']
                json_str = json.dumps(self.data)
                set_text_to_clipboard(f'ymjr:{json_str}')
                notify('Success!', f'{"Text" if self.data["type"] == "text" else "Image"} copy to clipboard success!')
        elif target == 'eagle':
            url = self.config.get('Eagle', 'url')
            token = self.config.get('Eagle', 'token')
            if self.data['type'] == 'image_path':
                data = {
                    "path": self.data['data'],
                    "name": os.path.basename(self.data['data']),
                    "website": '',
                    "tags": [self.name],
                    "token": token,
                }

                url = f"{url}/api/item/addFromPath"
            else:
                buffered = io.BytesIO()
                self.data['data'].save(buffered, format="PNG")
                img_byte = buffered.getvalue()
                
                now = datetime.now()        
                data = {
                    "url": f"data:image/png;base64,{base64.b64encode(img_byte).decode('utf-8')}",
                    "name": f'{self.name}_{now.strftime("%Y-%m-%d %H:%M:%S")}',
                    "website": self.origin_link,
                    "tags": [self.name],
                    "token": token,
                }

                url = f"{url}/api/item/addFromURL"
            json_data = json.dumps(data)
            headers = {
                'Content-Type': 'application/json'
            }
            try:
                response = requests.post(url, data=json_data, headers=headers)
                response.raise_for_status()
                result = response.json()
                print(result)
            except requests.exceptions.RequestException as error:
                print('error', error)
        elif target == 'anki':
            anki = AnkiNoteUpdater(self.config, self, args)
            if self.text and self.link:
                anki.process_app_request()
            else:
                notify("Anki发送失败", "未能同时获取到文本和链接。")
            return