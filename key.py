import util

class Event:

    ATTR_NAMES = (
            'down',
            #'up',
            #'time',
            'id',
            'autorepeat',
            'name',
            )

    def __init__(self, **kwas):
        self.__dict__.update({name: None for name in Event.ATTR_NAMES})
        self.__dict__.update(kwas)

    def __repr__(self):
        ch = self.char if self.down else self.char + '^'
        return '{:<2}'.format(ch)

class Hit:

    def __init__(self, key, modifiees):
        self.key = key
        self.modifiees = modifiees

    def __repr__(self):
        if self.modifiees:
            modifiees = ''.join(str(key) for key in self.modifiees)
            return '{}({})'.format(self.key, modifiees)
        else:
            return self.key

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
        self.undet = []
        self.det = []

    def addEventFilter(self, eventFilter):
        self.eventFilters.append(eventFilter)

    def addTrigger(self, trigger):
        pass

    def notify(self, event):
        if all(f(event) for f in self.eventFilters):
            self.notified(event)

    def notified(self, event):
        self.parse(event)
        self.isp()

    def parse(self, e):

        def takeModifiees(index):
            isHit = lambda key: isinstance(key, Hit)
            modifiees, self.undet[index:] = util.split(self.undet[index:], isHit)
            return modifiees

        c = e.name
        if e.down:
            self.undet.append(c)
        else:
            index = self.undet.index(c)
            modifiees = takeModifiees(index + 1)
            self.undet[index] = Hit(c, modifiees)
            if index == 0:
                hit = self.undet[0]
                del self.undet[0]
                self.det.append(hit)

    def isp(self):
        print self.undet
        print self.det
        print
