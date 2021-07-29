#!/usr/bin/env python3
"""A command-line utility to render tabular data to an SVG table.
"""


import csv
import argparse
import sys


def info(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)


def render(csv_path, svg_path):
    info(f'Loading {csv_path}')


def main():
    parser = argparse.ArgumentParser(
        description=('A command-line utility to render tabular data to an SVG '
                     'table.'))
    parser.add_argument(
        'input', type=str, help='The input CSV file.')
    parser.add_argument(
        '-o', '--output', type=str, required=False,
        help=('The output SVG file. '
              'If omitted, the output will be printed to the stdout.'))
    args = parser.parse_args()
    render(args.input, args.output)


if __name__ == '__main__':
    main()
