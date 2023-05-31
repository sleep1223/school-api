#!/usr/bin/env python
# coding=utf-8

from setuptools import setup

with open('README.md', 'rb') as f:
    long_description = f.read().decode('utf-8').split("## User permissions")[0]

setup(
    name='school-api',
    version='1.0',
    packages=['school_api', 'school_api.client', 'school_api.client.api', 'school_api.client.api.utils', 'school_api.session', 'school_api.check_code'],
    url='https://github.com/sleep1223/school-api',
    license='MIT',
    author='sleep1223',
    author_email='sleep1223@outlook.com',
    description=''
long_description = long_description,
long_description_content_type = 'text/markdown',
packages = find_packages(),
package_data = {'school_api': ['check_code/theta.dat'], },
include_package_data = True,
platforms = 'any',
zip_safe = False,

install_requires = [
    'six',
    'requests',
    'redis',
    'bs4',
    'pillow',
    'numpy',
    'beautifulsoup4',
    'openpyxl'

],
classifiers = [
    'Environment :: Web Environment',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: MIT License',
    'Operating System :: OS Independent',
    'Programming Language :: Python :: 2.7',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.3',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    'Topic :: Software Development :: Libraries :: Python Modules'
]

)
