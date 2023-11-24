from setuptools import setup
from walldo import __name__
import sys
from pathlib import Path
import semver
import distutils
from walldo.version import __version__


class VersionCommand(distutils.cmd.Command):

    description = 'increment app version'
    user_options = [
        ('version=', None, 'new version'),
    ]

    def initialize_options(self):
        self.version = __version__

    def finalize_options(self):
        pass

    def run(self):
        init = Path(__file__).parent / __name__.lower() / "version.py"
        cv = semver.VersionInfo.parse(self.version)
        nv = f"{cv.bump_patch()}"
        init.write_text(f'__version__ = "{nv}"')


def resolve_libs(libs):
    env = Path(sys.executable)
    root = env.parent.parent / "lib"
    return [(root / f).as_posix() for f in libs]


APP = ["app.py"]
DATA_FILES: list[str] = []
OPTIONS = {
    "iconfile": "icon.icns",
    "argv_emulation": False,
    "emulate_shell_environment": True,
    "no_strip": True,
    "plist": {
        "LSUIElement": True,
        "CFBundleIdentifier": "net.cacko.walldo",
        "CFBundleVersion": __version__,
        "LSEnvironment": dict(
            WALLDO_LOG_LEVEL="CRITICAL",
        ),
    },
    "packages": ["apscheduler", "click"],
    "frameworks": resolve_libs(
        [
            "libffi.dylib",
            "libssl.dylib",
            "libcrypto.dylib",
        ]
    ),
}
setup(
    cmdclass={
        "version": VersionCommand,
    },
    app=APP,
    name=__name__,
    data_files=DATA_FILES,
    options={"py2app": OPTIONS},
)
