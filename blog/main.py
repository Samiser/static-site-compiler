#!/usr/bin/env python

from blog.args import get_args
from blog.config import load_configuration
from blog.site import build
from blog.custom_pages import generate


def main():
    args = get_args()
    config, secrets = load_configuration(args["config"], args["secrets"])
    custom_pages = generate(secrets)
    build(config, custom_pages, args["out"])


if __name__ == "__main__":
    main()
