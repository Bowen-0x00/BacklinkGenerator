import os

def convert_to_os_path(string: str):
    converted_path = string.replace('/', os.path.sep).replace('\\', os.path.sep)
    return converted_path