"""Load all entry poins"""
import os
import sys
import logging
import argparse
from wmc import __version__
from wmc.dispatch import load_entry_points


def help_commands():
    """Print the command help."""
    commands = load_entry_points()
    for name, cls in commands.items():
        cmd = cls()
        text = '{:>8} v{:.5} - {}'.format(cmd.__class__.__name__, cmd.__version__, cmd.help)
        print(text)


def create_parse(commands):
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
        'command',  nargs='?', choices=commands,
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
    return parser


def main(argv=sys.argv[1:]):
    """Create parser und run the dispatch"""
    commands = load_entry_points()
    parser = create_parse(commands.keys())
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
