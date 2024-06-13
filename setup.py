from setuptools import setup, find_packages

setup(
    name = 'MindustryTools',
    version = '0.1a1',
    description = 'A series of tools for the game Mindustry, by Anuke.',
    long_description = open('README.md').read(),
    long_description_content_type='text/markdown',
    author = 'Samuel Squires',
    author_email = 'sdsquires@gmail.com',
    url = 'https://github.com/sdsquire/MindustryTools',
    packages = find_packages(),
    classifiers = [
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Intended Audience :: Fans',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.11',
    ],
    python_requires = '>=3.8',
    install_requires = [],

)