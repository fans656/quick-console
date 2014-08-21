import pyHook

import key

KEYDOWN_MSGS = (
        pyHook.HookConstants.WM_KEYDOWN,
        pyHook.HookConstants.WM_SYSKEYDOWN,
        )

CANONICAL_NAMES = {
        'lcontrol': 'lc',
        'escape': 'esc',
        'oem_1': ';',
        }

class Keyboard:

    downs = set()

    @staticmethod
    def normalizedName(name):
        name = name.lower()
        try:
            name = CANONICAL_NAMES[name]
        except KeyError:
            pass
        return name

    @staticmethod
    def normalizedEvent(e):
        d = {}
        d['name'] = Keyboard.normalizedName(e.Key)
        d['keyid'] = e.KeyID
        d['down'] = e.Message in KEYDOWN_MSGS
        d['autorepeat'] = d['down'] and d['keyid'] in Keyboard.downs
        return key.Event(**d)

    @staticmethod
    def updateState(e):
        if e.down:
            Keyboard.downs.add(e.keyid)
        else:
            Keyboard.downs.discard(e.keyid)

    def __init__(self, *notifiees):
        self.notifiees = notifiees
        self.hm = pyHook.HookManager()

    def add(self, notifiee):
        self.notifiees.append(notifiee)

    def hook(self):
        self.hm.KeyAll = self.onkey
        self.hm.HookKeyboard()

    def unhook(self):
        self.hm.UnhookKeyboard()

    def onkey(self, event):
        e = Keyboard.normalizedEvent(event)
        Keyboard.updateState(e)
        for notifiee in self.notifiees:
            notifiee.notify(e)
        return True
