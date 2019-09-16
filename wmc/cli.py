"""The cli"""
import os
import json
import logging
import argparse
import pkg_resources
from wmc import __version__


class Interface(object):
    """docstring for Inter."""

    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)
        self.setup = {}
        self.command = {}
        for enp in pkg_resources.iter_entry_points(group='wmc.register_setup'):
            self.setup[enp.name] = enp

        for enp in pkg_resources.iter_entry_points(group='wmc.register_command'):
            self.command[enp.name] = enp

    def _setup(self, path, file):
        settings = {}
        settings['path'] = path
        for name, setup in self.setup.items():
            func = setup.load()
            if not func(settings):
                raise Exception('Setup ERROR')

        if not os.path.isdir(path):
            os.mkdir(path)
            self.logger.info('Create "%s"', path)

        filename = os.path.join(path, file)
        with open(filename, 'w') as file:
            json.dump(settings, file, indent=4, sort_keys=True)
            self.logger.info('Save settings "%s"', filename)

    def commands(self):
        return ['setup'] + list(self.command.keys())

    def run(self, cmd, path, file, args):
        self.logger.info('Start cmd="%s", path="%s", file="%s", args="%s"', cmd, path, file, args)
        if cmd == 'setup':
            return self._setup(path, file)

        elif cmd in self.command:
            with open(os.path.join(path, file)) as file:
                settings = json.load(file)

            func = self.command[cmd].load()
            return func(settings, args)


def dispatch(argv):
    interface = Interface()

    parser = argparse.ArgumentParser(
        prog='wmc',
        description='Watch me coding, a toolbox',
        epilog='Copyright 2019 AxJu | WMCv{}'.format(__version__),
    )
    parser.add_argument(
        '-V','--version',
        action='version',
        version='%(prog)s version {}'.format(__version__),
    )
    parser.add_argument(
        '-v', '--verbose', action='store_true',
        help='Enable debug infos'
    )
    parser.add_argument(
        '-s', '--settings', default='data.json',
        help='The settings file'
    )
    parser.add_argument(
        'command',
        choices=interface.commands(),
    )
    parser.add_argument(
        'path', nargs='?', default=os.getcwd(),
        help='Path to the project'
    )
    parser.add_argument(
        'args',
        help=argparse.SUPPRESS,
        nargs=argparse.REMAINDER,
    )
    args = parser.parse_args(argv)

    if args.verbose:
        log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        logging.basicConfig(level=logging.DEBUG, format=log_format)

    return interface.run(args.command, args.path, args.settings, args.args)
