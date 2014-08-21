class Event:

    @staticmethod
    def normalizedName(name):
        name = name.lower()
        if len(name) > 1:
            name = '<{}>'.format(name)
        return name

    def __init__(self,
            name='invalid',
            keyid=999,
            down=True,
            autorepeat=False):
        self.name = name
        self.keyid = keyid
        self.down = down
        self.up = not down
        self.autorepeat = autorepeat
        self.normalize()

    def normalize(self):
        self.name = Event.normalizedName(self.name)

    def __repr__(self):
        if self.down:
            return self.name
        else:
            return self.name + '^'
