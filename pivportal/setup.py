#!/usr/bin/env python

import os
import sys

sys.path.insert(0, os.path.abspath('lib'))
from pivportal import __version__, __author__

try:
    from setuptools import setup, find_packages
except ImportError:
    print("pivportal needs setuptools in order to build. Install it using"
            " your package manager (usually python-setuptools) or via pip (pip"
            " install setuptools).")
    sys.exit(1)

setup(name='pivportal',
      version=__version__,
      description='Secure Linux sudo access using a PIV card.',
      author=__author__,
      author_email='david@davidwhiteside.com',
      url='https://github.com/starboarder2001/pivportal/pivportal',
      license='MIT',
      install_requires=["flask", "PyYAML", "PyJWT", "setuptools"],
      package_dir={ '': 'lib' },
      packages=find_packages('lib'),
      classifiers=[
          'Environment :: Console',
          'Intended Audience :: Information Technology',
          'Intended Audience :: System Administrators',
          'License :: OSI Approved :: MIT License',
          'Natural Language :: English',
          'Operating System :: POSIX',
          'Programming Language :: Python :: 2.6',
          'Programming Language :: Python :: 2.7',
          'Topic :: System :: Installation/Setup',
          'Topic :: System :: Systems Administration',
          'Topic :: Utilities',
      ],
      scripts=[
         'bin/pivportal',
      ],
      package_data={"": ["data_files/pivportal/*", "data_files/pivportal/css/*", "data_files/pivportal/imgs/*", "data_files/pivportal/js/*", "data_files/pivportal/templates/*"]},
)
