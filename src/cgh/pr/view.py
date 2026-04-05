import json
from datetime import datetime
from typing import TYPE_CHECKING

import humanize
import rich_click as click
from rich import box
from rich.columns import Columns
from rich.console import Console
from rich.panel import Panel
from rich.rule import Rule
from rich.text import Text

from .. import aws, git
from ..aws import UserArn
from ..errors import Error
from ..jira import Ticket
from ..utils import open_browser

if TYPE_CHECKING:
    from ..json_object import JSONObject

console = Console()


def status_style(status: str) -> tuple[str, str]:
    """Return (label, style) based on PR status."""
    match status.upper():
        case "OPEN":
            return "OPEN", "bold green"
        case "MERGED":
            return "MERGED", "bold magenta"
        case "CLOSED":
            return "CLOSED", "bold red"
        case _:
            return status, "bold yellow"


def short_hash(commit: str, length: int = 7) -> str:
    return commit[:length]


def format_approval_rule(rule: JSONObject) -> Text:
    content = json.loads(rule.approvalRuleContent)
    statements = content.get("Statements", [])
    needed = statements[0].get("NumberOfApprovalsNeeded", "?") if statements else "?"

    t = Text()
    t.append(rule.approvalRuleName, style="bold white")
    t.append(f"  —  {needed} approval(s) needed", style="dim")
    return t


@click.command()
@click.argument("ID")
@click.option("--web", flag_value=True, help="Open pull request in web browser.")
@click.option(
    "--jira", flag_value=True, help="Open associated jira ticket in web browser."
)
def view(id: str, web: bool, jira: bool) -> None:
    pr_id = id.lstrip("#")
    region = aws.get_current_repo_region()
    assert region is not None

    if web:
        open_browser(aws.get_pr_url(region, git.get_current_repository(), pr_id))
        return

    pr = (
        aws.cli.cmd("codecommit get-pull-request")
        .optv("--pull-request-id", pr_id)
        .json()
        .pullRequest
    )

    try:
        ticket = Ticket.from_pr_title(pr.title)
        jira_url: str | None = ticket.url()
    except ValueError, RuntimeError:
        jira_url = None

    if jira:
        if jira_url is None:
            msg = f'The PR with title "{pr.title}" does not have a jira ticket.'
            raise Error(msg)
        open_browser(jira_url)
        return

    created = humanize.naturaltime(datetime.fromisoformat(pr.creationDate))
    updated = humanize.naturaltime(datetime.fromisoformat(pr.lastActivityDate))
    t = pr.pullRequestTargets[0]
    author_arn = UserArn.parse(pr.authorArn)

    src = t.sourceReference.removeprefix("refs/heads/")
    dest = t.destinationReference.removeprefix("refs/heads/")
    description = pr._.get("description") or ""
    status_label, status_style_str = status_style(pr.pullRequestStatus)

    title = Text()
    title.append(f"#{pr_id} ", style="bold dim")
    title.append(pr.title, style="bold white")
    title.append(f"  [{status_label}]", style=status_style_str)

    console.print()
    console.print(title)
    console.print(Rule(style="dim"))

    meta_items = [
        Text.assemble(("  Author  ", "dim"), (author_arn.username, "cyan bold")),
        Text.assemble(("  Branch  ", "dim"), (f"{dest} ← {src}", "yellow")),
        Text.assemble(("  Updated  ", "dim"), (updated, "white")),
        Text.assemble(("  Created  ", "dim"), (created, "white")),
    ]
    if jira_url:
        meta_items.append(
            Text.assemble(("  Jira  ", "dim"), (jira_url, "blue underline"))
        )
    console.print(Columns(meta_items, padding=(0, 2)))
    console.print(Rule(style="dim"))

    if description:
        console.print(
            Panel(
                description.strip(),
                title="[dim]Description[/dim]",
                border_style="dim",
                box=box.ROUNDED,
                padding=(1, 2),
            )
        )
    else:
        console.print(Text("  No description provided.", style="dim italic"))

    approval_rules = getattr(pr, "approvalRules", [])
    if approval_rules:
        console.print()
        console.print(Rule("[dim]Approval Rules[/dim]", style="dim"))
        for rule in approval_rules:
            console.print(format_approval_rule(rule))

    console.print()
