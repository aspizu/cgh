import rich_click as click
from rich import print

from .. import aws, jira
from ..aws import get_current_repo_region, get_pr_url
from ..config import config
from ..git import get_current_branch, get_current_repository


@click.command()
@click.option("--base", "-B", help="The branch into which you want your code merged")
@click.option("--body", "-b", help="Body for the pull request")
@click.option(
    "--head",
    "-H",
    help="The branch that contains commits for your pull request (defaults to current)",
)
@click.option("--title", "-t", help="Title for pull request", required=True)
def create(base: str | None, body: str | None, head: str | None, title: str) -> None:
    head = head or get_current_branch()
    repo_name = get_current_repository()
    region = get_current_repo_region()
    assert region is not None
    targets = f"repositoryName={repo_name}"
    targets += f",sourceReference={head}"
    targets += f",destinationReference={base}"
    pr_id = (
        aws.cli.cmd("codecommit create-pull-request")
        .optv("--title", title)
        .optv("--description", body)
        .optv("--targets", targets)
        .json()
        .pullRequest.pullRequestId
    )
    pr_url = get_pr_url(region, repo_name, pr_id)
    print(f"Created PR [green]#{pr_id}[/green] at {pr_url}")
    if config.jira is None:
        return
    ticket = jira.Ticket.from_pr_title(title)
    jira.cli.cmd("issue edit").args(str(ticket)).optv(
        "--custom", f"Pull-Request={pr_url}"
    ).run()
    print(f"Updated Jira issue [cyan]{ticket}[/cyan] at {ticket.url()}")
