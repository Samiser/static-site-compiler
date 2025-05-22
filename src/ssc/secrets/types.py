from typing import TypedDict


class LastFMSecrets(TypedDict):
    api_key: str
    shared_secret: str


class DiscogsSecrets(TypedDict):
    token: str


class LetterboxdSecrets(TypedDict):
    username: str
    password: str


class Secrets(TypedDict):
    lastfm: LastFMSecrets
    discogs: DiscogsSecrets
    letterboxd: LetterboxdSecrets
