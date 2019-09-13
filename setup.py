import os
import sys
from setuptools import setup, find_packages
from setuptools.command.develop import develop
from setuptools.command.install import install
from subprocess import check_call


class CheckFfmpegDevelop(develop):
    """Post-installation for development mode."""
    def run(self):
        check_call("ffmpeg -version".split())
        develop.run(self)


class CheckFfmpegInstall(install):
    """Post-installation for installation mode."""
    def run(self):
        check_call("ffmpeg -version".split())
        install.run(self)


base_dir = os.path.dirname(__file__)

with open(os.path.join(base_dir, 'README.rst')) as readme:
    README = readme.read()

requirements = ['lying==0.0.1a1', 'ffmpeg-python', 'opencv-python', 'numpy']
if sys.platform.startswith('win'):
    requirements.append('pywin32')
elif sys.platform.startswith('linux'):
    requirements.append('Xlib')

setup(
    name='wmc',
    description='Watch me coding, a toolbox',
    url='https://github.com/axju/wmc',
    author='Axel Juraske',
    author_email='axel.juraske@short-report.de',
    license='MIT',
    long_description=README,
    classifiers=[
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],

    packages=find_packages(exclude=['tests']),
    include_package_data=True,
    use_scm_version=True,
    install_requires=requirements,
    setup_requires=[
        'setuptools_scm',
    ],
    entry_points={
        'console_scripts': [
            'wmc=wmc.cli:main',
        ]
    },

    cmdclass={
        'develop': CheckFfmpegDevelop,
        'install': CheckFfmpegInstall,
    },
)
