from setuptools import setup, find_packages

setup(
    name='MediaWikiAPI',
    version='0.1.0',
    description='A Python wrapper for the MediaWiki API',
    author='Huascar Fiorletta',
    url='https://github.com/huascarfiorletta/MediaWikiAPI',
    packages=find_packages(),
    install_requires=[
        'requests',  # Add any other dependencies your package needs
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)