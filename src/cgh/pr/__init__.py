import rich_click as click

from .list import list


@click.group()
def pr():
    pass


pr.add_command(list)
