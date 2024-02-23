# https://pychao.com/2021/03/01/sending-desktop-notification-in-linux-with-python-with-d-bus-directly/

import dbus

item = "org.freedesktop.Notifications"

notify_interface = dbus.Interface(dbus.SessionBus().get_object(item, "/" + item.replace(".", "/")), item)

app_name = "Test"
replaces_id = 0
app_icon = "fingerprint-gui"
summary = "Hello world!"
body = "This is the notification body"
actions = []
hints = {"urgency": 3}
expire_timeout = 3000

notify_interface.Notify(app_name, replaces_id, app_icon, summary, body, actions, hints, expire_timeout)
