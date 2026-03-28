import rich_click as click

from ..aws import get_current_repository_region, get_pr_url
from ..git import get_current_repository
from ..utils import open_browser


@click.command()
@click.argument("ID")
def view(id: str):
    id = id.lstrip("#")
    region = get_current_repository_region()
    assert region is not None
    open_browser(get_pr_url(region, get_current_repository(), id))
