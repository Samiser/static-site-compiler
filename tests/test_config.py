import pytest
import json
from pathlib import Path
from ssc.secrets import load_secrets
from ssc.secrets.types import Secrets


@pytest.fixture
def temp_secrets_file(tmp_path: Path) -> Path:
    secrets_data = {
        "lastfm": {"api_key": "test_api_key", "shared_secret": "test_shared_secret"},
        "discogs": {"token": "test_token"},
        "letterboxd": {"username": "test_user", "password": "test_pass"},
    }
    secrets_path = tmp_path / "secrets.json"
    _: int = secrets_path.write_text(json.dumps(secrets_data))
    return secrets_path


def test_load_secrets(temp_secrets_file: Path):
    _: Secrets = load_secrets(temp_secrets_file)
