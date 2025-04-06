import argparse
from typing import TypedDict, cast
from pathlib import Path


class Args(TypedDict):
    config: Path
    secrets: Path
    out: Path


def _parse_args() -> Args:
    parser = argparse.ArgumentParser(description="sam's cool static site compiler")
    _ = parser.add_argument("--config", required=True, help="config file path")
    _ = parser.add_argument("--secrets", required=True, help="secrets file path")
    _ = parser.add_argument("--out", required=True, help="output directory")
    args: argparse.Namespace = parser.parse_args()

    return Args(
        config=Path(cast(str, args.config)),
        secrets=Path(cast(str, args.secrets)),
        out=Path(cast(str, args.out)),
    )


_args = None


def get_args() -> Args:
    global _args
    if _args is None:
        _args = _parse_args()
    return _args
