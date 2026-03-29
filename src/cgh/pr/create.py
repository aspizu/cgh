import rich_click as click
from rich import print

from ..aws import get_current_repository_region, get_pr_url
from ..command import aws, jira_cli
from ..config import config
from ..errors import Error
from ..git import get_current_branch, get_current_repository
from ..jira import parse_pr_title


@click.command()
@click.option("--base", "-B", help="The branch into which you want your code merged")
@click.option("--body", "-b", help="Body for the pull request")
@click.option(
    "--head",
    "-H",
    help="The branch that contains commits for your pull request (defaults to current)",
)
@click.option("--title", "-t", help="Title for pull request", required=True)
def create(base: str | None, body: str | None, head: str | None, title: str):
    head = head or get_current_branch()
    repo_name = get_current_repository()
    region = get_current_repository_region()
    assert region is not None
    targets = f"repositoryName={repo_name}"
    targets += f",sourceReference={head}"
    targets += f",destinationReference={base}"
    pr_id = (
        aws.cmd("codecommit create-pull-request")
        .optv("--title", title)
        .optv("--description", body)
        .optv("--targets", targets)
        .json()
        .pullRequest.pullRequestId
    )
    pr_url = get_pr_url(region, repo_name, pr_id)
    print(f"Created PR [green]#{pr_id}[/green] at {pr_url}")
    issue_id = parse_pr_title(title)
    if issue_id is not None:
        if config.jira is None:
            msg = "jira is not configured in your config file."
            raise Error(msg)
        issue_key = f"{config.jira.key}-{issue_id}"
        jira_cli.cmd("issue edit").args(issue_key).optv(
            "--custom", f"Pull-Request={pr_url}"
        ).run()
        print(f"Updated Jira issue [cyan]{issue_key}[/cyan] Pull-Request field")
