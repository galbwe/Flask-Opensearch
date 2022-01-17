"""
Flask-Opensearch
-------------
Flask extension for Opensearch integration.
"""
from setuptools import setup


setup(
    name='Flask-Opensearch',
    version='0.0.0',
    url='https://github.com/galbwe/Flask-Opensearch',
    license='MIT',
    author='Wes Galbraith',
    author_email='galbwe92@gmail.com',
    description='Flask extension for opensearch integration',
    long_description=__doc__,
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