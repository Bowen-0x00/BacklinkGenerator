# import win32clipboard
from PIL import ImageGrab  #numpy
import pyperclip#QT5
import time

TIMEOUT = 5
class TimeoutException(RuntimeError):
    pass
# def get_content_from_clipboard(format):
#     data = None
#     win32clipboard.OpenClipboard()
#     if win32clipboard.IsClipboardFormatAvailable(format):
#         data = win32clipboard.GetClipboardData(format)
#     win32clipboard.CloseClipboard()
#     return data
def clear_clipboard():
    pyperclip.copy("")

def wait_for(paste):
    def wrapper(func=None, *args, **kw):
        if 'not_set' not in kw:
            pyperclip.copy("set temp")
        if func:
            func(*args, **kw)
        startTime = time.time()
        while True:
            data = paste()
            if data != None and data != 'set temp':
                return data
            time.sleep(0.05)
            if time.time() > startTime + TIMEOUT:
                raise TimeoutException('waitForPaste() timed out after ' + str(TIMEOUT) + ' seconds.')
    return wrapper

@wait_for
def get_text_from_clipboard():
   return pyperclip.paste()
    # data = get_content_from_clipboard(win32clipboard.CF_TEXT)
    # return data.decode() if data else None
@wait_for
def get_image_from_clipboard():
    return ImageGrab.grabclipboard()
    # return get_content_from_clipboard(win32clipboard.CF_DIB)

def set_text_to_clipboard(text: str):
    pyperclip.copy(text)
    # win32clipboard.OpenClipboard()
    # win32clipboard.SetClipboardData(win32clipboard.CF_TEXT, text.encode())
    # win32clipboard.CloseClipboard()


