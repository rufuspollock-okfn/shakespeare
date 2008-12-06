try:
    from setuptools import setup, find_packages
except ImportError:
    from ez_setup import use_setuptools
    use_setuptools()
    from setuptools import setup, find_packages

import sys
sys.path.insert(0, '.')
from shakespeare import __version__, __application_name__
from shakespeare import __doc__ as __long_description__

setup(
    name = __application_name__,
    version = __version__,
    packages=find_packages(exclude=['ez_setup']),
    include_package_data=True,

    install_requires=[
        'Pylons>=0.9.6.1',
        'SQLAlchemy>=0.4,<0.4.99',
        'Genshi>=0.3',
        'pygooglechart>=0.2,<0.3',
        # 'annotater>=0.1',
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

    [paste.paster_command]
    load-shkspr = shksprdata.load:LoadTexts
    load-milton = miltondata.load:LoadTexts

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
