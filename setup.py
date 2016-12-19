'''
jedha Installer using setuptools
'''
import os
from setuptools import setup

base_dir = os.path.dirname(__file__)

about = {}
with open(os.path.join(base_dir, 'jedha', '__about__.py')) as f:
    exec(f.read(), about)

setup(name=about['__title__'],
      version=about['__version__'],
      description=about['__summary__'],
      author=about['__author__'],
      author_email=about['__email__'],
      packages=['jedha'],
)