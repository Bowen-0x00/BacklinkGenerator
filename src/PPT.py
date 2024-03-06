import os
import configparser
import json
from utils.hotkey import press_hotkey_in_app
from utils.image import image_to_base64
import win32com.client
from urllib.parse import urlencode
from utils.clipboard import get_image_from_clipboard, set_text_to_clipboard
from utils.message import message

def get_PPT_backlink(config):
    image = get_image_from_clipboard(press_hotkey_in_app, config, 'PPT', 'hotkey-copy')
    image_base64 = image_to_base64(image)
    Application = win32com.client.Dispatch("PowerPoint.Application")
    Presentation = Application.Activepresentation
    current_slide_number = Application.ActiveWindow.Selection.SlideRange.SlideNumber
    params = {'app': 'PPT', 'file': Presentation.FullName, 'page': current_slide_number}
    link = f'[page: {current_slide_number}](ymjr://open?{urlencode(params)})'
    json_str = json.dumps({'link': link,'img': image_base64})
    set_text_to_clipboard(f'ymjr:image-link{json_str}')


if __name__ == "__main__":
    try:
        config_path: str = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'config.conf'))
        config = configparser.ConfigParser()
        config.read(config_path, encoding='utf-8')
        get_PPT_backlink(config)
    except Exception as e:
        print(e)
        message(e)