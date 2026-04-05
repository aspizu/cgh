import re
from dataclasses import dataclass

from . import git
from .command import Command

cli = Command.from_which("aws")


def get_user_arn(username: str | None = None) -> str:
    return cli.cmd("iam get-user").optv("--user-name", username).json().User.Arn


_user_arn_re = re.compile(r"^arn:aws:iam::(.*?):(.*?)/(.*?)$")


@dataclass
class UserArn:
    id: str
    role: str
    username: str

    @staticmethod
    def parse(user_arn: str) -> UserArn:
        m = _user_arn_re.match(user_arn)
        if m is None:
            msg = f"Invalid user ARN: {user_arn}"
            raise ValueError(msg)
        return UserArn(*m.groups())

    @staticmethod
    def get_from_username(username: str) -> UserArn:
        arn = cli.cmd("iam get-user").optv("--user-name", username).json().User.Arn
        return UserArn.parse(arn)

    @staticmethod
    def get_current_user() -> UserArn:
        arn = cli.cmd("iam get-user").json().User.Arn
        return UserArn.parse(arn)

    def __str__(self) -> str:
        return f"arn:aws:iam::{self.id}:{self.role}/{self.username}"


def get_pr_url(region: str, repo_name: str, pr_id: str) -> str:
    return f"https://{region}.console.aws.amazon.com/codesuite/codecommit/repositories/{repo_name}/pull-requests/{pr_id}/details"


_repo_region_re = re.compile(
    r"^https://git-codecommit\.(.*?)\.amazonaws.com/v1/repos/(.*?)$"
)


def get_current_repo_region() -> str | None:
    m = _repo_region_re.match(git.cli.cmd("remote get-url origin").output())
    return m and m.group(1)
