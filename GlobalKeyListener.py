import pyHook

import key

KEY_DOWN_MSGS = (
        pyHook.HookConstants.WM_KEYDOWN,
        pyHook.HookConstants.WM_SYSKEYDOWN)

class GlobalKeyListener:
    def __init__(self):
        self.trigerPool = key.TrigerPool()
        self.downKeys = set()

    def addKeySequence(self, seq, callback):
        self.trigerPool.add(seq, callback)

    def start(self):
        self.hookManager = pyHook.HookManager()
        self.hookManager.KeyAll = self.onKey
        self.hookManager.HookKeyboard()

    def onKey(self, event):
        e = key.Event()
        e.time = event.Time
        e.id = event.KeyID
        e.down = event.Message in KEY_DOWN_MSGS
        e.up = not e.down
        e.autoRepeat = e.down and e.id in self.downKeys

        if e.down:
            self.downKeys.add(e.id)
        else:
            self.downKeys.discard(e.id)

        self.trigerPool.notify(e)
        return True
