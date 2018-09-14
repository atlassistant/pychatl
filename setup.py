from setuptools import setup, find_packages
import os

with open('README.rst', encoding='utf8') as f:
  readme = f.read()

with open('pychatl/version.py') as f:
  version = f.readline().strip()[15:-1]

setup(
  name='pychatl',
  version=version,
  description='Tiny DSL to generate training dataset for NLU engines',
  long_description=readme,
  url='https://github.com/atlassistant/pychatl',
  author='Julien LEICHER',
  license='GPL-3.0',
  packages=find_packages(),
  include_package_data=True,
  install_requires=[
    'Arpeggio==1.9.0',
  ],
  # entry_points={
  #   'console_scripts': [
  #     'pytlas = pytlas.cli:main',
  #   ]
  # },
)