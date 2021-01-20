"""Some tools"""
import os
import json
import logging
import argparse
from wmc import __version__


class BasicCommand():
    """The BasicCommand"""

    __version__ = __version__

    def __init__(self, path='.', file='data.json'):
        self.logger = logging.getLogger(self.__class__.__name__)
        self.path, self.file = os.path.abspath(path), file
        self.filename = os.path.abspath(os.path.join(path, file))
        self.settings = {'name': os.path.basename(self.path), 'path': self.path}
        if os.path.isfile(self.filename):
            self.load()

        self.args = None
        self.setup()
        self.setup_parser()

    def __getitem__(self, key):
        return self.settings.get(key)

    def __contains__(self, key):
        return key in self.settings

    def setup_parser(self):
        """Create basic parser"""
        self.parser = argparse.ArgumentParser(
            prog='wmc {}'.format(self.__class__.__name__),
            description='Watch me coding, a toolbox',
            epilog='Copyright 2021 AxJu | WMCv{}'.format(__version__),
        )
        self.parser.add_argument(
            '-V', '--version',
            action='version',
            version='%(prog)s v{}'.format(self.__version__),
        )

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
        self.logger.info('Save settings (%s)', self.filename)
        with open(self.filename, 'w') as file:
            json.dump(self.settings, file, indent=4, sort_keys=True)

    def run(self, args):
        """execute the command"""
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

    def parse_args(self, argv):
        """Setup parser or load some values"""
        self.logger.info('parse_args')
        self.args = self.parser.parse_args(argv)

    def setup(self):
        """Setup parser or load some values"""
        self.logger.info('Setup command')

    def create(self, **kwargs):
        """Create the data file"""
        self.logger.info('Create settings')

    def main(self, **kwargs):
        """Run the command"""
        self.logger.info('Run command')
