import rich_click as click

from ..command import aws


@click.command()
@click.option("--title", "-t", help="Title for pull request")
@click.option("--body", "-b", help="Body for the pull request")
@click.argument("ID")
def edit(id: str, title: str, body: str | None):
    pr_id = id.lstrip("#")
    if title:
        (
            aws.cmd("codecommit update-pull-request-title")
            .optv("--title", title)
            .optv("--pull-request-id", pr_id)
            .run()
        )
    if body:
        (
            aws.cmd("codecommit update-pull-request-description")
            .optv("--description", body)
            .optv("--pull-request-id", pr_id)
            .run()
        )
