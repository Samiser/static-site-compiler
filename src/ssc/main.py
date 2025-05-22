#!/usr/bin/env python

from ssc.args import get_args
from ssc.site import build

from ssc.custom_pages import generate


def main():
    args = get_args()

    custom_pages = generate(args["config"], args["secrets"])

    build(args["config"], custom_pages, args["out"])


if __name__ == "__main__":
    main()
