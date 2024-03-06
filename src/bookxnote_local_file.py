import os
import configparser
import json
from utils.hotkey import press_hotkey_in_app
from utils.regex import get_regex_group
from utils.clipboard import get_image_from_clipboard, set_text_to_clipboard, get_text_from_clipboard
from utils.message import message

def get_bookxnote_backlink_local_file(config):
    link: str = get_text_from_clipboard(press_hotkey_in_app, config, 'Bookxnote', 'hotkey-link')
    page = get_regex_group('.*page=(\d)+.*', link)
    link = f'[page: {page}]({link})'
    text = get_text_from_clipboard(press_hotkey_in_app, config, 'Bookxnote', 'hotkey-content')
    if text:
        json_str = json.dumps({'link': link,'text': text})
        set_text_to_clipboard(f'ymjr:text-link{json_str}')
    else:
        notebook_path = config.get('Bookxnote', 'notebook_path')
        notebooks_json_path = f'{notebook_path}/notebooks/manifest.json'
        with open(notebooks_json_path, 'r', encoding='utf-8') as notebooks_json_file:
            notebook_id = get_regex_group('.*nb=({.*?}).*', link)
            notebooks_json_str: str = notebooks_json_file.read()
            uuid_index = notebooks_json_str.rfind(notebook_id)
            entry = get_regex_group('.*entry\":\"(.*?)\".*', notebooks_json_str[notebooks_json_str[0: uuid_index].rfind("entry"): uuid_index])
            notebook_json_path = f'{notebook_path}/notebooks/{entry}/markups.json'
            with open(notebook_json_path, 'r', encoding='utf-8') as notebook_json_file:
                notebook_json_str = notebook_json_file.read()
                uuid = get_regex_group('.*uuid=(.*)\).*', link)
                notebooks = json.loads(notebook_json_str)
                imgfile = ''
                for markup in notebooks['markups']:
                    if markup['uuid'] == uuid:
                        imgfile = markup['imgfile']
                        break
                json_str = json.dumps({'link': link, 'img_path': f'{notebook_path}/notebooks/{entry}/imgfiles/{imgfile}'})
                set_text_to_clipboard(f'ymjr:image-link{json_str}')

if __name__ == "__main__":
    try:
        config_path: str = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'config.conf'))
        config = configparser.ConfigParser()
        config.read(config_path, encoding='utf-8')
        get_bookxnote_backlink_local_file(config)
    except Exception as e:
        print(e)
        message(e)