from sys import argv

if len(argv) > 1:
    from wallies.cli import cli
    cli()
else:
    from wallies import start
    start()
