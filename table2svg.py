#!/usr/bin/env python3
"""A command-line utility to render tabular data to an SVG table.
"""


from enum import Enum
import csv
import argparse
import sys


_verbose = False


_DEFAULT_TABLE_WIDTH = 960
_DEFAULT_ROW_HEIGHT = 40
_DEFAULT_LINE_WIDTH = 1
_DEFAULT_LINE_COLOR = '#000000'
_DEFAULT_FONT = 'sans-serif'
_DEFAULT_FONT_SIZE = 24
_DEFAULT_FONT_COLOR = '#000000'
_DEFAULT_BACKGROUND_COLOR = '#ffffff'
_MARGIN = 30


class _TextAlign(Enum):
    LEFT = 'left'
    CENTER = 'center'
    RIGHT = 'right'


def info(*args, **kwargs):
    if _verbose:
        print(*args, file=sys.stderr, **kwargs)


def render(csv_path, svg_path,
           header_row=False, first_column=False,
           row_height=_DEFAULT_ROW_HEIGHT, column_widths=[],
           line_width=_DEFAULT_LINE_WIDTH, line_color=_DEFAULT_LINE_COLOR,
           font=_DEFAULT_FONT, font_size=_DEFAULT_FONT_SIZE,
           font_color=_DEFAULT_FONT_COLOR, text_align=_TextAlign.CENTER,
           background_color=_DEFAULT_BACKGROUND_COLOR):
    output_fd = (open(svg_path, 'w', encoding='utf-8')
                 if svg_path else sys.stdout)
    def _out(*args, **kwargs):
        print(*args, file=output_fd, **kwargs)

    info(f'Loading {csv_path}')
    data = []
    with open(csv_path, 'r', encoding='utf-8') as csvfile:
        data_reader = csv.reader(csvfile, delimiter=',', quotechar='"')
        for row in data_reader:
            info('\t'.join(row))
            data.append(row)
    if len(data) <= 0 or len(data[0]) <=0:
        info(f'No data found in {csv_path}')
        return

    rows = len(data)
    cols = len(data[0])
    table_width = (line_width * (cols + 1) + sum(column_widths + _MARGIN * 2)
                   if column_widths else 960)
    table_height = line_width * (rows + 1) + row_height * rows + _MARGIN * 2

    _out(f'<svg viewBox="0 0 {table_width} {table_height}" '
         f'width="{table_width}" height="{table_height}" '
         f'style="background-color:{background_color}" '
         'xmlns="http://www.w3.org/2000/svg">')
    _out('</svg>')


def main():
    parser = argparse.ArgumentParser(
        description='A command-line utility to render tabular data to an SVG '
                    'table.',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument(
        'input', type=str, help='The input CSV file.')
    parser.add_argument(
        '-o', '--output', type=str, required=False,
        help='The output SVG file. '
             'If omitted, the output will be printed to the stdout.')
    parser.add_argument(
        '-v', '--verbose', action='store_true',
        help='Turn on the verbose mode.')
    parser.add_argument(
        '-r', '--header_row', action='store_true',
        help='The table has a row heading.')
    parser.add_argument(
        '-c', '--first_column', action='store_true',
        help='The table has a column heading.')
    parser.add_argument(
        '--row_height', type=int, default=_DEFAULT_ROW_HEIGHT,
        help='The height of the rows.')
    parser.add_argument(
        '--column_widths', type=int, nargs='*',
        help='The list of the column widths. If the list is empty or omitted, '
             f'the width of the output SVG will be {_DEFAULT_TABLE_WIDTH} and '
             'all the columns will share an average width.')
    parser.add_argument(
        '--line_width', type=int, default=_DEFAULT_LINE_WIDTH,
        help='The width of the table lines.')
    parser.add_argument(
        '--line_color', type=str, default=_DEFAULT_LINE_COLOR,
        help='The color of the table lines.')
    parser.add_argument(
        '--font', type=str, default=_DEFAULT_FONT,
        help='The text font.')
    parser.add_argument(
        '--font_size', type=int, default=_DEFAULT_FONT_SIZE,
        help='The text size, in pixels.')
    parser.add_argument(
        '--font_color', type=str, default=_DEFAULT_FONT_COLOR,
        help='The text color.')
    parser.add_argument(
        '--text_align', type=str,
        choices=[
            _TextAlign.LEFT.value,
            _TextAlign.CENTER.value,
            _TextAlign.RIGHT.value
        ],
        default=_TextAlign.CENTER,
        help='The text alignment.')
    parser.add_argument(
        '--background_color', type=str, default=_DEFAULT_BACKGROUND_COLOR,
        help='The background color of the output SVG.')
    args = parser.parse_args()
    global _verbose
    _verbose = args.verbose
    render(args.input, args.output,
           args.header_row, args.first_column,
           args.row_height, args.column_widths,
           args.line_width, args.line_color,
           args.font, args.font_size,
           args.font_color, _TextAlign(args.text_align),
           args.background_color)


if __name__ == '__main__':
    main()
