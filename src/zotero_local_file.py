import os
import configparser
import json
from utils.hotkey import press_hotkey_in_app
from utils.regex import get_regex_group
import regex
from utils.clipboard import set_text_to_clipboard, get_text_from_clipboard
from utils.message import notify

def get_zotero_backlink_local_file(config):
    content = get_text_from_clipboard(press_hotkey_in_app, config, 'Zotero', 'hotkey-copy')
    match = regex.search('.*\(\[pdf\]\((.*?)\).*', content)
    link = match.group(1)
    page = get_regex_group('.*page=(\d)+.*', link)
    link = f'[page: {page}]({link})'
    if not content.startswith('[image]'):
        text = content[match.regs[0][0]: match.regs[0][1]]
        json_str = json.dumps({'link': link,'text': text})
        set_text_to_clipboard(f'ymjr:text-link{json_str}')
        return
    else:
        library_path = config.get('Zotero', 'library_path')
        id = get_regex_group('.*annotation=(\w+).*', content)
        image_path = os.path.abspath(os.path.join(library_path, f'{id}.png'))
        json_str = json.dumps({'link': link, 'img_path': image_path})
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
        get_zotero_backlink_local_file(config)
    except Exception as e:
        print(e)
        notify(e)
