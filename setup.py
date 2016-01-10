__author__ = "Reinhard Fleissner"
__date__ = "$01.01.2016 17:44:17$"

from setuptools import setup, find_packages

setup (
       name='ChEsher',
       version='1.0',
       packages=find_packages(),

       # Declare your packages' dependencies here, for eg:
       install_requires=['foo>=3'],

       # Fill in these to make your Egg ready for upload to
       # PyPI
       author='Reinhard Fleissner',
       author_email='',

       summary='Just another Python package for the cheese shop',
       url='',
       license='',
       long_description='Long description of the package',

       # could also include long_description, download_url, classifiers, etc.

       )