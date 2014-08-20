from itertools import permutations
from collections import Counter

def extract(seq, pred):
    return ''.join(key for key in seq if pred(key))

def extractDowns(seq):
    return extract(seq, lambda key: key.islower())

def extractUps(seq):
    return extract(seq, lambda key: key.isupper())

def valid(downs, seq):
    if downs != extractDowns(seq):
        return False
    for down in downs:
        up = down.upper()
        if seq.index(up) < seq.index(down):
            return False
    return True

def validSeqs(keys, valid=valid):
    downs = keys.lower()
    ups = downs.upper()
    seq = ''.join(ch for t in zip(downs, ups) for ch in t)
    seqs = (''.join(p) for p in permutations(seq) if valid(downs, p))
    return seqs

def countInversions(seq):
    n = 0
    for i in range(len(seq)):
        for j in range(i):
            if seq[i] < seq[j]:
                n += 1
    return n

def toNumSeq(seq, keys=None):
    if not keys:
        keys = extractDowns(seq)
    nseq = []
    for key in seq:
        index = keys.index(key.lower())
        if key.islower():
            index = 2 * index + 1
        else:
            index = 2 * index + 2
        nseq.append(index)
    return nseq

def numSeq2str(seq):
    return ''.join(str(n) for n in seq)

keys = 'abc'

seqs = list(validSeqs(keys))
nSeqInvs = [countInversions(seq.lower()) for seq in seqs]
numSeqs = [numSeq2str(toNumSeq(seq, keys)) for seq in seqs]
nNumSeqInvs = [countInversions(seq) for seq in numSeqs]

for args in zip(seqs, nSeqInvs, numSeqs, nNumSeqInvs):
    print '{} {:2} {} {:2}'.format(*args)
print len(seqs)
cntNumSeqInvs = dict(Counter(nNumSeqInvs))
print cntNumSeqInvs.values(), len(cntNumSeqInvs)
