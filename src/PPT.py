from utils.hotkey import press_hotkey_in_app
import win32com.client
from urllib.parse import urlencode
from utils.clipboard import get_image_from_clipboard
from base import Application

class PPT(Application):
    def get_data(self):
        image = get_image_from_clipboard(press_hotkey_in_app, self.config, self.name, 'hotkey-copy')
        Application = win32com.client.Dispatch("PowerPoint.Application")
        Presentation = Application.Activepresentation
        current_slide_number = Application.ActiveWindow.Selection.SlideRange.SlideNumber
        params = {'app': 'PPT', 'file': Presentation.FullName, 'page': current_slide_number}
        self.origin_link = f'ymjr://open?{urlencode(params)}'
        link = f'[page: {current_slide_number}]({self.origin_link})'
        self.data = {
            'type': 'image',
            'link': link,
            'data': image
        }

if __name__ == "__main__":
    import os
    import configparser
    from utils.message import notify
    try:
        config_path: str = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'config.conf'))
        config = configparser.ConfigParser()
        config.read(config_path, encoding='utf-8')
        ppt = PPT(config, 'PPT')
        print(ppt.construct_target('ob'))
    except Exception as e:
        print(e)
        notify('FAIL', e)