========================================================
Jedha - Easy Cisco CDP Parse
========================================================

.. image:: https://img.shields.io/travis/richardstrnad/jedha/master.svg?style=flat-square
   :target: https://travis-ci.org/richardstrnad/jedha
   :alt: Travis CI Status

.. image:: https://img.shields.io/pypi/v/jedha.svg?style=flat-square
   :target: https://pypi.python.org/pypi/jedha/
   :alt: Version

.. image:: https://img.shields.io/github/tag/richardstrnad/jedha.svg?style=flat-square   
   :target: https://github.com/richardstrnad/jedha
   :alt: GitHub Version

.. image:: http://img.shields.io/badge/license-GPLv3-blue.svg?style=flat-square
   :target: https://www.gnu.org/copyleft/gpl.html
   :alt: License

.. image:: https://img.shields.io/github/issues/richardstrnad/jedha.svg?style=flat-square
   :target: https://github.com/richardstrnad/jedha/issues
   :alt: Issues

.. image:: https://img.shields.io/github/stars/richardstrnad/jedha.svg?style=flat-square
   :target: https://github.com/richardstrnad/jedha/stargazers
   :alt: Stars

.. image:: https://img.shields.io/badge/Richard-Strnad-blue.svg?style=flat-square
   :alt: RichardStrnad

.. contents:: Table of Contents

.. _introduction:

Introduction: What is jedha?
=====================================

jedha is a Python_ library, which parses through Cisco CDP output and generates 
python objects out of it.


Usage
====

jedha takes the output of :code:`show cdp neighbors detail` as input.

.. code:: python

  cdp_input = '''MYSwitch01#show cdp neighbors detail
  -------------------------
  Device ID: NETS999999.domain.local
  Entry address(es):
    IP address: 192.168.1.19
  Platform: WS-C3560-48PS,  Capabilities: Switch IGMP
  Interface: GigabitEthernet2/0/23,  Port ID (outgoing port): GigabitEthernet0/1
  Holdtime : 124 sec

  Version :
  Cisco IOS Software, C3560 Software (C3560-IPBASEK9-M), Version 12.2(52)SE, RELEASE SOFTWARE (fc3)
  Copyright (c) 1986-2009 by Cisco Systems, Inc.
  Compiled Fri 25-Sep-09 08:13 by sasyamal

  advertisement version: 2
  Protocol Hello:  OUI=0x00000C, Protocol ID=0x0112; payload len=27, value=RandVal
  VTP Management Domain: ''
  Native VLAN: 1
  Duplex: full
  Management address(es):
    IP address: 192.168.1.19
  '''

  from jedha.cdp import *

  dev = Device(cdp_input)
  
This device object provides a various of methods.


- The Docs follow soon...
- jedha tutorial follow soon...

.. _Pre-Requisites:

Pre-requisites
==============

jedha_ requires Python versions 3.4+; the OS should not
matter. If you want to run it under a Python virtualenv_, it's been heavily 
tested in that environment as well.

.. _Installation:

Installation and Downloads
==========================

The best way to get jedha is with or pip_. 
::

      pip install --upgrade jedha


Otherwise `download it from PyPi <https://pypi.python.org/pypi/jedha>`_, extract it and run the ``setup.py`` script:

::

      python setup.py install

If you're interested in the source, you can always pull from the `github repo`_:


- From github_:

::

      git clone https://github.com/richardstrnad/jedha.git

.. _Samples:

Samples
=======

::

    python samples/sample_script.py samples/sample_input.txt
    python samples/sample_script_ciscocmd.py samples/sample_input_ciscocmd.txt


.. _Unit-Tests:

Unit-Tests
==========

`Travis CI project <https://travis-ci.org>`_ tests jedha on Python versions 3.4 through 3.7-dev

Click the image below for details; the current build status is:

.. image:: https://img.shields.io/travis/richardstrnad/jedha/master.svg?style=flat-square
   :target: https://travis-ci.org/richardstrnad/jedha
   :alt: Travis CI Status

.. _`License and Copyright`:

License and Copyright
=====================

jedha_ is licensed GPLv3_; 
2016.


.. _Author:

Author and Thanks
=================

jedha_ was developed by Richard Strnad

.. _jedha: https://pypi.python.org/pypi/jedha

.. _Python: http://python.org/

.. _setuptools: https://pypi.python.org/pypi/setuptools

.. _pip: https://pypi.python.org/pypi/pip

.. _virtualenv: https://pypi.python.org/pypi/virtualenv

.. _`github repo`: https://github.com/richardstrnad/jedha

.. _github: https://github.com/richardstrnad/jedha

.. _`GPLv3`: http://www.gnu.org/licenses/gpl-3.0.html
