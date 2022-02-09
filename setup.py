"""
Flask-Opensearch
-------------
Flask extension for Opensearch integration.
"""
import os
from setuptools import setup


VERSION = "1.0.1"


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name='Flask-Opensearch',
    version=VERSION,
    url='https://github.com/galbwe/Flask-Opensearch',
    license='MIT',
    author='Wes Galbraith',
    author_email='galbwe92@gmail.com',
    description='Flask extension for opensearch integration',
    long_description=read("README.md"),
    long_description_content_type="text/markdown",
    py_modules=['flask_opensearch'],
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    python_requires='>=3.6',
    install_requires=[
        'Flask',
        'opensearch-py',
        'aws-requests-auth',
    ],
    setup_requires=["flake8", "black", "pytest-runner"],
    tests_require=['pytest', 'tox'],
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)