"""The cli"""
import os
import logging
from argparse import ArgumentParser
from wmc import __version__
from wmc.assemble import Interface


def main():
    """print some help"""
    parser = ArgumentParser(
        description='Watch me coding, a toolbox',
        epilog='Copyright 2019 AxJu | WMCv{}'.format(__version__),
    )
    parser.add_argument(
        'action',  nargs='?', help='Select the action',
        choices=(
            'setup', 'info', 'record', 'size', 'link', 'intro',
            'censor', 'censorvideos', 'censortemplates'
        ),
    )
    parser.add_argument(
        'path', nargs='?', default=os.getcwd(),
        help='Path to the project'
    )
    parser.add_argument(
        '-v', '--verbose', action='store_true',
        help='enable debug infos'
    )
    parser.add_argument(
        '-V', '--version', action='store_true',
        help='Print program version and exit'
    )

    args = parser.parse_args()
    if args.version:
        print(__version__)
        return 1

    if args.verbose:
        log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        logging.basicConfig(level=logging.DEBUG, format=log_format)

    try:
        interface = Interface(args.path, create=args.action == 'setup')
        if args.action == 'setup':
            print('Create new project')
            return 1

        if not args.action:
            parser.print_help()
        else:
            kwargs = {}
            getattr(interface, args.action)(**kwargs)

    except Exception as e:
        if args.verbose:
            raise e
        else:
            print('Oh no, a error.')
    return 1


if __name__ == '__main__':
    main()
