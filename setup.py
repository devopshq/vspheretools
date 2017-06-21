#!/usr/bin/env python
# -*- coding: utf-8 -*-


from setuptools import setup
import os

__version__ = '1.0'  # identify main version of vspheretools
devStatus = '4 - Beta'  # default build status, see: https://pypi.python.org/pypi?%3Aaction=list_classifiers

if 'TRAVIS_BUILD_NUMBER' in os.environ and 'TRAVIS_BRANCH' in os.environ:
    print("This is TRAVIS-CI build")
    print("TRAVIS_BUILD_NUMBER = {}".format(os.environ['TRAVIS_BUILD_NUMBER']))
    print("TRAVIS_BRANCH = {}".format(os.environ['TRAVIS_BRANCH']))

    __version__ += '.{}{}'.format(
        '' if 'release' in os.environ['TRAVIS_BRANCH'] or os.environ['TRAVIS_BRANCH'] == 'master' else 'dev',
        os.environ['TRAVIS_BUILD_NUMBER'],
    )

    devStatus = '5 - Production/Stable' if 'release' in os.environ['TRAVIS_BRANCH'] or os.environ['TRAVIS_BRANCH'] == 'master' else devStatus

else:
    print("This is local build")
    __version__ += '.localbuild'  # set version as major.minor.localbuild if local build: python setup.py install

print("vspheretools build version = {}".format(__version__))


setup(
    name='vspheretools',

    version=__version__,

    description='vSphereTools is a set of scripts from DevOpsHQ to support working with vSphere and virtual machines (VMs) on it, which are based on the pysphere library.',

    long_description='You can see detailed user manual here: https://devopshq.github.io/vspheretools/',

    license='MIT',

    author='Timur Gilmullin',

    author_email='tim55667757@gmail.com',

    url='https://devopshq.github.io/vspheretools/',

    download_url='https://github.com/devopshq/vspheretools.git',

    entry_points={'console_scripts': ['vspheretools = VSphereTools:Main']},

    classifiers=[
        'Development Status :: {}'.format(devStatus),
        'Environment :: Console',
        'Intended Audience :: System Administrators',
        'Topic :: Utilities',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 2.7',
    ],

    keywords=[
        'vsphere',
        'sphere client',
        'client',
        'classificator',
        'utility',
        'virtual',
        'VM',
        'virtualization',
        'routines',
    ],

    packages=[
        '.',
    ],

    setup_requires=[
    ],

    tests_require=[
        'pytest',
    ],

    install_requires=[
    ],

    package_data={
        '': [
            './pysphere/*.py',
            './pysphere/resources/*.py',
            './pysphere/ZSI/*.py',
            './pysphere/ZSI/LBNLCopyright',
            './pysphere/ZSI/generate/*.py',
            './pysphere/ZSI/wstools/*.py',

            'VSphereTools.py',
            'Logger.py',

            'LICENSE',
            'README.md',
        ],
    },

    zip_safe=True,
)
