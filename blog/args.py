import argparse

def _parse_args():
    parser = argparse.ArgumentParser(description="sam's cool static site compiler")
    parser.add_argument("--config", required=True, help="config file path")
    parser.add_argument("--secrets", required=True, help="secrets file path")
    parser.add_argument("--out", required=True, help="output directory")
    return parser.parse_args()

_args = None

def get_args():
    global _args
    if _args is None:
        _args = _parse_args()
    return _args
