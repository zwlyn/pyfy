#!/usr/bin/env python
#-*- coding:utf-8 -*-

from setuptools import setup, find_packages 

setup(
    name = "py-fy",      
    version = "2.0.3",  
    keywords = ("pip", "py-fy","translate", "fy"),
    description = "An Word-translation software stranslate between simple-Chinese and English",
    long_description = "An Word-translation software translate between simple-Chinese and English",
    license = "MIT Licence",
    url = "https://github.com/zwlyn/pyfy",     
    author = "zwlyn",
    author_email = "1666013677@qq.com",
    packages = find_packages(),
    include_package_data = True,
    platforms = "any",
    install_requires = ["pymouse", "pyinstaller"],          
    python_requires=">=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*",
    classifiers=[
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy'
    ]
)

