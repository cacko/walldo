import click


class YankoCommand(click.Group):

    def list_commands(self, ctx: click.Context) -> list[str]:
        return list(self.commands)


@click.group(cls=YankoCommand)
def cli():
    """This script showcases different terminal UI helpers in Click."""
    pass
