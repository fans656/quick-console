"""
press key and show the keyboard event
"""
import sys

from PySide.QtGui import *

from GlobalKeyListener import GlobalKeyListener
import key

seq = key.Sequence('Ctrl+;')

listener = GlobalKeyListener()
listener.addKeySequence(seq, lambda: None)
listener.start()

app = QApplication(sys.argv)
app.exec_()
