import os
import sys
import configparser
from utils.process import get_active_window_process_name
from potplayer import get_potplayer_backlink
from potplayer_http import get_potplayer_backlink_http
from bookxnote import get_bookxnote_backlink
from bookxnote_local_file import get_bookxnote_backlink_local_file
from zotero import get_zotero_backlink
from zotero_local_file import get_zotero_backlink_local_file
from PPT import get_PPT_backlink
from utils.message import message

app_to_func = {
    'potplayer-paste': get_potplayer_backlink,
    'potplayer-http': get_potplayer_backlink_http,
    'bookxnote-paste': get_bookxnote_backlink,
    'bookxnote-local': get_bookxnote_backlink_local_file,
    'zotero-paste': get_zotero_backlink,
    'zotero-local': get_zotero_backlink_local_file,
    'ppt-paste': get_PPT_backlink
}
def get_func(app: str, method: str='paste'):
    return app_to_func[f'{app.lower()}-{method.lower()}']

if __name__ == "__main__":
    try:
        argv = sys.argv
        config_path: str = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'config.conf'))
        config = configparser.ConfigParser()
        config.read(config_path, encoding='utf-8')
        app = 'potplayer'
        method = 'paste'
        if len(argv) < 3:
            if len(argv) == 2:
                method = argv[1]
            process_name = get_active_window_process_name()
            for section in config.sections():
                if process_name.lower() == config.get(section, 'program').lower():
                    app = section
                    break
        elif len(argv) >= 3:
            method = argv[1]
            app = argv[2]
        get_func(app, method)(config)
    except Exception as e:
        print(e)
        message(e)
        