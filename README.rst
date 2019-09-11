===============
Watch me coding
===============

Hot to uses
-----------
Create a new project. This is basically a folder with a settings file::

  wmc setup .
  wmc setup test
  wmc info

You can edit the config file or simple start recording::

  wmc record

Render some fake shell commands to make a nice intro::

  wmc intro

And maybe some tools::

  wmc size
  wmc link


Development
-----------

Virtual environment windows::

  python -m venv venv
  venv\Scripts\activate

Virtual environment linux::

  python3 -m venv venv
  source venv/bin/activate

Setup project::

  python -m pip install --upgrade pip wheel setuptools tox flake8
  pip install -e .

Run some test::

  tox
  python setup.py test
  python setup.py flake8
  python setup.py isort
  python setup.py check

ToDo
----

1. expand test
2. create intro render
3. catch exception on cli function call
