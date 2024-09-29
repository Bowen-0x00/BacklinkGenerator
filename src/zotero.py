import os
import configparser
import json
from utils.hotkey import press_hotkey_in_app
from utils.image import image_to_base64
from utils.regex import get_regex_group
import regex
from utils.clipboard import set_text_to_clipboard, get_text_from_clipboard
from PIL import Image
from utils.message import notify


def get_zotero_backlink(config):
    content = get_text_from_clipboard(press_hotkey_in_app, config, 'Zotero', 'hotkey-copy')
    match = regex.search('.*\(\[pdf\]\((.*?)\).*', content)
    link = match.group(1)
    page = get_regex_group('.*page=(\d+).*', link)
    link = f'[page: {page}]({link})'
    if not content.startswith('[image]'):
        text = get_regex_group('(.*?”) \(\[.*?\]\(zotero://select/library/items/.*?\)\)', content)
        json_str = json.dumps({'link': link,'text': text})
        set_text_to_clipboard(f'ymjr:text-link{json_str}')
        return
    else:
        library_path = os.path.join(config.get('Zotero', 'library_path'), 'cache/library/')
        id = get_regex_group('.*annotation=(\w+).*', content)
        image_path = os.path.abspath(os.path.join(library_path, f'{id}.png'))
        image = Image.open(image_path)
        image_base64 = image_to_base64(image)
        json_str = json.dumps({'link': link,'img': image_base64})
        set_text_to_clipboard(f'ymjr:image-link{json_str}')

    if text:
        notify('Success', 'Text copied to clipboard successfully!')
    else:
        notify('Success', 'Image copied to clipboard successfully!')

if __name__ == "__main__":
    try:
        config_path: str = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'config.conf'))
        config = configparser.ConfigParser()
        config.read(config_path, encoding='utf-8')
        get_zotero_backlink(config)
    except Exception as e:
        print(e)
        notify(e)
