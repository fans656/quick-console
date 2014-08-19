class Event:

    ATTR_NAMES = (
            'down',
            #'up',
            #'time',
            'id',
            'autorepeat',
            )

    def __init__(self, **kwas):
        self.__dict__.update({name: None for name in Event.ATTR_NAMES})
        self.__dict__.update(kwas)

    def __repr__(self):
        d = {name: getattr(self, name) for name in Event.ATTR_NAMES}
        return str(d)

class Sequence(unicode):

    @staticmethod
    def normalized(seq):
        return seq.lower()

    def __new__(cls, seq):
        seq = cls.normalized(seq)
        return unicode.__new__(cls, seq)

class TrigerPool:

    def add(self, seq, callback):
        pass

    def notify(self, event):
        print event
