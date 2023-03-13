from sys import argv

if len(argv) > 1:
    from walldo.cli import cli
    cli()
else:
    from walldo import start
    start()
