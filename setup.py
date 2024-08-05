from setuptools import setup, find_packages

setup(
    name='aichat-cli',
    version='0.1.1',
    package_dir={'': 'src'},
    packages=find_packages(where='src'),
    install_requires=[
        'openai',
        'rich',
        'ansi',
        'pyperclip',
        'emoji'
    ],
    entry_points={
        'console_scripts': [
            'aichat-cli = src.cli:main',
        ],
    },
)
