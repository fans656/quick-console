import ctypes
import itertools
import time
from pprint import pprint

import win32con
import win32ui
import win32api
import pyHook
from PySide.QtGui import QApplication

import simulate

user32 = ctypes.windll.user32

class Listener(object):

    def __init__(self):
        self.keys = {}
        self.saved_wnds = {}

    def parse(self, e):
        self.is_key_down = e.Message in (win32con.WM_KEYDOWN, win32con.WM_SYSKEYDOWN)
        self.is_key_up = not self.is_key_down
        try:
            self.is_autorepeat = self.keys[e.KeyID]
        except KeyError:
            self.is_autorepeat = False
        if self.is_key_down:
            self.keys[e.KeyID] = True
        else:
            self.keys[e.KeyID] = False
        self.ch = e.Key
        self.key_id = e.KeyID

    def on_key(self, e):
        self.parse(e)
        if self.is_key_down and self.is_autorepeat:
            return True
        # save current foreground window
        if self.is_digit() and self.is_key_down and self.is_alt_shift_down():
            hwnd = user32.GetForegroundWindow()
            wnd = win32ui.CreateWindowFromHandle(hwnd)
            self.saved_wnds[self.ch] = wnd
            print '*' * 70
            for index, wnd in self.saved_wnds.items():
                print '{:2} {}'.format(index, wnd.GetWindowText())
            print '*' * 70
        # restore to previous foreground window
        elif self.is_digit() and self.is_key_down and self.is_ctrl_alt_down():
            index = self.ch
            if self.valid_window(index):
                keys_to_eat = [self.key_id, win32con.VK_LMENU, win32con.VK_LCONTROL]
                keys_stats = [win32api.GetAsyncKeyState(key) & 0x8000 for key in keys_to_eat]
                for key in keys_to_eat:
                    simulate.up(key)
                if not self.bring_window_to_foreground(index):
                    print 'alt-tab activate'
                    simulate.down(win32con.VK_LMENU)
                    simulate.tap(win32con.VK_TAB)
                    simulate.down(win32con.VK_LSHIFT)
                    simulate.tap(win32con.VK_TAB)
                    simulate.up(win32con.VK_LSHIFT)
                    simulate.up(win32con.VK_LMENU)
                for key, stat in reversed(zip(keys_to_eat, keys_stats)):
                    if stat:
                        simulate.down(key)
        return True

    def valid_window(self, index):
        try:
            wnd = self.saved_wnds[index]
            return wnd if wnd.IsWindow() else None
        except KeyError:
            return None

    def is_digit(self):
        return self.ch.isdigit()

    def is_ctrl_alt_down(self):
        try:
            return self.keys[win32con.VK_LCONTROL] and self.keys[win32con.VK_LMENU]
        except KeyError:
            return False

    def is_alt_shift_down(self):
        try:
            return self.keys[win32con.VK_LMENU] and self.keys[win32con.VK_LSHIFT]
        except KeyError:
            return False

    def bring_window_to_foreground(self, index):
        wnd = self.valid_window(index)
        if wnd:
            print 'Bring "{}" to foreground'.format(wnd.GetWindowText())
            if wnd.SetForegroundWindow():
                print 'native activate'
                return True
            else:
                time.sleep(0.05)
                return False
        else:
            print 'No saved foreground window at index {}'.format(index)
            return False

listener = Listener()
hm = pyHook.HookManager()
hm.KeyAll = listener.on_key
hm.HookKeyboard()

app = QApplication([])
app.exec_()
