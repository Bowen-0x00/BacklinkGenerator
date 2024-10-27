from utils.regex import get_regex_group
from base import Application

class BookxNote(Application):
    def is_text(self):
        self.text = self.get_text()
        return bool(self.text)
    
    def get_page(self, link):
        page = get_regex_group('.*page=(\d+).*', link)
        return page

if __name__ == "__main__":
    import os
    import configparser
    from utils.message import notify
    try:
        config_path: str = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'config.conf'))
        config = configparser.ConfigParser()
        config.read(config_path, encoding='utf-8')
        bookxtote = BookxNote(config, 'Bookxnote')
        bookxtote.get_data()
        print(bookxtote.data)
    except Exception as e:
        print(e)
        notify('FAIL', e)