import os
from setuptools import setup

with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='django-sendpdf',
    version='0.1.0',
    packages=['sendpdf'],
    include_package_data=True,
    license='MIT License',
    description='Generate PDF from html templates and print, view or send via email',
    install_requires=['Django', 'pdfkit'],
    long_description=README,
    url='http://pythonhosted.org/django-sendpdf/',
    author='James Wanderi',
    author_email='wanderi@wanderi.me',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        "Development Status :: 5 - Production/Stable",
        "Natural Language :: English",
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
