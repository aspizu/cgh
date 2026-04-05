import rich_click as click

from .create import create
from .edit import edit
from .list import list_prs
from .view import view


@click.group()
def pr() -> None:
    pass


pr.add_command(create)
pr.add_command(edit)
pr.add_command(list_prs, "list")
pr.add_command(view)
