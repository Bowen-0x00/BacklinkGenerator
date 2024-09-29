from plyer import notification
def notify(title, message, timeout=2):
    try:
        notification.notify(title=title, message=str(message), timeout=timeout)
    except NotImplementedError:
        with open('error.log', 'w') as f:
            f.write(str(message))


            