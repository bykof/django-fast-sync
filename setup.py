from distutils.core import setup

setup(
    name='django-fast-sync',
    version='0.2.1',
    packages=['django_fast_sync'],
    url='https://github.com/bykof/django-fast-sync',
    license='Apache License',
    include_package_data=True,
    author='mbykovski',
    author_email='mbykovski@seibert-media.net',
    description='A Django app which helps you to import a lot of data with raw SQL', requires=['django']
)
