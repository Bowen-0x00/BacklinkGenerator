from plyer import notification
def message(e):
    try:
        notification.notify(title="Error", message=str(e), timeout=5)
    except NotImplementedError:
        with open('error.log', 'w') as f:
            f.write(str(e))