from PIL import Image
from utils.regex import get_regex_group
from base import Application
import os

class Zotero(Application):
    def get_link(self) -> str:
        content = super().get_link('hotkey-copy')
        self.content = content
        self.origin_link = get_regex_group('.*\(\[pdf\]\((.*?)\).*', content)
        return self.origin_link
    
    def get_text(self) -> str:
        text = get_regex_group('(.*?”) \(\[.*?\]\(zotero://select/library/items/.*?\)\)', self.content)
        return text

    def get_image(self):
        library_path = os.path.join(self.config.get('Zotero', 'library_path'), 'cache/library/')
        id = get_regex_group('.*annotation=(\w+).*', self.content)
        image_path = os.path.abspath(os.path.join(library_path, f'{id}.png'))
        image = Image.open(image_path)
        return image

if __name__ == "__main__":
    import configparser
    from utils.message import notify
    try:
        config_path: str = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'config.conf'))
        config = configparser.ConfigParser()
        config.read(config_path, encoding='utf-8')
        zotero = Zotero(config, 'Zotero')
        zotero.get_data()
        print(zotero.data)
    except Exception as e:
        print(e)
        notify('FAIL', e)