"""The basic commands"""

__all__ = ['Setup', 'Info', 'Record', 'Link']

import os

import ffmpeg
from wmc.utils import BasicCommand
from wmc.dispatch import load_entry_points

from wmc.commands.record import Record


class Setup(BasicCommand):
    """Setup the project"""

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


class Link(BasicCommand):
    """Concat all videos to one"""

    def setup_parser(self):
        super(Link, self).setup_parser()
        self.parser.add_argument('-s', '--show', action='store_false', help='show ffmpeg output')

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
