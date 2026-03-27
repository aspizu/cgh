import builtins
from datetime import datetime

import humanize
import rich_click as click
from rich import box, print
from rich.table import Table
from rich.text import Text

from ..aws import get_user_arn, parse_user_arn
from ..command import aws
from ..git import get_current_repository


@click.command()
@click.option(
    "--author", "-a", help="Filter by author username. (@me for your PRs)", default=None
)
@click.option(
    "--status", "-s", help="Status of the PR. (open, closed, merged)", default="open"
)
def list(author: str | None, status: str):
    author_arn = author and get_user_arn(None if author == "@me" else author)
    pr_ids: builtins.list[str] = (
        aws.cmd("codecommit list-pull-requests")
        .optv("--repository-name", get_current_repository())
        .optv("--pull-request-status", status)
        .optv("--author-arn", author_arn)
        .json()
        .pullRequestIds
    )
    table = Table(
        "ID",
        "Author",
        "Title",
        "Branch",
        "Updated",
        "Created",
        box=box.MINIMAL_HEAVY_HEAD,
    )
    for pr_id in pr_ids:
        pr = (
            aws.cmd("codecommit get-pull-request")
            .optv("--pull-request-id", pr_id)
            .json()
            .pullRequest
        )
        author_arn = parse_user_arn(pr.authorArn)
        author_username = author_arn and author_arn.username
        src = pr.pullRequestTargets[0].sourceReference.removeprefix("refs/heads/")
        dest = pr.pullRequestTargets[0].destinationReference.removeprefix("refs/heads/")
        table.add_row(
            Text(
                f"#{pr_id}",
                style={
                    "OPEN": "green",
                    "CLOSED": "red",
                    "merged": "gray",
                }[pr.pullRequestStatus],
            ),
            str(author_username),
            pr.title,
            f"{dest} <- {src}",
            humanize.naturaltime(datetime.fromisoformat(pr.lastActivityDate)),
            humanize.naturaltime(datetime.fromisoformat(pr.creationDate)),
        )
    print(table)
