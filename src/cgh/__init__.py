import rich_click as click

from .pr import pr


@click.group()
def main() -> None:
    pass


main.add_command(pr)
