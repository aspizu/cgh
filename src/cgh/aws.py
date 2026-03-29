import re
from dataclasses import dataclass

from .command import aws, git


def get_user_arn(username: str | None = None) -> str:
    return aws.cmd("iam get-user").optv("--user-name", username).json().User.Arn


@dataclass
class UserArn:
    id: str
    role: str
    username: str


arn_re = re.compile(r"^arn:aws:iam::(.*?):(.*?)/(.*?)$")


def parse_user_arn(user_arn: str) -> UserArn | None:
    m = arn_re.match(user_arn)
    return m and UserArn(*m.groups())


def get_pr_url(
    region: str,
    repository: str,
    pull_request_id: str,
):
    return f"https://{region}.console.aws.amazon.com/codesuite/codecommit/repositories/{repository}/pull-requests/{pull_request_id}/details"


region_re = re.compile(r"^https://git-codecommit\.(.*?)\.amazonaws.com/v1/repos/(.*?)$")


def get_current_repository_region() -> str | None:
    m = region_re.match(git.cmd("remote get-url origin").output())
    return m and m.group(1)
