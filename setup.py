from setuptools import setup
from wallies import __name__, __version__


APP = ['app.py']
DATA_FILES = []
OPTIONS = {
    'iconfile': 'icon.icns',
    'argv_emulation': True,
    'plist': {
        'LSUIElement': True,
        'CFBundleIdentifier': f'net.cacko.{__name__.lower()}',
        'CFBundleVersion': __version__
    },
    'packages': [
        'rumps',
        'dataclasses_json',
        'requests',
        'appdir',
        'click',
        "PyYAML",
        
    ],
}
setup(
    app=APP,
    name=__name__,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)
