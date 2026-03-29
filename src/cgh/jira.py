import re

from .config import config
from .errors import Error

pr_title_re = None
if config.jira:
    pr_title_re = re.compile(rf"^\s*{config.jira}-(\d+)")


def parse_pr_title(title: str) -> int | None:
    if pr_title_re is None:
        msg = "jira is not configured in your config file."
        raise Error(msg)
    m = pr_title_re.match(title)
    return m and int(m.group(1))


def get_work_item_url(id: int) -> str:
    if config.jira is None:
        msg = "jira is not configured in your config file."
        raise Error(msg)
    return f"{config.jira.url}/browse/{config.jira.key}-{id}"
