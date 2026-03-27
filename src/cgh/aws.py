import re
from dataclasses import dataclass

from .command import aws
from .memoize import memoize


@memoize()
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
    if m is None:
        return None
    return UserArn(*m.groups())
