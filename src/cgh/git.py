from pathlib import Path

from .command import Command

cli = Command.from_which("git")


def get_current_repository() -> str:
    return Path(cli.cmd("remote get-url origin").output()).name


def get_current_branch() -> str:
    return cli.cmd("branch --show-current").output()
