import os
import setuptools

def setup(cmd):
    cmd.__version__ = '0.1.0'
    cmd.__help__ = 'A Plugin with a function'

def main(cmd, **kwargs):
    print('Hello, have a nice day :)')

if __name__ == '__main__':
    os.chdir(os.path.dirname(__file__))
    setuptools.setup(
        name='wmc-plugin-func',
        version='0.1.0',
        py_modules=['plugin_func'],
        entry_points={
            'wmc.register_setup': [
                'plugin-func=plugin_func:setup',
            ],
            'wmc.register_main': [
                'plugin-func=plugin_func:main',
            ],
        }
    )
