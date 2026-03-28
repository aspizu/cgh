import rich_click as click

from .create import create
from .list import list
from .view import view


@click.group()
def pr():
    pass


pr.add_command(create)
pr.add_command(list)
pr.add_command(view)
