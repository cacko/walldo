from setuptools import setup
from walldo import __name__
import sys
from pathlib import Path
import semver


def version():
    if len(sys.argv) > 1 and sys.argv[1] == "py2app":
        init = Path(__file__).parent / __name__.lower() / "version.py"
        _, v = init.read_text().split(" = ")
        cv = semver.VersionInfo.parse(v.strip().strip('"'))
        nv = f"{cv.bump_patch()}"
        init.write_text(f'__version__ = "{nv}"')
        return nv
    from walldo.version import __version__

    return __version__


def resolve_libs(libs):
    env = Path(sys.executable)
    root = env.parent.parent / "lib"
    return [(root / f).as_posix() for f in libs]


APP = ['app.py']
DATA_FILES: list[str] = []
OPTIONS = {
    'iconfile': 'icon.icns',
    'argv_emulation': False,
    "emulate_shell_environment": True,
    "plist": {
        "LSUIElement": True,
        "CFBundleIdentifier": "net.cacko.walldo",
        "CFBundleVersion": f"{version()}",
        "LSEnvironment": dict(
            WALLDO_LOG_LEVEL="CRITICAL",
        ),
    },
    "packages": [
        "apscheduler",
    ],
    "frameworks": resolve_libs(
        [
            "libffi.dylib",
            "libssl.dylib",
            "libcrypto.dylib",
        ]
    ),
}
setup(
    app=APP,
    name=__name__,
    # data_files=DATA_FILES,
    options={'py2app': OPTIONS},
)
