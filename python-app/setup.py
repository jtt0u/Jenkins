"""
Setup script for Jenkins Python Application
Creates installable package
"""
from setuptools import setup, find_packages
import os

# Read version from environment or use default
version = os.environ.get('APP_VERSION', '1.0.0')
build = os.environ.get('BUILD_NUMBER', '0')

setup(
    name='jenkins-python-app',
    version=f'{version}',
    description='Jenkins Course - Python Application for CI/CD demonstrations',
    long_description=open('README.md').read() if os.path.exists('README.md') else '',
    long_description_content_type='text/markdown',
    author='Jenkins Course',
    author_email='course@example.com',
    url='https://github.com/example/jenkins-python-app',
    py_modules=['app'],
    install_requires=[
        'flask>=3.0.0',
        'requests>=2.31.0',
    ],
    extras_require={
        'dev': [
            'pytest>=7.4.3',
            'pytest-cov>=4.1.0',
        ]
    },
    entry_points={
        'console_scripts': [
            'jenkins-app=app:main',
        ],
    },
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Education',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
    ],
    python_requires='>=3.8',
)
