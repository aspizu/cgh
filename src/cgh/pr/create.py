import rich_click as click
from rich import print

from .. import aws, git, jira
from ..config import config


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
    head = head or git.get_current_branch()
    repo_name = git.get_current_repository()
    region = aws.get_current_repo_region()
    assert region is not None
    if config.jira is not None:
        try:
            ticket = jira.Ticket.from_pr_title(title)
            jira_link = f"[{ticket}]({ticket.url()})"
            body = f"{body}\n\n{jira_link}" if body else jira_link
        except ValueError, RuntimeError:
            ticket = None
    else:
        ticket = None
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
    pr_url = aws.get_pr_url(region, repo_name, pr_id)
    print(f"Created PR [green]#{pr_id}[/green] at {pr_url}")
    if ticket is None:
        return
    jira.cli.cmd("issue edit").args(str(ticket)).optv(
        "--custom", f"Pull-Request={pr_url}"
    ).run()
    print(f"Updated Jira issue [cyan]{ticket}[/cyan] at {ticket.url()}")
