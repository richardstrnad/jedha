'''
jedha Installer using setuptools
'''
import os
from setuptools import setup

from jedha.__about__ import (__title__, __version__, __summary__, __author__,
                             __email__)

def read(fname):
    '''
    Reads the variables from the fname file
    '''
    # Dynamically generate setup(long_description)
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(name=__title__,
      version=__version__,
      description=__summary__,
      author=__author__,
      author_email=__email__,
      packages=['jedha'],
      long_description=read('README.rst')
     )
