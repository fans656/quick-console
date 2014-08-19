class Event:

    ATTR_NAMES = (
            'down',
            #'up',
            #'time',
            'id',
            'autorepeat',
            'char',
            )

    def __init__(self, **kwas):
        self.__dict__.update({name: None for name in Event.ATTR_NAMES})
        self.__dict__.update(kwas)

    def __repr__(self):
        ch = self.char if self.down else self.char + '^'
        return '{:<2}'.format(ch)

class Sequence(unicode):

    @staticmethod
    def normalized(seq):
        return seq.lower()

    def __new__(cls, seq):
        seq = cls.normalized(seq)
        return unicode.__new__(cls, seq)

class Trigger:
    def __init__(self, seq, *callbacks):
        if isinstance(seq, unicode):
            seq = Sequence(seq)
        self.callbacks = callbacks

class TriggerPool:

    def __init__(self):
        self.eventFilters = []
        from collections import deque
        self.queue = deque()

    def addEventFilter(self, eventFilter):
        self.eventFilters.append(eventFilter)

    def addTrigger(self, trigger):
        pass

    def notify(self, event):
        if all(f(event) for f in self.eventFilters):
            self.notified(event)

    def notified(self, event):
        ch = event.char
        if event.down:
            self.queue.append(ch)
        else:
            if ch != self.queue.popleft():
                print 'fifo not satisfied'
        print list(self.queue)
