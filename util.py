def _super(cls):
    setattr(cls, '_super', lambda self: super(cls, self))
    return cls

def split(l, pred):
    a = []
    b = []
    for e in l:
        if pred(e):
            a.append(e)
        else:
            b.append(e)
    return a, b
