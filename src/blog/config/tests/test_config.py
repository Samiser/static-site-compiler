import pytest
import json
from pathlib import Path
from blog.config import load_config, load_secrets, load_configuration
from blog.config.types import Config, Secrets


@pytest.fixture
def temp_config_file(tmp_path: Path) -> Path:
    config_data = {
        "templates": str(tmp_path / "templates"),
        "blogs": str(tmp_path / "blogs"),
        "static": str(tmp_path / "static"),
        "pages": str(tmp_path / "pages"),
    }
    config_path = tmp_path / "config.json"
    _: int = config_path.write_text(json.dumps(config_data))
    return config_path


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


def test_load_config(temp_config_file: Path):
    _: Config = load_config(temp_config_file)


def test_load_secrets(temp_secrets_file: Path):
    _: Secrets = load_secrets(temp_secrets_file)


def test_load_configuration(temp_config_file: Path, temp_secrets_file: Path):
    _: tuple[Config, Secrets] = load_configuration(temp_config_file, temp_secrets_file)
