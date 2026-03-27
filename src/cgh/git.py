from pathlib import Path

from .command import git


def get_current_repository() -> str:
    return Path(git.cmd("remote get-url origin").output()).name


def get_current_branch() -> str:
    return git.cmd("git branch --show-current").output()
