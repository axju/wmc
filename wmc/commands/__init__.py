"""The basic commands"""

__all__ = ['Setup', 'Info', 'Record', 'Link']

import os
from argparse import SUPPRESS, REMAINDER

import ffmpeg
from wmc.utils import BasicCommand
from wmc.dispatch import load_entry_points

from wmc.commands.record import Record


class Setup(BasicCommand):
    """Setup the project"""

    def _create_kwargs(self):
        setup_kwargs = {
            'silent': self.args.silent,
            'rebuild': self.args.rebuild,
        }
        for arg in self.args.args:
            values = arg.split('=')
            setup_kwargs[values[0]] = values[1] if len(values) > 1 else True
        return setup_kwargs

    def setup_parser(self):
        super(Setup, self).setup_parser()
        self.parser.add_argument('-s', '--silent', action='store_true', help='try to run the setup silent')
        self.parser.add_argument('-r', '--rebuild', action='store_true', help='overwrite the data if exists')
        self.parser.add_argument('args', help=SUPPRESS, nargs=REMAINDER)

    def check(self):
        """Check the project"""
        if not self.args.rebuild and os.path.isfile(self.filename):
            raise Exception('There are already a file')

    def main(self, **kwargs):
        super(Setup, self).main()
        setup_kwargs = self._create_kwargs()
        self.logger.debug(
            'Start Setup path="%s", silent="%s", rebuild="%s", kwargs="%s"',
            self.path, self.args.silent, self.args.rebuild, setup_kwargs
        )
        if not os.path.isdir(self.path):
            os.makedirs(self.path)

        entry_points = load_entry_points()
        for cls in entry_points.values():
            cmd = cls(self.path, self.file)
            cmd.create(**setup_kwargs)
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
