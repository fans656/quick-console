"""
Log the raw key press/release sequence
Use <esc> to clear the log.
"""
import qt
from keyboard import Keyboard

class Logger:
    def __init__(self):
        self.seq = []

    def notify(self, event):
        if not event.autorepeat:
            self.notified(event)

    def notified(self, event):
        if str(event) == '<esc>':
            self.clear()
        elif str(event) == '<esc>^':
            pass
        else:
            self.seq.append(event)
            print ''.join(str(e) for e in self.seq)

    def clear(self):
        self.seq = []
        print '> Cleared\n'

logger = Logger()

kb = Keyboard(logger)
kb.hook()

qt.run()
