"""The cli"""
import os
import sys
import logging
from argparse import ArgumentParser
from wmc import __version__
from wmc.assemble import Interface


def call(interface, name, **kwargs):
    func = getattr(interface, name)
    func(**kwargs)
    #try:
    #    func(**kwargs)
    #except:
    #    print('Oh no, a error.')


def main():
    """print some help"""
    parser = ArgumentParser(
        description='Watch me coding, a toolbox',
        epilog='Copyright 2019 AxJu | WMCv{}'.format(__version__),
    )
    parser.add_argument(
        'action',  nargs='?', choices=('setup', 'info', 'record', 'size', 'link', 'intro', 'clean'),
        help='Select the action'
    )
    parser.add_argument(
        'path', nargs='?', default=os.getcwd(),
        help='Path to the project'
    )
    parser.add_argument(
        '--verbose', action='store_true',
        help='enable debug infos'
    )
    parser.add_argument(
        '--version', action='store_true',
        help='Print program version and exit'
    )

    args = parser.parse_args()
    if args.version:
        print(__version__)
        sys.exit(0)
    if args.verbose:
        log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        logging.basicConfig(level=logging.DEBUG, format=log_format)

    interface = Interface(args.path, create=args.action == 'setup')
    if args.action == 'setup':
        print('Create new project')
        return 1

    if not args.action:
        parser.print_help()
    else:
        kwargs = {}
        call(interface, args.action, **kwargs)


if __name__ == '__main__':
    main()
