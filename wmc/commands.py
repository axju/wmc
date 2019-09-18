"""The basic commands"""
import os
import sys
from datetime import datetime
from time import sleep

import ffmpeg
from wmc.utils import BasicCommand
from wmc.dispatch import load_entry_points


class Setup(BasicCommand):
    """Setup the project"""

    __help__ = 'Some help'

    def check(self):
        """Check the project"""
        if os.path.isfile(self.filename):
            raise Exception('There are already a file')

    def main(self, **kwargs):
        super(Setup, self).main()
        self.logger.info('Start Setup path="%s"', self.path)
        if not os.path.isdir(self.path):
            os.makedirs(self.path)

        entry_points = load_entry_points()
        for cls in entry_points.values():
            cmd = cls(self.path, self.file)
            cmd.create()
            cmd.save()


class Info(BasicCommand):
    """Print some infos"""

    def main(self, **kwargs):
        """Print som infos"""
        super(Info, self).main()
        print(self.settings)


class Record(BasicCommand):
    """Start the record"""

    DATA = {
        'win': {
            "input": {
                "filename": "desktop",
                "f": "gdigrab",
                "framerate": 1,
                "video_size": (1920, 1080),
                "offset_x": -1920,
                "show_region": 1,
            },
            "output": {
                "vcodec": "libx264",
                "preset": "ultrafast",
                "r": 30,
            },
            "setpts": "N/TB/30",
        },
        'linux': {
            "input": {
                "filename": ":0.0+0,0",
                "f": "x11grab",
                "framerate": 1,
                "video_size": (1920, 1080),
            },
            "output": {
                "vcodec": "libx264",
                "preset": "ultrafast",
                "r": 30,
            },
            "setpts": "N/TB/30",
        }
    }

    def setup_parser(self):
        parser = super(Record, self).setup_parser()
        parser.add_argument('-t', '--time', type=int, help='set a fix time to run')
        parser.add_argument('-s', '--show', action='store_false', help='show ffmpeg output')
        return parser

    def create(self, **kwargs):
        """Create the basic settings"""
        super(Record, self).create()
        platform = 'None'
        if sys.platform.startswith('win'):
            platform = 'win'
        elif sys.platform.startswith('linux'):
            platform = 'linux'
        self.settings['record'] = self.DATA.get(platform, {})

    def main(self, **kwargs):
        """Start the record"""
        super(Record, self).create()
        now = datetime.now().strftime('%Y%m%d%H%M.mp4')
        filename = os.path.join(self.settings['path'], 'video_' + now)
        settings = self.settings['record']
        stream = ffmpeg.input(**settings['input']).setpts(settings['setpts'])
        stream = ffmpeg.output(stream, filename, **settings['output'])
        process = ffmpeg.run_async(
            stream,
            pipe_stdin=True,
            pipe_stdout=True,
            pipe_stderr=self.args.show,
            overwrite_output=True,
        )
        try:
            if self.args.time:
                self.logger.info('record the screen for %i sec', self.args.time)
                for _ in range(self.args.time):
                    sleep(1)
            else:
                input('press enter to finish ')
        except KeyboardInterrupt:
            self.logger.info('breack with KeyboardInterrupt')

        finally:
            self.logger.info('save file')
            process.communicate(input=b"q")


class Link(BasicCommand):
    """Concat allvideos to one"""

    def setup_parser(self):
        parser = super(Link, self).setup_parser()
        parser.add_argument('-s', '--show', action='store_false', help='show ffmpeg output')
        return parser

    def main(self, **kwargs):
        """concat all videos to one"""
        super(Link, self).create()
        records = []
        for rec in os.listdir(self.settings['path']):
            if rec.startswith('video_'):
                records.append(os.path.join(self.settings['path'], rec))
        if not records:
            return
        records.sort()
        stream = ffmpeg.input(records[0])
        for video in records[1:]:
            stream = stream.concat(ffmpeg.input(video))
        stream = ffmpeg.output(stream, os.path.join(self.settings['path'], 'full.mp4'))
        ffmpeg.run(stream, overwrite_output=True, quiet=self.args.show)
