import json
from pathlib import Path

from .types import (
    Config,
    Secrets,
    LastFMSecrets,
    DiscogsSecrets,
    LetterboxdSecrets,
)


def load_config(path: Path) -> Config:
    with path.open() as f:
        raw_config: dict[str, str] = json.load(f)

    config: Config = Config(
        templates=Path(raw_config["templates"]),
        blogs=Path(raw_config["blogs"]),
        static=Path(raw_config["static"]),
        pages=Path(raw_config["pages"]),
    )

    print(f"Loaded config: {config}")
    return config


def load_secrets(path: Path) -> Secrets:
    with path.open() as f:
        raw_secrets: dict[str, dict[str, str]] = json.load(f)

    secrets: Secrets = Secrets(
        lastfm=LastFMSecrets(
            api_key=raw_secrets["lastfm"]["api_key"],
            shared_secret=raw_secrets["lastfm"]["shared_secret"],
        ),
        discogs=DiscogsSecrets(token=raw_secrets["discogs"]["token"]),
        letterboxd=LetterboxdSecrets(
            username=raw_secrets["letterboxd"]["username"],
            password=raw_secrets["letterboxd"]["password"],
        ),
    )
    print("Loaded secrets")
    return secrets


def load_configuration(config_path: Path, secrets_path: Path) -> tuple[Config, Secrets]:
    config = load_config(config_path)
    secrets = load_secrets(secrets_path)
    return config, secrets
