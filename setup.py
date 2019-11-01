# coding=utf8
from setuptools import setup
import os

dir_path = os.path.dirname(os.path.realpath(__file__))

with open('README.md') as f:
    long_description = f.read()

setup(name='cloudformation-utils',
      version='0.0.2',
      description='Utility functions for working with AWS CloudFormation templates',
      long_description=long_description,
      long_description_content_type='text/markdown',
      url='http://github.com/NitorCreations/cloudformation-utils',
      download_url='https://github.com/NitorCreations/cloudformation-utils',
      author='Pasi Niemi',
      author_email='pasi.niemi@nitor.com',
      license='Apache 2.0',
      packages=['cloudformation_utils'],
      include_package_data=True,
      scripts=[],
      entry_points={
          'console_scripts': [],
      },
      setup_requires=['pytest-runner'],
      install_requires=['pyyaml'],
      tests_require=[
          'pytest==4.6.5',
          'pytest-mock==1.10.4',
          'pytest-cov==2.7.1',
          'requests-mock==1.6.0',
          'pytest-runner',
          'mock==3.0.5'
      ],
      test_suite='tests')
