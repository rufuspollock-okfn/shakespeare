import ez_setup
ez_setup.use_setuptools()
from setuptools import setup, find_packages

import sys
sys.path.append('./src')
from shakespeare import __version__, __application_name__

setup(
    name = __application_name__,
    version = __version__,
    packages = find_packages(),
    scripts = ['bin/shakespeare-admin'],

    install_requires = ['SQLObject>=0.6,<=0.7.99'],
    # don't require cherrypy and kid as they are not needed for the core
    # library -- only for the web interface
    extras_require = {
        'web_gui' : ['CherryPy>=0.3', 'kid>=0.9'],
        },

    # metadata for upload to PyPI
    author = "Rufus Pollock (Open Knowledge Foundation)",
    author_email = "rufus.pollock@okfn.org",
    description = \
"A complete open set of Shakespeare's works along with an extensive python api",
    long_description = \
"""
The Open Shakespeare package provides a complete set of shakespeare's works
(often in multiple versions) along with ancillary material and functionality
such as an introduction, chronology, explanatory notes and search facilities.

All material is open source/open knowledge so that anyone can use, redistribute
and reuse these materials freely. For exact details of the license under which
this package is made available please see COPYING.txt.

Open Shakespeare has been developed under the aegis of the Open Knowledge
Foundation (http://www.okfn.org/).
""",
    license = "MIT",
    keywords = "open shakespeare search view",
    url = "http://www.openshakespeare.org/", 
    download_url = "http://www.openshakespeare.org/download/",
    classifiers = [
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules'],
)
