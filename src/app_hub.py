import os
import configparser
import argparse
from utils.process import get_active_window_process_name
from utils.message import notify

from base import Application
from bookxnote import BookxNote
from bookxnote_local_file import BookxNote_local
from potplayer import Potplayer
from potplayer_http import Potplayer_http
from PPT import PPT
from zotero import Zotero
from zotero_local_file import Zotero_file
from eagle import Eagle
import time

def get_application(config, app_name, method='paste') -> Application:
    app_classes = {
        'potplayer': {
            'paste': Potplayer,
            'http': Potplayer_http
        },
        'bookxnote': {
            'paste': BookxNote,
            'local': BookxNote_local
        },
        'ppt': {
            'paste': PPT
        },
        'zotero': {
            'paste': Zotero,
            'local': Zotero_file
        },
        'eagle': {
            'local': Eagle
        }
    }
    
    app_name_lower = app_name.lower()
    method_lower = method.lower()
    
    if app_name_lower not in app_classes:
        raise ValueError(f"Application {app_name} is not supported.")

    method_classes = app_classes[app_name_lower]

    app_class = method_classes.get(method_lower)
    if not app_class:
        app_class = next(iter(method_classes.values()))
    
    return app_class(config, app_name)


def parse_arguments():
    parser = argparse.ArgumentParser(description="Genetate annotation to other app")
    parser.add_argument('--app', type=str, default='', help='The application to use')
    parser.add_argument('--method', type=str, default='paste', help='The method to use')
    parser.add_argument('--target', type=str, default='ob', help='The target structure to construct')
    parser.add_argument('--extra', type=str, help='Any extra information needed')

    return parser.parse_args()

if __name__ == "__main__":
    try:
        args = parse_arguments()
        config_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'config.conf'))
        config = configparser.ConfigParser()
        config.read(config_path, encoding='utf-8')

        app_name = args.app
        method = args.method
        target = args.target

        if not app_name:
            process_name = get_active_window_process_name()
            for section in config.sections():
                if process_name.lower() == config.get(section, 'program').lower():
                    app_name = section
                    break

        app: Application = get_application(config, app_name, method)
        constructed_target = app.construct_target(target, args.extra)
    except Exception as e:
        print(e)
        notify('FAIL', e)
