from datetime import datetime

import humanize
import rich_click as click
from rich import box
from rich.columns import Columns
from rich.console import Console
from rich.panel import Panel
from rich.rule import Rule
from rich.text import Text

from ..aws import get_current_repository_region, get_pr_url, parse_user_arn
from ..command import aws
from ..git import get_current_repository
from ..utils import open_browser

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


@click.command()
@click.argument("ID")
@click.option("--web", flag_value=True, help="Open pull request in web browser.")
def view(id: str, web: bool):
    pr_id = id.lstrip("#")
    region = get_current_repository_region()
    assert region is not None

    if web:
        open_browser(get_pr_url(region, get_current_repository(), pr_id))
        return

    pr = (
        aws.cmd("codecommit get-pull-request")
        .optv("--pull-request-id", pr_id)
        .json()
        .pullRequest
    )

    created = humanize.naturaltime(datetime.fromisoformat(pr.creationDate))
    updated = humanize.naturaltime(datetime.fromisoformat(pr.lastActivityDate))
    t = pr.pullRequestTargets[0]
    author_arn = parse_user_arn(pr.authorArn)
    assert author_arn is not None

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

    console.print()
