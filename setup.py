from distutils.core import setup
from setuptools import find_packages

setup(
    name='django-fast-sync',
    version='0.2.3',
    packages=find_packages(),
    url='https://github.com/bykof/django-fast-sync',
    license='Apache License',
    include_package_data=True,
    author='mbykovski',
    author_email='mbykovski@seibert-media.net',
    description='A Django app which helps you to import a lot of data with raw SQL', requires=['django']
)
