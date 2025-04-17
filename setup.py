from setuptools import setup

APP = ['sudoku.py']
DATA_FILES = []
OPTIONS = {
    'argv_emulation': True,
    'includes': ['toga', 'toga_cocoa'],
    'iconfile': 'sudoku_icon.png',
    'packages': ['toga'],
    'plist': {
        'CFBundleName': 'Sudoku by Bachi',
        'CFBundleDisplayName': 'Sudoku by Bachi Peachy',
        'CFBundleIdentifier': 'com.bachipeachy.sudoku',
        'CFBundleVersion': '1.0',
        'CFBundleShortVersionString': '1.0',
        'NSHumanReadableCopyright': 'Copyright © 2025 Bachi Peachy',
    },
}

setup(
    app=APP,
    name='Sudoku by Bachi',
    version='1.0',
    author='Bachi Peachy',
    author_email='bachipeachy@users.noreply.github.com',
    description='A simple and stylish Sudoku game for macOS, built with Toga.',
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)
