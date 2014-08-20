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

    class Key:

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
        modifiees, a[index:] = split(a[index:], lambda key: isinstance(key, Key))
        return modifiees

    def isp():
        print 'q:    {}'.format(q)
        print 'keys: {}'.format(keys)
        print

    q = []
    keys = []
    for c in seq:
        if c.islower():
            #print '{} down'.format(c)
            q.append(c)
            #isp()
        else:
            #print '{} up'.format(c)
            down = c.lower()
            index = q.index(down)
            modifiees = getModifiees(q, index + 1)
            q[index] = Key(down, modifiees)
            if index == 0:
                key = q[0]
                del q[0]
                keys.append(key)
                #isp()
                #continue
            #isp()
    return ''.join(str(key) for key in keys)

def printParse(keys):
    seqs = list(validSeqs(keys))
    for i, seq in enumerate(seqs):
        #if not (0 <= i):
        #    continue
        #print i
        #print seq
        print '{} -> {}'.format(seq, parse(seq))
        print segmentGraph(seq)
        print

#for i in range(5):
#    keys = string.letters[:i + 1]
#    sys.stdout = open(keys + '.txt', 'w')
#    printParse(keys)

printParse('abc')
