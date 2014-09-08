# coding: utf-8
# quick console
import pyHook
import os
import re
import win32con
import win32gui
import win32clipboard
import threading
import sys
import time
import subprocess
import datetime
from PySide.QtGui import *
from PySide.QtCore import *

from ctypes import pythonapi, c_void_p, py_object

VK_SEMICOLON = 186

def copyToClipboard(s):
    win32clipboard.OpenClipboard()
    win32clipboard.EmptyClipboard()
    win32clipboard.SetClipboardText(s)
    win32clipboard.CloseClipboard()

def getTextFromClipboard():
    win32clipboard.OpenClipboard()
    text = win32clipboard.GetClipboardData()
    win32clipboard.CloseClipboard()
    return text

def curDatetime(fmt=None):
    t = datetime.datetime.now()
    return t.strftime(fmt) if fmt else t

def command(cmd):
    subprocess.call(cmd, shell=True)

class Widget(QWidget):
    def __init__(self, parent=None):
        super(Widget, self).__init__(parent, Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowFlags(self.windowFlags() | Qt.Tool)
        self.resize(300, 30)
        self.cmd = []
        self.lastCmd = ''
        self.cmds = ['!yx', '!quit', 'dt', 'dh', 'cmd',
                ]
        self.cmds += [f.split('.')[0] for f in os.listdir('D:/Hotkeys')]

    def keyPressEvent(self, event):
        ch = event.text()
        # ignore ctrl-; (although this will ignore all ;)
        if not ch or ch ==';':
            return
        # backspace
        if ch == '\b':
            if self.cmd:
                self.cmd.pop()
                self.update()
        elif ch and ch in '\r\n':
            text = self.text()
            if not text or text in self.cmds:
                self.execute()
        else:
            self.cmd.append(ch)
            self.update()
            if self.matched():
                self.execute()
        
    def matched(self):
        matches = []
        text = self.text()
        for cmd in self.cmds:
            if cmd.startswith('!') and cmd[1:] == text:
                matches.append(text)
            elif cmd.startswith(text):
                matches.append(cmd)
        if len(matches) == 1 and text == matches[0]:
            self.cmd = matches[0]
            return True
        else:
            return False
        
    def text(self):
        # eliminate initial semicolon
        return ''.join(self.cmd)

    def execute(self):
        cmd = self.text()
        if not cmd:
            cmd = self.lastCmd
        # yinxiang
        if cmd == 'yx':
            command('start chrome "https://app.yinxiang.com/Home.action"')
        # date time in filename format
        elif cmd == 'dt':
            copyToClipboard(curDatetime('%Y%m%d%H%M%S'))
        # date time in readable format
        elif cmd == 'dh':
            copyToClipboard(curDatetime('%Y-%m-%d %H:%M:%S'))
        # open cmd in clipboard
        elif cmd == 'cmd':
            path = getTextFromClipboard()
            if not os.path.exists(path):
                path = '.'
            if os.path.isfile(path):
                path = os.path.dirname(path)
            command('start cmd /k cd /d {}'.format(path))
        # quit
        elif cmd == 'quit':
            exit()
        # execute in hotkeys directory
        elif cmd in self.cmds:
            command('cd /d D:/Hotkeys & start /b {}'.format(cmd))
        self.clear()

    def clear(self):
        self.lastCmd = self.text()
        self.cmd = []
        self.hide()

    def paintEvent(self, event):
        p = QPainter(self)

        rc = self.rect().adjusted(0, 0, -1, -1)
        p.fillRect(rc, QBrush(QColor(255, 255, 255)))
        rc.adjust(1, 1, -1, -1)
        p.fillRect(rc, QBrush(QColor(0, 0, 0)))

        font = p.font()
        font.setPixelSize(30)
        p.setFont(font)
        pen = p.pen()
        pen.setColor(QColor(200,200,200))
        p.setPen(pen)
        p.drawText(self.rect(), Qt.AlignCenter, self.text())

class KeyListener:
    def __init__(self, window):
        self.window = window

    def start(self):
        self.hm = pyHook.HookManager()
        self.hm.KeyAll = self.onKey
        self.hm.HookKeyboard()
        self.lctrldown = False

    def onKey(self, event):
        self.event = event
        if self.isKey(win32con.VK_LCONTROL):
            if self.isDown():
                self.lctrldown = True
            elif self.isUp():
                self.lctrldown = False
        elif self.isKey(VK_SEMICOLON) and self.lctrldown:
            if self.isDown():
                if self.window.isVisible():
                    self.window.clear()
                else:
                    self.window.show()
                    self.window.setWindowState(Qt.WindowMinimized)
                    self.window.setWindowState(Qt.WindowActive)

                    desktop = QDesktopWidget()
                    height = desktop.geometry().height()

                    pos = self.window.pos()
                    self.window.move(pos.x(), height - self.window.height() - 50)
        return True

    def isKey(self, key):
        return self.event.KeyID == key

    def isDown(self):
        return self.event.Message == win32con.WM_KEYDOWN

    def isUp(self):
        return self.event.Message == win32con.WM_KEYUP

app = QApplication(sys.argv)
w = Widget()
KeyListener(w).start()
app.exec_()
