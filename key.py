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

    CANONICAL_NAMES = {
            'Lcontrol': 'ctrl',
            'Rcontrol': 'ctrl',
            'Oem_1':    ';',
            'Return':   'enter',
            }

    def __init__(self, **kwas):
        self.__dict__.update({name: None for name in Event.ATTR_NAMES})
        self.__dict__.update(kwas)

    def __repr__(self):
        if self.down:
            return self.name
        else:
            return self.name + '^'

    def normalize(self):
        try:
            self.name = Event.CANONICAL_NAMES[self.name]
        except KeyError:
            pass
        self.name = self.name.lower()
        if len(self.name) > 1:
            self.name = '<{}>'.format(self.name)

class Hit:

    @staticmethod
    def key2str(*keys):
        return ''.join(str(key) for key in keys)

    @staticmethod
    def name2str(name):
        return name if len(name) == 1 else '<{}>'.format(name)

    def __init__(self, modifier, modifiees):
        self.modifier = modifier
        self.modifiees = modifiees

    def __repr__(self):
        modifier = Hit.name2str(self.modifier.name)
        if self.modifiees:
            modifiees = Hit.key2str(*self.modifiees)
            return '{}({})'.format(modifier, modifiees)
        else:
            return modifier

class Trigger:

    def __init__(self, seq, callbacks, eaters=[]):
        self.seq = seq
        self.eaters = eaters
        self.callbacks = callbacks
        self.curCallbacks = reversed(self.callbacks)

    def match(self, seq):
        print 'seq:      {}'.format(seq)
        print 'self.seq: {}'.format(self.seq)
        if self.seq.startswith(seq):
            if self.seq == seq:
                return 'Yes'
            else:
                return 'Maybe'
        else:
            return 'No'

    def fire(self):
        while True:
            try:
                next(self.curCallbacks)()
                return
            except StopIteration:
                self.curCallbacks = reversed(self.callbacks)

class TriggerPool:

    def __init__(self):
        self.eventFilters = []
        self.triggers = []
        self.eaters = set()
        self.raw = []
        self.undet = []
        self.det = []

    def addEventFilter(self, eventFilter):
        self.eventFilters.append(eventFilter)

    def addTrigger(self, trigger):
        self.triggers.append(trigger)

    def notify(self, event):
        if all(f(event) for f in self.eventFilters):
            self.notified(event)

    def notified(self, event):
        if str(event) in self.eaters:
            self.eaters.remove(str(event))
            return
        self.raw.append(event)
        for trigger in self.triggers:
            result = trigger.match(''.join(str(e) for e in self.raw))
            print result
            if result == 'Yes':
                trigger.fire()
                self.raw = []
                self.eaters.update(trigger.eaters)
            elif result == 'No':
                self.raw = []
            # elif result == 'Maybe':
            #     pass

        #self.parse(event)
        #self.isp()
        print

    def parse(self, e):

        def takeModifiees(index):
            isHit = lambda key: isinstance(key, Hit)
            modifiees, self.undet[index:] = util.split(self.undet[index:], isHit)
            return modifiees

        if e.down:
            self.undet.append(e)
        else:
            index = self.undet.index(e)
            modifiees = takeModifiees(index + 1)
            self.undet[index] = Hit(e, modifiees)
            if index == 0:
                hit = self.undet[0]
                del self.undet[0]
                self.det.append(hit)

    def isp(self):
        print
