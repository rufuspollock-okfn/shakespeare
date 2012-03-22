try:
    from setuptools import setup, find_packages
except ImportError:
    from ez_setup import use_setuptools
    use_setuptools()
    from setuptools import setup, find_packages

import sys
sys.path.insert(0, '.')
from shakespeare import __version__, __application_name__
try:
    fo = open('README.rst')
    __long_description__ = fo.read()
except:
    pass

setup(
    name = __application_name__,
    version = __version__,
    packages=find_packages(exclude=['ez_setup']),
    include_package_data=True,

    install_requires=[
        # needed for this version fo Pylons
        'WebOb==1.0.8',
        'Pylons>=0.9.7,<0.9.7.99',
        'SQLAlchemy==0.5.8',
        'Genshi>=0.4',
        'pygooglechart>=0.2,<0.3',
        'FormAlchemy>=1.0',
        # last version to work with SQLA < 0.5
        'SQLAlchemy-migrate==0.4.5',
        'repoze.who>=1.0.0,<1.0.99',
        'repoze.who.plugins.openid>=0.5,<0.5.99',
        ## Needed if you are doing deliverance/proxying stuff
        # you should install python-lxml first directly
        # (has lots of c extensions ...)
        # 'swiss>=0.3',
        # 'deliverance>=0.3a'
        ## Needed for word_of_the_day syncing ...
        'feedparser==5.1.1'
        ],
    test_suite='nose.collector',
    package_data={'shakespeare': ['i18n/*/LC_MESSAGES/*.mo']},
    #message_extractors = {'shakespeare': [
    #        ('**.py', 'python', None),
    #        ('public/**', 'ignore', None)]},
    entry_points='''
    [paste.app_factory]
    main = shakespeare.config.middleware:make_app

    [paste.app_install]
    main = pylons.util:PylonsInstaller

    [console_scripts]
    shakespeare-admin=shakespeare.cli:main
    ''',

    # metadata for upload to PyPI
    author = "Open Knowledge Foundation",
    author_email = 'info@okfn.org',
    description = \
"A full open set of Shakespeare's works along with anciallary material, a variety of tools and a python api",
    long_description = __long_description__,
    license = "MIT",
    keywords = "open shakespeare search view",
    url = "http://www.openshakespeare.org/", 
    download_url = "http://www.openshakespeare.org/code/",
    classifiers = [
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules'],
)
