"""The basic commands"""
import os
import sys
from datetime import datetime
from time import sleep

import ffmpeg
from wmc.utils import BasicCommand


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
                "pix_fmt": "yuv420p",
            },
            "setpts": "N/TB/30",
        },
        'linux': {
            "input": {
                "filename": ":1",
                "f": "x11grab",
                "framerate": 1,
                "video_size": (1920, 1080),
            },
            "output": {
                "vcodec": "libx264",
                "preset": "ultrafast",
                "r": 30,
                "pix_fmt": "yuv420p",
            },
            "setpts": "N/TB/30",
        }
    }

    def setup_parser(self):
        super(Record, self).setup_parser()
        self.parser.add_argument('-t', '--time', type=int, help='set a fix time to run')
        self.parser.add_argument('-s', '--show', action='store_false', help='show ffmpeg output')

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
