import os
import random
import subprocess

paths = [
        "E:\Music",
        ]
exts = [
    'mp3',
]

def is_music(f):
    return any(f.endswith(ext) for ext in exts)

musics = []
for path in paths:
    files = os.walk(path)
    for dirpath, dirnames, filenames in files:
        musics += [os.path.join(dirpath, f)
                for f in filenames if is_music(f)]
music = random.choice(musics)
kmp = r"C:\Program Files\DAUM\PotPlayer\PotPlayerMini64.exe"
subprocess.Popen([kmp, music])
