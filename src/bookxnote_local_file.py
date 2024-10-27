from utils.regex import get_regex_group
from bookxnote import BookxNote
import json

class BookxNote_local(BookxNote):
    def get_image(self):
        notebook_path = self.config.get('Bookxnote', 'notebook_path')
        notebooks_json_path = f'{notebook_path}/notebooks/manifest.json'
        with open(notebooks_json_path, 'r', encoding='utf-8') as notebooks_json_file:
            notebook_id = get_regex_group('.*nb=({.*?}).*', self.link)
            notebooks_json_str: str = notebooks_json_file.read()
            uuid_index = notebooks_json_str.rfind(notebook_id)
            entry = get_regex_group('.*entry\":\"(.*?)\".*', notebooks_json_str[notebooks_json_str[0: uuid_index].rfind("entry"): uuid_index])
            notebook_json_path = f'{notebook_path}/notebooks/{entry}/markups.json'
            with open(notebook_json_path, 'r', encoding='utf-8') as notebook_json_file:
                notebook_json_str = notebook_json_file.read()
                uuid = get_regex_group('.*uuid=(.*)', self.link)
                notebooks = json.loads(notebook_json_str)
                imgfile = ''
                for markup in notebooks['markups']:
                    if markup['uuid'] == uuid:
                        imgfile = markup['imgfile']
                        break
                return f'{notebook_path}/notebooks/{entry}/imgfiles/{imgfile}'       

if __name__ == "__main__":
    import os
    import configparser
    from utils.message import notify
    try:
        config_path: str = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'config.conf'))
        config = configparser.ConfigParser()
        config.read(config_path, encoding='utf-8')
        bookxtote = BookxNote_local(config, 'Bookxnote')
        bookxtote.get_data()
        print(bookxtote.data)
    except Exception as e:
        print(e)
        notify('FAIL', e)