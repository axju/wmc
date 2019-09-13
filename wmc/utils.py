"""Some useful tools"""
import os
import sys
import logging
import ffmpeg
import cv2
import numpy as np
from time import sleep
from tempfile import mkdtemp
from shutil import rmtree, copyfile


def resize_window(size, wait=1):
    """Resize the current window"""
    sleep(wait)
    if sys.platform in ["win32", "win64"]:
        import win32gui
        hwnd = win32gui.GetForegroundWindow()
        win32gui.MoveWindow(hwnd, *size, True)

    elif sys.platform in ["linux", "linux2"]:
        import Xlib
        import Xlib.display
        display = Xlib.display.Display()
        root = display.screen().root
        wid = root.get_full_property(
            display.intern_atom("_NET_ACTIVE_WINDOW"),
            Xlib.X.AnyPropertyType,
        ).value[0]
        window = display.create_resource_object("window", wid)
        window.configure(
            x=size[0], y=size[1], width=size[2], height=size[3]
        )
        display.sync()


class BasicKeys():
    """docstring for BasicKeys."""

    KEYS = []

    def __contains__(self, key):
        if key in self.KEYS:
            return True
        return False


class Censorship():
    """docstring for Censorship."""

    def __init__(self, videofile, templates, filename, **kwargs):
        self.logger = logging.getLogger(self.__class__.__name__)
        self.dirs = {
            'frames': None,
            'templates': None,
            'cleaned': None,
        }
        self.videofile = videofile
        self.templates = templates
        self.filename = filename
        self.threshold = kwargs.get('threshold', 0.5)
        self.multi = kwargs.get('multi', True)
        self.tmpdir = kwargs.get('dir', mkdtemp())

    def setup(self, dir=None):
        """create the dirs"""
        self.tmpdir = mkdtemp()
        self.logger.info('Create tmp dir "{}"'.format(self.tmpdir))
        for name in self.dirs:
            self.dirs[name] = os.path.join(self.tmpdir, name)
            if not os.path.exists(self.dirs[name]):
                os.makedirs(self.dirs[name])
                self.logger.info('Create tmp dir "{}"'.format(self.dirs[name]))

    def cleanup(self):
        """delete the tmp dir"""
        rmtree(self.tmpdir)
        self.logger.info('delete tmp dir "{}"'.format(self.tmpdir))

    def get_files(self, kind):
        return sorted([os.path.join(self.dirs[kind], fn) for fn in os.listdir(self.dirs[kind])])

    def create_frames(self):
        stream = ffmpeg.input(self.videofile)
        stream = ffmpeg.output(stream, os.path.join(self.dirs['frames'], '%06d.png'))
        ffmpeg.run(stream, overwrite_output=True, quiet=True)

    def create_templates(self):
        for i, data in enumerate(self.templates):
            filename = os.path.join(self.dirs['templates'], '{}.png'.format(i))
            font = data.get('font', cv2.FONT_HERSHEY_SIMPLEX)
            template = np.zeros((*data['size'], 3), np.uint8)
            cv2.imwrite(filename, template)
            template = cv2.imread(filename, 0)
            template = cv2.putText(template, data['text'], tuple(data['pos']), font, data['scale'], (255, 255, 255), 1)
            cv2.imwrite(filename, template)

    def check_frame(self, frame):
        result = []
        img = cv2.imread(frame, 0)
        ret, edges = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)

        for filename in self.get_files('templates'):
            template = cv2.imread(filename, 0)
            w, h = template.shape[::-1]
            res = cv2.matchTemplate(edges, template, cv2.TM_CCORR_NORMED)

            if self.multi:
                loc = np.where(res >= self.threshold)
                for pt in zip(*loc[::-1]):
                    result.append((pt, (pt[0] + w, pt[1] + h)))

            else:
                _, max_val, _, max_loc = cv2.minMaxLoc(res)
                if max_val > self.threshold:
                    result.append((max_loc, (max_loc[0] + w, max_loc[1] + h)))

        return result

    def blur_frame(self, frame, areas):
        self.logger.debug('blur frame {}'.format(os.path.basename(frame)))
        img = cv2.imread(frame, 3)
        blurred_img = cv2.GaussianBlur(img, (15, 15), 3)
        mask = np.zeros(img.shape, dtype=np.uint8)
        for pt in areas:
            cv2.rectangle(mask, pt[0], pt[1], (255, 255, 255), -1)
        out = np.where(mask != (255, 255, 255), img, blurred_img)
        cleaned = os.path.join(self.dirs['cleaned'], os.path.basename(frame))
        cv2.imwrite(cleaned, out)

    def save(self):
        stream = ffmpeg.input(os.path.join(self.dirs['cleaned'], '%06d.png'))
        stream = ffmpeg.output(stream, self.filename)
        ffmpeg.run(stream, overwrite_output=True, quiet=True)

    def run(self):
        self.setup()
        self.create_frames()
        self.create_templates()
        for frame in self.get_files('frames'):
            areas = self.check_frame(frame)
            if areas:
                self.blur_frame(frame, areas)
            else:
                copyfile(frame, os.path.join(self.dirs['cleaned'], os.path.basename(frame)))
        self.save()
        self.cleanup()
