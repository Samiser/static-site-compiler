import argparse
from typing import TypedDict, cast
from pathlib import Path

from ssc.secrets.types import Secrets
from ssc.secrets import load_secrets
from ssc.config.types import Config
from ssc.config import create_config


class Args(TypedDict):
    config: Config
    secrets: Secrets
    out: Path


def _parse_args() -> Args:
    parser = argparse.ArgumentParser(description="sam's cool static site compiler")
    _ = parser.add_argument("--pages", required=True, help="pages directory")
    _ = parser.add_argument("--blog-posts", required=True, help="blog post directory")
    _ = parser.add_argument("--secrets", required=True, help="secrets file path")
    _ = parser.add_argument("--out", required=True, help="output directory")
    args: argparse.Namespace = parser.parse_args()

    config = create_config(
        Path(cast(str, args.blog_posts)), Path(cast(str, args.pages))
    )

    secrets = load_secrets(Path(cast(str, args.secrets)))

    return Args(
        config=config,
        secrets=secrets,
        out=Path(cast(str, args.out)),
    )


_args = None


def get_args() -> Args:
    global _args
    if _args is None:
        _args = _parse_args()
    return _args
