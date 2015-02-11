import os
import random
import subprocess

paths = [
        "E:\Movies\AV",
        "D:\AV",
        ]
exts = [
    'mpg', 'vob', '3gp', 'wmv', 'flv', 'mkv',
    'mp4', 'rmvb', 'avi', 'm2ts', 'rm'
]

def is_movie(f):
    return any(f.endswith(ext) for ext in exts)

movies = []
for path in paths:
    files = os.walk(path)
    for dirpath, dirnames, filenames in files:
        movies += [os.path.join(dirpath, f)
                for f in filenames if is_movie(f)]
movie = random.choice(movies)
kmp = r"D:\Media\KMP\KMPlayer.exe"
subprocess.Popen([kmp, movie])
