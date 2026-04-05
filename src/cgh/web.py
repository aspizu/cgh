import rich_click as click

from . import aws, git
from .utils import open_browser


@click.command()
def web() -> None:
    region = aws.get_current_repo_region()
    repo = git.get_current_repository()
    branch = git.get_current_branch()
    url = f"https://{region}.console.aws.amazon.com/codesuite/codecommit/repositories/{repo}/browse/refs/heads/{branch}?region={region}"
    open_browser(url)