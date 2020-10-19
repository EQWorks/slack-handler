from setuptools import setup, find_packages

# read the contents of your README file
from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='slack_handler',
    version='0.1.1',
    packages=find_packages(),
    install_requires=['requests'],
    keywords=['logging', 'slack'],
    description='Slack :tm: handler for the standard Python logging facility.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/EQWorks/slack-handler',
    author='Devs at EQ Works',
    author_email='dev@eqworks.com',
    license='MIT',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Intended Audience :: Developers',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
)
