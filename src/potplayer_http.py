import os
import configparser
from potplayer import get_potplayer_backlink_obj
import requests
from utils.message import message

def get_potplayer_backlink_http(config):
    obj = get_potplayer_backlink_obj(config)
    url = config.get('Potplayer', 'url')
    # headers = {
    #     'content-type': 'png;'
    # }
    response = requests.post(url, json=obj)
    if response.status_code == 200:
        ...
    else:
        raise requests.exceptions.HTTPError(f'requst fail! code: {response.status_code}')

if __name__ == "__main__":
    try:
        config_path: str = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'config.conf'))
        config = configparser.ConfigParser()
        config.read(config_path, encoding='utf-8')
        get_potplayer_backlink_http(config)
    except Exception as e:
        print(e)
        message(e)