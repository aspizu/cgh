from pathlib import Path

import msgspec

_config_path = Path("~/.config/cgh/config.toml").expanduser()


class Jira(msgspec.Struct):
    url: str
    key: str


class Config(msgspec.Struct):
    jira: Jira | None = None

    @staticmethod
    def load() -> Config:
        try:
            with _config_path.open("rb") as f:
                return msgspec.toml.decode(f.read(), type=Config)
        except FileNotFoundError:
            return Config()

    def save(self) -> None:
        _config_path.parent.mkdir(parents=True, exist_ok=True)
        with _config_path.open("wb") as f:
            f.write(msgspec.toml.encode(self))


config = Config.load()
