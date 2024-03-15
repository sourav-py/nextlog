from setuptools import setup, find_packages
from pathlib import Path

description = 'A logging library with asynchronous logs dispatch to Loki.'

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name='nextlog',
    version='1.1.1',
    description=description,
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Sourav',
    author_email='imsrv2k@gmail.com',
    url="https://github.com/sourav-py/nextlog",
    packages=find_packages(),
    install_requires=[
        # list of dependencies
        'requests',
        'redis'
    ],
)