===============
Watch me coding
===============
.. image:: https://img.shields.io/pypi/v/wmc
   :alt: PyPI
   :target: https://pypi.org/project/wmc/

.. image:: https://img.shields.io/pypi/pyversions/wmc
   :alt: Python Version
   :target: https://pypi.org/project/wmc/

.. image:: https://img.shields.io/pypi/l/wmc
   :alt: License
   :target: https://pypi.org/project/wmc/

Create some screen recording. I would like to share my coding process. This
small tool should help me. But you can use it for any long time recording.

It's still under develop, but you can try it. See "How does it work" for more
information

Install
-------
It is on PyPi::

  pip install wmc

Hot to uses
-----------
Create a new project. This is basically a folder with a settings file::

  wmc setup .
  wmc setup test

You can edit the config file or simple start recording::

  wmc record

Use the help for more::

  >>> wmc --help
  usage: wmc [-h] [-V] [-v] [-s SETTINGS] [-H] [{info,link,record,setup}] [path]

  Watch me coding, a toolbox

  positional arguments:
    {info,link,record,setup}
                          Select one command.
    path                  Path to the project.


  optional arguments:
    -h, --help            show this help message and exit
    -V, --version         show program's version number and exit
    -v, --verbose         Enable debug infos.
    -s SETTINGS, --settings SETTINGS
                          The settings file.
    -H, --help-commands   Some command infos.

  Copyright 2019 AxJu | WMCv0.3.2

Every sub command could have some different options. But you can look into there
help, too::

  >>> wmc info dummy -h
  usage: wmc info [-h] [-V]

  Watch me coding, a toolbox

  optional arguments:
    -h, --help     show this help message and exit
    -V, --version  show program's version number and exit

  Copyright 2019 AxJu | WMCv0.3.2

How does it work
----------------
The workplace is simple folder with a data file. Every command work with this
folder and the settings from the data file. To manage the different commands I
create a basic class and uses the entry_points from the setuptools. This make
it also easy to write custom commands. Write your own pypackage, integrate your
command to the entry_points and the command is variable. To create the command
you can inherit from the basic class and then override the functions. To take
your dependency small and clean, you can overwrite single functions from the
basic class.

It is simple as usual in python. I put some examples in the example folder, a
class and an function example. Look into the folder, if you want to create
your own command. I will explain how you can use this.

1. Clone the repo or download the files.::

     git clone https://github.com/axju/wmc.git

2. Install wmc.
   You should always use a virtual environment, but that's not my business. If
   you would install wmc from source::

     python setup.py install

   or from PyPi::

    pip install wmc

3. Take a look to the default commands::

    >>> wmc -H
        info v0.3.2 - Print some infos
        link v0.3.2 - Concat all videos to one
      record v0.3.2 - Start the record
       setup v0.3.2 - Some help

4. Now install the Plugins::

     python examples/plugin_func.py install
     python examples/plugin_cls.py install

5. Look again to the commands::

    >>> wmc -H
           info v0.3.2 - Print some infos
           link v0.3.2 - Concat allvideos to one
         record v0.3.2 - Start the record
          setup v0.3.2 - Some help
     plugin-cls v0.1.0 - A Plugin with a the basic class
    plugin-func v0.1.0 - A Plugin with a function

6. Now you can use the command::

    >>> wmc plugin-cls dummy -h
    usage: wmc plugin-cls [-h] [-V] [--hello]

    Watch me coding, a toolbox

    optional arguments:
    -h, --help     show this help message and exit
    -V, --version  show program's version number and exit
    --hello        say hello

    Copyright 2019 AxJu | WMCv0.3.2


Development
-----------

Virtual environment windows::

  python -m venv venv
  venv\Scripts\activate

Virtual environment linux::

  python3 -m venv venv
  source venv/bin/activate

Setup project::

  python -m pip install --upgrade pip wheel setuptools tox flake8 pylama pylint coverage rstcheck
  python setup.py develop

Run some test::

  tox
  python setup.py test
  python setup.py flake8
  python setup.py check

Test coverage::

  coverage run --source wmc setup.py test
  coverage report -m

Publish package::

  git tag -a 1.0.0a1 -m '1.0.0a1'
  rstcheck README.rst
  python setup.py --version
  python setup.py check
  python setup.py sdist bdist_wheel
  twine upload dist/*
  git push origin 1.0.0a1
  
shields
-------
.. image:: https://img.shields.io/pypi/wheel/wmc
   :alt: Wheel
   :target: https://pypi.org/project/wmc/

.. image:: https://img.shields.io/pypi/implementation/wmc
   :alt: Implementation
   :target: https://pypi.org/project/wmc/
   
.. image:: https://requires.io/github/axju/wmc/requirements.svg?branch=master
   :target: https://requires.io/github/axju/wmc/requirements/?branch=master
   :alt: Requirements

.. image:: https://img.shields.io/pypi/dm/wmc
   :alt: Downloads
   :target: https://pypi.org/project/wmc/

.. image:: https://img.shields.io/github/languages/code-size/axju/wmc
   :alt: GitHub code size in bytes
   
.. image:: https://img.shields.io/github/repo-size/axju/wmc
   :alt: GitHub repo size
   
.. image:: https://img.shields.io/github/issues/axju/wmc
   :alt: GitHub issues
   
.. image:: https://img.shields.io/twitter/follow/0xAxJu?style=social
   :alt: Twitter Follow
   
.. image:: https://img.shields.io/github/v/tag/axju/wmc
   :alt: GitHub tag (latest by date)
