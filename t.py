"""
press key and show the keyboard event
"""
import sys

from PySide.QtGui import *

from GlobalKeyListener import GlobalKeyListener
import key

trigPool = key.TriggerPool()
trigPool.addEventFilter(lambda e: not e.autorepeat)

trig = key.Trigger('Ctrl+;', lambda: None)

listener = GlobalKeyListener(trigPool)
listener.addTrigger(trig)
listener.start()

app = QApplication(sys.argv)
app.exec_()
