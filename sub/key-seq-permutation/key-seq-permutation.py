import sys
import string
from itertools import permutations
from collections import Counter, deque

ident = lambda e: e

def extract(l, pred=ident, key=ident):
    return (e for e in l if pred(key(e)))

def split(l, pred):
    a = []
    b = []
    for e in l:
        if pred(e):
            a.append(e)
        else:
            b.append(e)
    return a, b

def extractDowns(seq, key=ident):
    return extract(seq, lambda c: c.islower(), key)

def extractUps(seq, key=ident):
    return extract(seq, lambda c: c.isupper(), key)

def valid(seq, downs):
    if list(downs) != list(extractDowns(seq)):
        return False
    for down in downs:
        up = down.upper()
        if seq.index(up) < seq.index(down):
            return False
    return True

def sequence(downs):
    ups = downs.upper()
    seq = (ch for t in zip(downs, ups) for ch in t)
    return seq

def validSeqs(keys, valid=valid):
    downs = keys.lower()
    perm = permutations(sequence(downs))
    seqs = (''.join(p) for p in perm if valid(p, downs))
    return seqs

def segmentGraph(seq):

    def line(beg, down):
        end = seq.index(down.upper())
        padding = ' ' * beg
        segment = down + '_' * (end - beg - 1) + down
        return padding + segment

    downs = extractDowns(enumerate(seq), lambda e: e[1])
    lines = [line(*d) for d in downs]
    return '\n'.join(lines)

def parse(seq):

    class Hit:
        """
        A Hit is a key press/release pair which may contains other hits
        as its modifiees.
        For example, in 'abBA' -> 'a(b)', 'a' is a hit and '(b)' is it's
        modifiees, which means press b(modifiee) while holding a(modifier).
        """

        def __init__(self, key, modifiees):
            self.key = key
            self.modifiees = modifiees

        def __repr__(self):
            if self.modifiees:
                modifiees = ''.join(str(key) for key in self.modifiees)
                return '{}({})'.format(self.key, modifiees)
            else:
                return self.key

    def getModifiees(a, index):
        modifiees, a[index:] = split(a[index:], lambda key: isinstance(key, Hit))
        return modifiees

    # undet store the partial key sequence which's meaning is undetermined
    # det store the partial key sequence which's meaning is determined
    # 
    # Fetch one key press/release at a time:
    # - If it's a press, just put into the undet queue;
    # - It it's a release, we take (remove from undet) every finished hit
    #   between this hit as its modifiees, and replace the previous key
    #   press with this key hit.
    #   If this hit is at the begining of the undet queue, then we'll be sure
    #   that no other key could modify it. So we take it from undet and put
    #   into det.
    undet = []
    det = []
    for c in seq:
        if c.islower():
            undet.append(c)
        else:
            down = c.lower()
            index = undet.index(down)
            modifiees = getModifiees(undet, index + 1)
            undet[index] = Hit(down, modifiees)
            if index == 0:
                key = undet[0]
                del undet[0]
                det.append(key)
    return ''.join(str(key) for key in det)

def printParse(keys):
    seqs = list(validSeqs(keys))
    for i, seq in enumerate(seqs):
        print '{} -> {}'.format(seq, parse(seq))
        print segmentGraph(seq)
        print

#for i in range(5):
#    keys = string.letters[:i + 1]
#    sys.stdout = open(keys + '.txt', 'w')
#    printParse(keys)

printParse('abc')
