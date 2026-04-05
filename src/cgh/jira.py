import re
from dataclasses import dataclass

from .command import Command
from .config import config

cli = Command.from_which("jira")

_pr_title_re = re.compile(rf"^\s*{config.jira}-(\d+)")


def ensure_jira() -> None:
    if config.jira is None:
        msg = "jira is not configured in your config file."
        raise RuntimeError(msg)


@dataclass
class Ticket:
    id: int

    @staticmethod
    def from_pr_title(title: str) -> Ticket:
        ensure_jira()
        m = _pr_title_re.match(title)
        if m is None:
            msg = f'The PR with title "{title}" does not have jira ticket.'
            raise ValueError(msg)
        return Ticket(int(m.group(1)))

    def __str__(self) -> str:
        ensure_jira()
        assert config.jira
        return f"{config.jira.key}-{self.id}"

    def url(self) -> str:
        ensure_jira()
        assert config.jira
        return f"{config.jira.url}/browse/{self}"
