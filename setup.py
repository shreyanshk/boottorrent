#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst', encoding='utf-8') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst', encoding='utf-8') as history_file:
    history = history_file.read()

with open('requirements.txt', encoding='utf-8') as req_file:
    requirements = [i for i in req_file.read().split('\n') if i]

setup(
    author="Shreyansh Khajanchi",
    author_email='shreyansh_k@live.com',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
    ],
    description="P2P bittorrent based network boot",
    entry_points={
        'console_scripts': [
            'boottorrent=boottorrent.cli:parse_args',
        ],
    },
    install_requires=requirements,
    license="GNU General Public License v3",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='boottorrent',
    name='boottorrent',
    packages=find_packages(include=['boottorrent']),
    python_requires='>=3.6',
    url='https://github.com/shreyanshk/boottorrent',
    version='0.1.0',
    zip_safe=False,
)
