import rich_click as click

from .. import aws, git
from ..errors import Error


@click.command()
@click.argument("ID")
@click.option(
    "--strategy",
    type=click.Choice(["fast-forward", "squash"]),
    default="squash",
    help="Merge strategy.",
)
@click.option(
    "--description",
    "-d",
    help="Description for this merge.",
)
def merge(id: str, strategy: str, description: str | None) -> None:
    pr_id = id.lstrip("#")
    repo_name = git.get_current_repository()

    pr = (
        aws.cli.cmd("codecommit get-pull-request")
        .optv("--pull-request-id", pr_id)
        .json()
        .pullRequest
    )

    if pr.pullRequestStatus == "MERGED":
        msg = f"PR #{pr_id} is already merged."
        raise Error(msg)

    if pr.pullRequestStatus == "CLOSED":
        msg = f"PR #{pr_id} is closed and cannot be merged."
        raise Error(msg)

    target = pr.pullRequestTargets[0]
    _source_branch = target.sourceReference.removeprefix("refs/heads/")
    dest_branch = target.destinationReference.removeprefix("refs/heads/")

    if description is None:
        description = f"Merged PR #{pr_id}: {pr.title}"

    if strategy == "fast-forward":
        result = (
            aws.cli.cmd("codecommit merge-pull-request-by-fast-forward")
            .optv("--pull-request-id", pr_id)
            .optv("--repository-name", repo_name)
            .optv("--source-commit-id", target.sourceCommit)
            .optv("--commit-message", description)
            .json()
        )
    else:
        result = (
            aws.cli.cmd("codecommit merge-pull-request-by-squash")
            .optv("--pull-request-id", pr_id)
            .optv("--repository-name", repo_name)
            .optv("--source-commit-id", target.sourceCommit)
            .optv("--commit-message", description)
            .json()
        )

    click.echo(f"Successfully merged PR #{pr_id} into {dest_branch}")
    click.echo(f"New commit: {result.commitId}")
