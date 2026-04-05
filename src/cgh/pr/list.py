from datetime import datetime

import humanize
import rich_click as click
from rich import box, print
from rich.table import Table
from rich.text import Text

from .. import aws, git
from ..aws import UserArn


@click.command()
@click.option(
    "--author", "-a", help="Filter by author username. (@me for your PRs)", default=None
)
@click.option(
    "--status", "-s", help="Status of the PR. (open, closed, merged)", default="open"
)
def list_prs(author: str | None, status: str) -> None:
    author_arn = author and str(
        UserArn.get_current_user()
        if author == "@me"
        else UserArn.get_from_username(author)
    )
    pr_ids: list[str] = (
        aws.cli.cmd("codecommit list-pull-requests")
        .optv("--repository-name", git.get_current_repository())
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
            aws.cli.cmd("codecommit get-pull-request")
            .optv("--pull-request-id", pr_id)
            .json()
            .pullRequest
        )
        pr_author = UserArn.parse(pr.authorArn)
        author_username = pr_author.username
        src = pr.pullRequestTargets[0].sourceReference.removeprefix("refs/heads/")
        dest = pr.pullRequestTargets[0].destinationReference.removeprefix("refs/heads/")
        table.add_row(
            Text(
                f"#{pr_id}",
                style={
                    "OPEN": "green",
                    "CLOSED": "red",
                    "MERGED": "purple",
                }[pr.pullRequestStatus],
            ),
            str(author_username),
            pr.title,
            f"{dest} <- {src}",
            humanize.naturaltime(datetime.fromisoformat(pr.lastActivityDate)),
            humanize.naturaltime(datetime.fromisoformat(pr.creationDate)),
        )
    print(table)
