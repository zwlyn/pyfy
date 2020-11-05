#!/usr/bin/env python
#-*- coding:utf-8 -*-

from setuptools import setup, find_packages            #这个包没有的可以pip一下

setup(
    name = "pyfy",      #这里是pip项目发布的名称
    version = "2.0.0",  #版本号，数值大的会优先被pip
    keywords = ("pip", "pyfy","featureextraction"),
    description = "",
    long_description = "An Word-translation software simple-Chinese ⇆ English",
    license = "MIT Licence",
    url = "https://github.com/zwlyn/pyfy",     #项目相关文件地址，一般是github
    author = "zwlyn",
    author_email = "1666013677@qq.com",
    packages = find_packages(),
    include_package_data = True,
    platforms = "any",
    install_requires = ["pymouse", "pyinstaller"]          #这个项目需要的第三方库
)

