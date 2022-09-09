from setuptools import setup
from wallies import __name__
import sys
from pathlib import Path
import semver

def version():
    if len(sys.argv) > 1 and sys.argv[1] == "py2app":
        init = Path(__file__).parent / __name__.lower() / "version.py"
        _, v = init.read_text().split(" = ")
        cv = semver.VersionInfo.parse(v.strip('"'))
        nv = f"{cv.bump_patch()}"
        init.write_text(f'__version__ = "{nv}"')
        return nv
    from wallies.version import __version__

    return __version__


def resolve_libs(libs):
    env = Path(sys.executable)
    root = env.parent.parent / "lib"
    return [(root / f).as_posix() for f in libs]


APP = ['app.py']
DATA_FILES = []
OPTIONS = {
    'iconfile': 'icon.icns',
    'argv_emulation': True,
    'plist': {
        'LSUIElement': True,
        'CFBundleIdentifier': f'net.cacko.{__name__.lower()}',
        'CFBundleVersion': version()
    },
    'packages': [
        'rumps',
        'dataclasses_json',
        'requests',
        'appdir',
        'click',
        "yaml",
    ],
    "frameworks": resolve_libs(
        [
            "libffi.8.dylib",
            "libtcl8.6.dylib",
            "libtk8.6.dylib",
            "libssl.3.dylib",
            "libcrypto.3.dylib",
        ]
    ),
}
setup(
    app=APP,
    name=__name__,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)
