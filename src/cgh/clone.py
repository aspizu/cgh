from pathlib import Path

import rich_click as click

from . import aws
from . import git as git_


@click.command()
@click.argument("REPO_NAME")
@click.argument("DIRECTORY", required=False)
def clone(repo_name: str, directory: str | None) -> None:
    if directory is None:
        directory = repo_name
    if Path(directory).exists():
        msg = f"Directory '{directory}' already exists"
        raise RuntimeError(msg)
    clone_url = (
        aws.cli.cmd("codecommit get-repository")
        .optv("--repository-name", repo_name)
        .json()
        .repositoryMetadata.cloneUrlHttp
    )
    git_.cli.cmd("clone").args(clone_url, directory).run()
