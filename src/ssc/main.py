#!/usr/bin/env python

from ssc.args import get_args
from ssc.config import load_configuration
from ssc.site import build

from ssc.custom_pages import generate


def main():
    args = get_args()
    config, secrets = load_configuration(args["config"], args["secrets"])

    custom_pages = generate(config, secrets)

    build(config, custom_pages, args["out"])


if __name__ == "__main__":
    main()
