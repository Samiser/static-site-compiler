import json
from pathlib import Path

from .types import (
    Secrets,
    LastFMSecrets,
    DiscogsSecrets,
    LetterboxdSecrets,
)


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
