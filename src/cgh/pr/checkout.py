import rich_click as click

from .. import aws, git


@click.command()
@click.argument("ID")
def checkout(id: str) -> None:
    pr_id = id.lstrip("#")
    pr = (
        aws.cli.cmd("codecommit get-pull-request")
        .optv("--pull-request-id", pr_id)
        .json()
        .pullRequest
    )
    branch = pr.pullRequestTargets[0].sourceReference.removeprefix("refs/heads/")
    git.cli.cmd("checkout").args(branch).output()
