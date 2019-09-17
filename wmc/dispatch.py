"""Load all entry poins"""
import os
import sys
import json
import logging
import argparse
import pkg_resources
from wmc import __version__
from wmc.utils import BasicCommand

def get_basic_call():
    """get all functions from the basic class"""
    for name in dir(BasicCommand):
        if not name.startswith('_') and callable(getattr(BasicCommand, name)):
            yield name


def load_entry_points():
    """Load the classes and create new for only functions entry points"""
    command = {}
    for enp in pkg_resources.iter_entry_points(group='wmc.register_cls'):
        cls = enp.load()
        command[enp.name] = cls
        command[enp.name].__name__ = enp.name

    for name in get_basic_call():
        for enp in pkg_resources.iter_entry_points(group='wmc.register_{}'.format(name)):
            func = enp.load()
            if enp.name in command:
                setattr(command[enp.name], name, func)
            else:
                command[enp.name] = type(enp.name, (BasicCommand, ), {name: func, '__name__': enp.name})
    return command


def help_commands():
    """Print the command help."""
    commands = load_entry_points()
    for name, cls in commands.items():
        cmd = cls()
        text = '{:>8} v{:.5} - {}'.format(cmd.__class__.__name__, cmd.__version__, cmd.help)
        print(text)


def main(argv=sys.argv[1:]):
    """Create parser und run the dispatch"""
    commands = load_entry_points()
    parser = argparse.ArgumentParser(
        prog='wmc',
        description='Watch me coding, a toolbox',
        epilog='Copyright 2019 AxJu | WMCv{}'.format(__version__),
    )
    parser.add_argument(
        '-V', '--version',
        action='version',
        version='%(prog)s v{}'.format(__version__),
    )
    parser.add_argument(
        '-v', '--verbose', action='store_true',
        help='Enable debug infos.'
    )
    parser.add_argument(
        '-s', '--settings', default='data.json',
        help='The settings file.'
    )
    parser.add_argument(
        '-H', '--help-commands', action='store_true',
        help='Some command infos.'
    )
    parser.add_argument(
        'command',  nargs='?', choices=commands.keys(),
        help='Select one command.'
    )
    parser.add_argument(
        'path', nargs='?', default=os.getcwd(),
        help='Path to the project.'
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

    if args.help_commands:
        return help_commands()

    if args.command:
        cmd = commands[args.command](args.path, args.settings)
        try:
            return cmd.run(args.args)
        except Exception as e:
            if args.verbose:
                raise
            else:
                print('Oh no, a error :(')
                print('Error:', e)
                print('Run with --verbose for more information.')
                return 0

    return parser.print_help()
