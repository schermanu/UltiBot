# -*- coding: utf-8 -*-
from setuptools import setup, find_packages


with open('README.md') as f:
    readme = f.read()

# with open('LICENSE') as f:
#     license = f.read()

setup(
    name='ConstantiaBot',
    # version='0.1.0',
    description='bot for the constantia discord server',
    long_description=readme,
    # author='Multiple',
    # author_email='me@kennethreitz.com',
    # url='https://github.com/kennethreitz/samplemod',
    # license=license,
    packages=find_packages(exclude=('tests', 'docs'))
)
