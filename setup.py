import os
import codecs
from setuptools import setup, find_packages


# read() and get_version() derived from https://github.com/pypa/pip/blob/main/setup.py
# TODO: with setuptools 46.4.0+ one can use setup.cfg to do this:
# [metadata]
# version = attr: package.__version__
def read(rel_path):
    here = os.path.abspath(os.path.dirname(__file__))
    with codecs.open(os.path.join(here, rel_path), 'r') as fp:
        return fp.read()


def get_version(rel_path):
    for line in read(rel_path).splitlines():
        if line.startswith('__version__'):
            delim = '"' if '"' in line else "'"
            return line.split(delim)[1]

    raise RuntimeError('Unable to find version string.')


setup(
    name='slack_handler',
    version=get_version('slack_handler/__init__.py'),
    packages=find_packages(),
    install_requires=['requests'],
    keywords=['logging', 'slack'],
    description='Slack :tm: handler for the standard Python logging facility.',
    url='https://github.com/EQWorks/slack-handler',
    author='Devs at EQ Works',
    author_email='dev@eqworks.com',
    license='MIT',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Intended Audience :: Developers',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
)
