"""Some tools"""
import os
import json
import logging
import pkg_resources
import argparse
from types import SimpleNamespace
from wmc import __version__


class BasicCommand():
    """docstring for BasicCommand."""

    __version__=__version__

    def __init__(self, path='.', file='data.jons'):
        self.logger = logging.getLogger(self.__class__.__name__)
        self.path, self.file = os.path.abspath(path), file
        self.filename = os.path.abspath(os.path.join(path, file))
        self.settings = {'name': os.path.basename(path), 'path': self.filename}
        if os.path.isfile(self.filename):
            self.load()

        self.setup()
        self.parser = self.setup_parser()

    def __getitem__(self, key):
        """ ProjectData['info'] """
        return self.settings.get(key)

    def setup_parser(self):
        parser = argparse.ArgumentParser(
            prog='wmc {}'.format(self.__class__.__name__),
            description='Watch me coding, a toolbox',
            epilog='Copyright 2019 AxJu | WMCv{}'.format(__version__),
        )
        parser.add_argument(
            '-V', '--version',
            action='version',
            version='%(prog)s v{}'.format(self.__version__),
        )
        return parser

    def check(self):
        """Check the project"""
        if not os.path.isfile(self.filename):
            raise Exception('No wmc-project')

    def load(self):
        """Load the data from the file"""
        with open(self.filename) as file:
            self.settings = json.load(file)

    def save(self):
        """Save the data to the file"""
        self.logger.info('Save settings (%s)',self.filename)
        with open(self.filename, 'w') as file:
            json.dump(self.settings, file, indent=4, sort_keys=True)

    def run(self, args):
        self.check()
        self.parse_args(args)
        return self.main()

    @property
    def help(self):
        """Return __help__ ot __doc__"""
        doc = getattr(self, '__help__', None)
        if not doc:
            doc = self.__class__.__doc__ or ''
        return doc

    def parse_args(self, args):
        """Setup parser or load some values"""
        self.logger.info('parse_args')
        self.args = self.parser.parse_args(args)

    def setup(self):
        """Setup parser or load some values"""
        self.logger.info('Setup command')

    def create(self, **kwargs):
        """Create the data file"""
        self.logger.info('Create settings')

    def main(self, **kwargs):
        """Run the command"""
        self.logger.info('Run command')
