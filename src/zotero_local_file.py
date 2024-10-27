from PIL import Image
from utils.regex import get_regex_group
from base import Application
from zotero import Zotero

class Zotero_file(Zotero):
    def get_image(self):
        library_path = os.path.join(config.get('Zotero', 'library_path'), 'cache/library/')
        id = get_regex_group('.*annotation=(\w+).*', self.content)
        image_path = os.path.abspath(os.path.join(library_path, f'{id}.png'))
        return image_path
    
if __name__ == "__main__":
    import os
    import configparser
    from utils.message import notify
    try:
        config_path: str = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'config.conf'))
        config = configparser.ConfigParser()
        config.read(config_path, encoding='utf-8')
        zotero = Zotero_file(config, 'Zotero')
        zotero.get_data()
        print(zotero.data)
    except Exception as e:
        print(e)
        notify('FAIL', e)
