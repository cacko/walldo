# nuitka-project: --macos-create-app-bundle
# nuitka-project: --macos-app-name=walldo
# nuitka-project: --macos-app-mode=ui-element
# nuitka-project: --product-name=walldo
# nuitka-project: --macos-signed-app-name=net.cacko.walldo
# nuitka-project: --macos-sign-identity=5D6C94808201B324ACB57431A017780BB494D9DC
# nuitka-project: --file-description=walldo
# nuitka-project: --macos-app-icon={MAIN_DIRECTORY}/icon.png
# nuitka-project: --file-version="0.2.0"
# nuitka-project: --product-version="0.2.0"
# nuitka-project: --macos-app-version="0.2.0"


from sys import argv

if len(argv) > 1:
    from walldo.cli import cli
    cli()
else:
    from walldo import start
    start()
