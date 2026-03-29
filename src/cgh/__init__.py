import rich_click as click
from rich import print

from .errors import Error
from .pr import pr


class MainGroup(click.Group):
    def invoke(self, ctx: click.Context) -> object:
        try:
            return super().invoke(ctx)
        except Error as e:
            if ctx.obj and ctx.obj.get("verbose"):
                raise
            print(f"[red]Error:[/red] {e.message}")
            raise SystemExit(1) from None


@click.group(cls=MainGroup)
@click.option("--verbose", "-v", is_flag=True)
@click.pass_context
def main(ctx: click.Context, verbose: bool) -> None:
    ctx.ensure_object(dict)
    ctx.obj["verbose"] = verbose


main.add_command(pr)
