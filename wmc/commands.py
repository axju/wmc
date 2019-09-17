"""The basic commands"""
import os
import ffmpeg
from datetime import datetime
from types import SimpleNamespace
from wmc.utils import BasicCommand
from wmc.dispatch import load_entry_points


class Setup(BasicCommand):
    """Setup the project"""

    __help__ = 'Some help'

    def check(self):
        """Check the project"""
        if os.path.isfile(self.filename):
            raise Exception('There are already a file')

    def main(self):
        super(Setup, self).main()
        self.logger.info('Start Setup path="%s"', self.path)
        if not os.path.isdir(self.path):
            os.makedirs(self.path)

        entry_points = load_entry_points()
        for name, cls in entry_points.items():
            cmd = cls(self.path, self.file)
            cmd.create()
            cmd.save()


class Info(BasicCommand):
    """Print some infos"""

    def main(self):
        """Print som infos"""
        super(Info, self).main()
        print(self.settings)


class Record(BasicCommand):
    """Start the record"""

    def create(self):
        """Create the basic settings"""
        super(Record, self).create()
        self.settings['record'] = {
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

    def main(self):
        """Start the record"""
        super(Record, self).create()
        now = datetime.now().strftime('%Y%m%d%H%M.mp4')
        filename = os.path.join(self.settings['path'], 'video_' + now)
        settings = self.settings['record']
        stream = ffmpeg.input(**settings['input']).setpts(settings['setpts'])
        stream = ffmpeg.output(stream, filename, **settings['output'])
        ffmpeg.run(stream, overwrite_output=True)


class Link(BasicCommand):
    """Concat allvideos to one"""

    def main(self):
        """concat all videos to one"""
        super(Link, self).create()
        records = []
        for rec in os.listdir(self.settings['path']):
            if rec.startswith('video_'):
                records.append(os.path.join(self.settings['path'], rec))
        stream = ffmpeg.input(records[0])
        for video in records[1:]:
            stream = stream.concat(ffmpeg.input(video))
        stream = ffmpeg.output(stream, os.path.join(self.settings['path'], 'full.mp4'))
        ffmpeg.run(stream, overwrite_output=True)
