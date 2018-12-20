#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ========================================================
# Module         :  setup
# Author         :  Null
# Create Date    :  11/11/2018
# Amended by     :  Null
# Amend History  :  11/11/2018
# ========================================================
try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup, find_packages

setup(
    name='Marketing_Android_Auto',
    version='1.0.0',
    author='Null',
    author_email='546464268@qq.com',
    description='',
    keywords='',
    license='MLT',
    url='',
    package=find_packages(),
    install_requires=[
        'pyyaml', 'matplotlib', 'Appium-Python-Client', 'selenium', 'termcolor'
    ],
    zip_safe=False
)
