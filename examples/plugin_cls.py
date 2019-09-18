import os
import setuptools
from wmc.utils import BasicCommand


class Plugin(BasicCommand):
    """A Plugin with a the basic class"""
    __version__ = '0.1.0'

    def setup_parser(self):
        super(Plugin, self).setup_parser()
        self.parser.add_argument('--hello', action='store_true', help='say hello')

    def main(self, **kwargs):
        super(Plugin, self).main()
        if self.args.hello:
            print('Hello, have a nice day :)')
        else:
            print('Bye bey ;)')


if __name__ == '__main__':
    os.chdir(os.path.dirname(__file__))
    setuptools.setup(
        name='wmc-plugin-cls',
        version='0.1.0',
        py_modules=['plugin_cls'],
        entry_points={
            'wmc.register_cls': [
                'plugin-cls=plugin_cls:Plugin',
            ],
        }
    )
