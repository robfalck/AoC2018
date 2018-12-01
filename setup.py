from distutils.core import setup
from setuptools import find_packages


setup(name='aoc2018',
    version='0.0.1',
    description='Solutions to the Advent of Code - 2018',
    url='https://github.com/robfalck/AoC2018',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: Apache 2.0',
        'Natural Language :: English',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: POSIX :: Linux',
        'Operating System :: Microsoft :: Windows',
        'Topic :: Scientific/Engineering',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: Implementation :: CPython',
    ],
    license='Apache License',
    packages=find_packages(),
    install_requires=[
        'numpy>=1.14.1',
        'scipy>=0.19.1',
        'six',
        'pep8',
        'parameterized'
    ],
    zip_safe=False,
)
