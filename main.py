# coding: utf-8
# quick console
import time
import os
import re
import threading
import sys
import time
import subprocess
import multiprocessing
from datetime import datetime
from ctypes import pythonapi, c_void_p, py_object
import traceback

# https://stackoverflow.com/questions/35202087/pyhook-on-python-3-5
import pyHook
import win32con
import win32gui
import win32api
import win32clipboard
from PIL import ImageGrab
from PySide.QtGui import *
from PySide.QtCore import *

from screenshot import screenshot_timely_saver
from window import Windows
from keyboard import Keyboard
import fme_local
import config
from clipboard import Clipboard
from logger import logger
from run_tmp import run_tmp_script

SCREENSHOTS_PATH = r'C:\data\pictures\screen-capture'
SCREENSHOTS_TIMELY_PATH = r'C:\data\pictures\screen-capture\timely'
SCREENSHOTS_INTERVAL = 30 * 60  # 30 minutes
hotkeys = 'C:/apps/scripts'

VK_SEMICOLON = 186
VK_PRNTSCR = 44

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
            '!quit', 'dt', 'dh', 'cmd', 'av', 'mav', 'yav', 'put',
            'rm', 'mt', 'bs', 'ba', 'te',
            'cl', 'tm',
        ]
        self.cmds += [f.split('.')[0] for f in os.listdir(hotkeys)]
        logger.info('cmds: {}'.format(self.cmds))
        self.keyboard = Keyboard()
        self.keyboard.on('ctrl ;', self.toggle_active)
        self.keyboard.on('print', self.screenshot)

    def toggle_active(self):
        if self.isVisible():
            self.clear()
        else:
            self.show()
            self.setWindowState(Qt.WindowMinimized)
            self.setWindowState(Qt.WindowActive)

            desktop = QDesktopWidget()
            height = desktop.geometry().height()

            pos = self.pos()
            self.move(
                pos.x(), height - self.height() - 50)

    def screenshot(self):
        logger.info('screenshot')
        im = ImageGrab.grab()
        ts = datetime.strftime(datetime.now(), config.FNAME_TIMESTAMP_FORMAT)
        fpath = os.path.join(SCREENSHOTS_PATH, ts + '.png')
        if im:
            im.save(fpath, 'png')

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
                print('no match')
        print('current cmd: {}'.format(u''.join(self.cmd)))

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
        logger.info('executing: {}'.format(cmd))
        # date time in filename format
        if cmd == 'dt':
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
            command('start cmd.exe /k cd /d {}'.format(path))
        elif cmd == 'te':
            cur = Windows().current
            if not cur or not cur.path == r'C:\Windows\explorer.exe':
                return
            path = getTextFromClipboard()
            if not os.path.exists(path):
                print('path not exists')
                return
            if os.path.isfile(path):
                print('is not directory')
                return
            command(u'start gvim {}'.format(os.path.join(path, '0txt.txt')))
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
            print(path)
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
            print(path)
            s = 'start bash -c \'cd {}; $SHELL\''.format(path)
            command(s)
        # random music
        elif cmd == 'rm':
            command('start pythonw rand_music.py')
        # secret
        elif cmd == 'av':
            command('start pythonw rand_movie.py')
        elif cmd == 'mav':
            command('start pythonw rand_mmd.py')
        elif cmd == 'yav':
            command('start pythonw rand_av.py')
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
        elif cmd == 'cl':
            logger.info('cl start')
            try:
                logger.info('cl get_image')
                logger.info(repr(Clipboard))
                fname = Clipboard.get_image()
                if fname:
                    logger.info('cl: ' + fname)
                    copyToClipboard(fname)
                else:
                    logger.info('cl nothing')
            except:
                logger.info(traceback.format_exc())
            logger.info('cl end')
        elif cmd == 'tm':
            run_tmp_script()
        # quit
        elif cmd == 'quit':
            exit()
        # execute in hotkeys directory
        elif cmd in self.cmds:
            logger.info('special cmds: {}'.format(hotkeys))
            logger.info('cmd: {}'.format(cmd))
            ecmd = 'start {}'.format(os.path.join(hotkeys, cmd))
            logger.info('ecmd: {}'.format(ecmd))
            command(ecmd)
        else:
            logger.error('unknown command {}'.format(cmd))
            print('oops')
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


def update_wsl_host():
    out = subprocess.check_output('wsl.exe ifconfig', shell = True)
    lines = map(str.strip, out.decode().splitlines())
    line = next(l for l in lines if l.startswith('inet 172'))
    ip = line.split(' ')[1]
    print(repr(ip))


if __name__ == '__main__':
    try:
        update_wsl_host()
    except:
        logger.warning(traceback.format_exc())

    app = QApplication(sys.argv)
    w = Widget()

    # 半小时截屏一次
    screenshot_saver = threading.Thread(
        target=screenshot_timely_saver,
        args=(SCREENSHOTS_INTERVAL, SCREENSHOTS_TIMELY_PATH))
    screenshot_saver.daemon = True # quit when main thread is quited
    screenshot_saver.start()

    app.exec_()
