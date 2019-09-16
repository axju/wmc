===============
Watch me coding
===============
.. image:: https://img.shields.io/pypi/v/wmc
   :alt: PyPI
   :target: https://pypi.org/project/wmc/

.. image:: https://img.shields.io/pypi/pyversions/wmc
   :alt: Python Version
   :target: https://pypi.org/project/wmc/

.. image:: https://img.shields.io/pypi/wheel/wmc
   :alt: Wheel
   :target: https://pypi.org/project/wmc/

.. image:: https://img.shields.io/pypi/implementation/wmc
   :alt: Implementation
   :target: https://pypi.org/project/wmc/

.. image:: https://img.shields.io/pypi/dm/wmc
   :alt: Downloads
   :target: https://pypi.org/project/wmc/

.. image:: https://img.shields.io/pypi/l/wmc
   :alt: License
   :target: https://pypi.org/project/wmc/

Install
-------
It is on PyPi::

  pip install wmc

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

  python -m pip install --upgrade pip wheel setuptools tox flake8 pylama pylint coverage
  python setup.py develop

Run some test::

  tox
  python setup.py test
  python setup.py flake8
  python setup.py check

Test coverage::

  coverage run --source wmc setup.py test
  coverage report -m
