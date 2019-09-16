import os
import sys
from setuptools import setup, find_packages
from setuptools.command.develop import develop
from setuptools.command.install import install
from subprocess import check_call


base_dir = os.path.dirname(__file__)

with open(os.path.join(base_dir, 'README.rst')) as readme:
    README = readme.read()

requirements = []
if sys.platform.startswith('win'):
    requirements.append()
elif sys.platform.startswith('linux'):
    requirements.append('Xlib')

setup(
    packages=find_packages(exclude=['tests']),
    include_package_data=True,
    use_scm_version=True,
    install_requires=[
        'ffmpeg-python',
        'pywin32 ; platform_system=="Windows"',
        'Xlib ; platform_system=="Linux"'
    ],
    setup_requires=[
        'setuptools_scm',
    ],
    entry_points={
        'wmc.register_setup':[
            'basic=wmc.basic:setup',
        ],
        'wmc.register_command':[
            'info=wmc.basic:info',
            'record=wmc.basic:record',
            'link=wmc.basic:link',
        ],
        'console_scripts': [
            'wmc=wmc.cli:main',
        ],

    },
)
