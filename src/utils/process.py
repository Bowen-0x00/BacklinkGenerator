import pygetwindow as gw
import psutil
import win32process

def get_active_window_process_name():
    window = gw.getActiveWindow()
    thread_id, process_id = win32process.GetWindowThreadProcessId(window._hWnd)
    process = psutil.Process(process_id)
    process_name = process.name()
    return process_name