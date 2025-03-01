import datetime

import win32clipboard
from PIL import ImageGrab

from logger import logger


KNOWN_FORMAT_SPECS = [
    {'format': win32clipboard.CF_UNICODETEXT, 'type': 'text'},
    {'format': win32clipboard.CF_BITMAP, 'type': 'image', 'data': False},
    {'format': win32clipboard.CF_DIB, 'type': 'image', 'data': False},
    {'format': win32clipboard.CF_DIBV5, 'type': 'image', 'data': False},
]
FORMAT_TO_SPEC = {d['format']: d for d in KNOWN_FORMAT_SPECS}
KNOWN_FORMATS = set([d['format'] for d in KNOWN_FORMAT_SPECS])


class Clipboard:

    def __enter__(self):
        win32clipboard.OpenClipboard()
        return self

    def __exit__(self, *_, **__):
        win32clipboard.CloseClipboard()

    @property
    def formats(self):
        fmt = 0
        while True:
            fmt = win32clipboard.EnumClipboardFormats(fmt)
            if not fmt:
                break
            yield fmt

    @property
    def format_names(self):
        for fmt in self.formats:
            yield win32clipboard.GetClipboardFormatName(fmt)

    @property
    def data(self):
        unknown_formats = []
        for fmt in self.formats:
            if fmt in KNOWN_FORMATS:
                ret = {
                    'type': FORMAT_TO_SPEC[fmt]['type'],
                }
                spec = FORMAT_TO_SPEC[fmt]
                if spec.get('data') is None:
                    ret['data'] = self.get_data(fmt),
                return ret
            unknown_formats.append(fmt)
        for fmt in unknown_formats:
            print(fmt_to_name[fmt])
        return None

    def get_data(self, fmt):
        #return win32clipboard.GetClipboardData(win32clipboard.CF_DIB)
        return win32clipboard.GetClipboardData(fmt)

    @staticmethod
    def get_image():
        logger.info('Clipboard()')
        with Clipboard() as clip:
            data = clip.data
        logger.info('data')
        if data:
            if data['type'] == 'text':
                pass
            elif data['type'] == 'image':
                img = ImageGrab.grabclipboard()
                now = datetime.datetime.now()
                fname = now.strftime('%Y-%m-%d_%H-%M-%S_%f.png')
                path = 'D:\\\\.fme\\data\\files\img\\' + fname
                img.save(path)
                return '`eno.img /f/img/' + fname + '`'
