# coding: utf-8
# quick console
from screenshot import screenshot_timely_saver

import pyHook
import win32con
import win32gui
import win32api
import win32clipboard
from PIL import ImageGrab
from PySide.QtGui import *
from PySide.QtCore import *

import time
import os
import re
import threading
import sys
import time
import subprocess
from datetime import datetime
from ctypes import pythonapi, c_void_p, py_object


VK_SEMICOLON = 186
VK_PRNTSCR = 44
SCREENSHOTS_PATH = r'E:\Depot\Pictures\screen_capture'
SCREENSHOTS_INTERVAL = 30 * 60  # 30 minutes
hotkeys = 'D:/Private/Hotkeys'

def save_screenshot():
    time.sleep(0.1)
    im = ImageGrab.grabclipboard()
    ts = datetime.strftime(datetime.now(), '%Y%m%d%H%M%S')
    fpath = os.path.join(SCREENSHOTS_PATH, ts + '.png')
    if im:
        im.save(fpath, 'png')

def copyToClipboard(s):
    win32clipboard.OpenClipboard()
    win32clipboard.EmptyClipboard()
    win32clipboard.SetClipboardText(s)
    win32clipboard.CloseClipboard()

def getTextFromClipboard():
    win32clipboard.OpenClipboard()
    try:
        text = win32clipboard.GetClipboardData()
    except TypeError:
        text = ''
    win32clipboard.CloseClipboard()
    return text

def curDatetime(fmt=None):
    t = datetime.now()
    return t.strftime(fmt) if fmt else t

def command(cmd):
    # use os.system instead subprocess.call to evade
    # the lnk folder hiding problem
    os.system(cmd)

class Widget(QWidget):
    def __init__(self, parent=None):
        super(Widget, self).__init__(parent, Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowFlags(self.windowFlags() | Qt.Tool)
        self.resize(300, 30)
        self.cmd = []
        self.lastCmd = ''
        self.cmds = [
            '!yx', '!quit', 'dt', 'dh', 'cmd', 'av', 'put',
            'rm', 'mt', 'bs', 'ba'
        ]
        self.cmds += [f.split('.')[0] for f in os.listdir(hotkeys)]
        print 'cmds: '
        print self.cmds

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
        # esc | ctrl-k
        elif ch == '\x1b' or ch == '\x0b':
            del self.cmd[:]
            self.update()
        # return | ctrl-j | ctrl-m
        elif ch and ch in '\r\n':
            text = self.text()
            if not text or text in self.cmds:
                self.execute()
        # normal char
        else:
            self.cmd.append(ch)
            self.update()
            if self.matched():
                self.execute()
            else:
                print 'no match'
        print 'current cmd: {}'.format(u''.join(self.cmd))

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
        # hide quick-console window before cmd is executed
        self.hide()
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
        # open mintty
        elif cmd == 'mt':
            path = getTextFromClipboard()
            try:
                if not os.path.exists(path):
                    raise Exception()
                if os.path.isfile(path):
                    path = os.path.dirname(path)
                path = path.replace('\\', '/')
                path = path.replace(':', '')
                path = '"/cygdrive/{}"'.format(path)
            except Exception:
                path = '~'
            print path
            command(("mintty --title \"mintty\" /bin/bash -lc 'cd {};"
                    + " exec bash'").format(path))
        elif cmd == 'ba' or cmd == 'bs':
            path = getTextFromClipboard()
            try:
                if not os.path.exists(path):
                    raise Exception()
                if os.path.isfile(path):
                    path = os.path.dirname(path)
                path = path.replace('\\', '/')
                path = path.replace(':', '')
                path = '"/cygdrive/{}"'.format(path)
            except Exception:
                path = '~'
            print path
            s = 'start bash -c \'cd {}; $SHELL\''.format(path)
            command(s)
        # random music
        elif cmd == 'rm':
            command('start pythonw rand_music.py')
        # secret
        elif cmd == 'av':
            command('start pythonw rand_movie.py')
        # put foreground window to right bottom
        elif cmd == 'put':
            import win32gui
            availGeo = QApplication.desktop().availableGeometry()
            right, bottom = availGeo.width(), availGeo.height()
            hwnd = win32gui.GetForegroundWindow()
            x, y, r, b = win32gui.GetWindowRect(hwnd)
            w = r - x
            h = b - y
            x, y = right - w, bottom - h
            win32gui.MoveWindow(hwnd, x, y, w, h, True)
        # quit
        elif cmd == 'quit':
            exit()
        # execute in hotkeys directory
        elif cmd in self.cmds:
            print 'special cmds: ', hotkeys
            print 'cmd:', cmd
            ecmd = 'start {}'.format(os.path.join(hotkeys, cmd))
            print 'ecmd:', ecmd
            command(ecmd)
        else:
            print 'oops'
            return
        self.clear(cmd)

    def clear(self, cmd=''):
        self.lastCmd = cmd
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

    def onKey(self, event):
        self.event = event
        # Ctrl-; 呼出控制台
        if (self.isKey(VK_SEMICOLON) and
                win32api.GetKeyState(win32con.VK_LCONTROL) & 0x8000):
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
                    self.window.move(
                        pos.x(), height - self.window.height() - 50)
        # 按下 PrintScreen 时保存截屏到 E:\Depot\Pictures\screen_capture
        if event.KeyID == VK_PRNTSCR:
            threading.Thread(target=save_screenshot).start()
        return True

    def isKey(self, key):
        return self.event.KeyID == key

    def isDown(self):
        return self.event.Message in (win32con.WM_KEYDOWN, win32con.WM_SYSKEYDOWN)

    def isUp(self):
        return self.event.Message in (win32con.WM_KEYUP, win32con.WM_SYSKEYUP)

from multiprocessing import Process

def f(cmd):
    os.system(cmd)

def run_task(cmd):
    p = Process(target=f, args=(cmd,))
    p.daemon = True
    p.start()

if __name__ == '__main__':
    #run_task(r'pythonw D:\Source\Python\bridge\pc-watcher\main.py')

    app = QApplication(sys.argv)
    w = Widget()
    KeyListener(w).start()
    # 半小时截屏一次
    screenshot_saver = threading.Thread(
        target=screenshot_timely_saver,
        args=(SCREENSHOTS_INTERVAL, SCREENSHOTS_PATH))
    screenshot_saver.start()
    app.exec_()
