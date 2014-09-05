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
        self.text = ''

    def keyPressEvent(self, event):
        ch = event.text()
        print ch
        if ch == '\r':
            self.execute()
        else:
            self.text += ch
            self.update()
        self.showKeyEvent(event)

    def keyReleaseEvent(self, event):
        ch = event.text()
        self.showKeyEvent(event)

    def showKeyEvent(self, event):
        attrs = {
                'count'}

    def execute(self):
        cmd = self.text[1:]
        # yinxiang
        if cmd == 'yx':
            command('start chrome "https://app.yinxiang.com/Home.action"')
        # math
        elif cmd == 'ma':
            command('"E:\\Depot\\Subject\\201405161208\\PostGraduate\\301\\bk\\A1.pdf"')
        # post graduate
        elif cmd == 'pg':
            command('explorer "E:\\Depot\\Subject\\201405161208\\PostGraduate"')
        # study time
        elif cmd == 'st':
            command('start pythonw "E:/Prog/Python/201407272013_studyTime.py"')
        # date time in filename format
        elif cmd == 'd':
            copyToClipboard(curDatetime('%Y%m%d%H%M%S'))
        # date time in readable format
        elif cmd == 'd ':
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
        self.clear()

    def clear(self):
        self.text = ''
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
        p.drawText(self.rect(), Qt.AlignCenter, self.text[1:])

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
                    self.window.hide()
                    self.window.text = ''
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
