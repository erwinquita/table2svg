#!/usr/bin/env python3
"""A command-line utility to render tabular data to an SVG table.
"""


from enum import Enum
import csv
import argparse
import html
import sys


_verbose = False


_DEFAULT_TABLE_WIDTH = 960
_DEFAULT_ROW_HEIGHT = 40
_MIN_ROW_HEIGHT = 1
_MAX_ROW_HEIGHT = 999
_DEFAULT_COL_WIDTH = 100
_MIN_COLUMN_WIDTH = 1
_MAX_COLUMN_WIDTH = 999
_DEFAULT_LINE_WIDTH = 1
_MIN_LINE_WIDTH = 1
_MAX_LINE_WIDTH = 10
_DEFAULT_LINE_COLOR = '#000000'
_DEFAULT_FONT = 'sans-serif'
_DEFAULT_FONT_SIZE = 20
_MIN_FONT_SIZE = 1
_MAX_FONT_SIZE = 199
_DEFAULT_FONT_COLOR = '#000000'
_DEFAULT_BACKGROUND_COLOR = '#ffffff'
_MARGIN = 30
_PADDING = 5


class _TextAlign(Enum):
    LEFT = 'left'
    CENTER = 'center'
    RIGHT = 'right'


class _Borders(Enum):
    ALL = 'all'
    HORIZONTAL = 'horizontal'
    VERTICAL = 'vertical'
    INSIDE = 'inside'
    INSIDE_HORIZONTAL = 'inside_horizontal'
    INSIDE_VERTICAL = 'inside_vertical'
    NONE = 'none'


def _info(*args, **kwargs):
    if _verbose:
        print(*args, file=sys.stderr, **kwargs)


def _clamp(n, min_number, max_number):
    return max(min(max_number, n), min_number)


def render(csv_path, svg_path,
           header_row=False, first_column=False,
           row_height=_DEFAULT_ROW_HEIGHT, column_widths=[],
           line_width=_DEFAULT_LINE_WIDTH, line_color=_DEFAULT_LINE_COLOR,
           font=_DEFAULT_FONT, font_size=_DEFAULT_FONT_SIZE,
           font_color=_DEFAULT_FONT_COLOR, text_align=_TextAlign.CENTER,
           background_color=_DEFAULT_BACKGROUND_COLOR, borders=_Borders.ALL):
    row_height = _clamp(row_height, _MIN_ROW_HEIGHT, _MAX_ROW_HEIGHT)
    line_width = _clamp(line_width, _MIN_LINE_WIDTH, _MAX_LINE_WIDTH)
    font_size = _clamp(font_size, _MIN_FONT_SIZE, _MAX_FONT_SIZE)
    if column_widths:
        for i, width in enumerate(column_widths):
            column_widths[i] = _clamp(width,
                                      _MIN_COLUMN_WIDTH,
                                      _MAX_COLUMN_WIDTH)

    output_fd = (open(svg_path, 'w', encoding='utf-8')
                 if svg_path else sys.stdout)
    def _out(*args, **kwargs):
        print(*args, file=output_fd, **kwargs)

    _info(f'Loading {csv_path}')
    data = []
    with open(csv_path, 'r', encoding='utf-8-sig') as csvfile:
        data_reader = csv.reader(csvfile, delimiter=',', quotechar='"')
        for row in data_reader:
            _info('\t'.join(row))
            data.append(row)
    if len(data) <= 0 or len(data[0]) <=0:
        _info(f'No data found in {csv_path}')
        return

    rows = len(data)
    cols = len(data[0])
    if column_widths:
        while len(column_widths) < cols:
            column_widths.append(_DEFAULT_COL_WIDTH)
        table_width = line_width * (cols + 1) + sum(column_widths) + _MARGIN * 2
    else:
        table_width = 960
        column_widths = [(960 - 2 * _MARGIN - line_width * (cols + 1)) // cols
                         for x in range(cols)]
        column_widths[0] += (table_width - 2 * _MARGIN - line_width * (cols + 1)
                             - sum(column_widths))
    table_height = line_width * (rows + 1) + row_height * rows + _MARGIN * 2

    _info('Rendering SVG')

    _out(f'<svg viewBox="0 0 {table_width} {table_height}" '
         f'width="{table_width}" height="{table_height}" '
         'xmlns="http://www.w3.org/2000/svg">')
    _out(f'<rect x="{_MARGIN}" y="{_MARGIN}" '
         f'width="{table_width - 2 * _MARGIN}" '
         f'height="{table_height- 2 * _MARGIN}" '
         f'fill="{background_color}" stroke="none" />')

    horizontal_line_start = 0
    horizontal_line_end = rows
    vertical_line_start = 0
    vertical_line_end = cols
    if borders == _Borders.HORIZONTAL:
        vertical_line_end = -1
    elif borders == _Borders.VERTICAL:
        horizontal_line_end = -1
    elif borders == _Borders.INSIDE:
        horizontal_line_start += 1
        horizontal_line_end -= 1
        vertical_line_start += 1
        vertical_line_end -= 1
    elif borders == _Borders.INSIDE_HORIZONTAL:
        horizontal_line_start += 1
        horizontal_line_end -= 1
        vertical_line_end = -1
    elif borders == _Borders.INSIDE_VERTICAL:
        vertical_line_start += 1
        vertical_line_end -= 1
        horizontal_line_end = -1
    elif borders == _Borders.NONE:
        vertical_line_end = -1
        horizontal_line_end = -1
    for i in range(horizontal_line_start, horizontal_line_end + 1):
        x1 = _MARGIN + line_width // 2
        y1 = _MARGIN + line_width // 2 + i * (row_height + line_width)
        x2 = table_width - _MARGIN - line_width // 2 - 1
        y2 = _MARGIN + line_width // 2 + i * (row_height + line_width)
        _out(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" '
             f'stroke="{line_color}" stroke-width="{line_width}" '
             'stroke-linecap="square"/>')
    for i in range(vertical_line_start, vertical_line_end + 1):
        x1 = _MARGIN + line_width // 2 + sum(column_widths[:i]) + i * line_width
        y1 = _MARGIN + line_width // 2
        x2 = _MARGIN + line_width // 2 + sum(column_widths[:i]) + i * line_width
        y2 = table_height - _MARGIN - line_width // 2 - 1
        _out(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" '
             f'stroke="{line_color}" stroke-width="{line_width}" '
             'stroke-linecap="square"/>')

    for i, row in enumerate(data):
        for j, text in enumerate(row):
            left = _MARGIN + sum(column_widths[:j]) + (j + 1) * line_width
            width = column_widths[j]
            top = _MARGIN + i * (line_width + row_height) + line_width
            height = row_height
            y = top + height // 2 - font_size // 2
            if text_align == _TextAlign.LEFT:
                x = left + _PADDING
                anchor = 'start'
            elif text_align == _TextAlign.CENTER:
                x = left + width // 2
                anchor = 'middle'
            elif text_align == _TextAlign.RIGHT:
                x = left + width - _PADDING
                anchor = 'end'
            if (i == 0 and header_row) or (j == 0 and first_column):
                font_weight = "bold"
            else:
                font_weight = "normal"
            text = html.escape(text)
            _out(f'<text dominant-baseline="hanging" text-anchor="{anchor}" '
                 f'x="{x}" y="{y}" '
                 f'fill="{font_color}" font-family="{font}" '
                 f'font-size="{font_size}px" font-weight="{font_weight}">'
                 f'{text}</text>')

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
        help='Highlight the header row.')
    parser.add_argument(
        '-c', '--first_column', action='store_true',
        help='Highlight the first column.')
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
        help='The width of the border lines.')
    parser.add_argument(
        '--line_color', type=str, default=_DEFAULT_LINE_COLOR,
        help='The color of the border lines.')
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
            _TextAlign.RIGHT.value,
        ],
        default=_TextAlign.CENTER.value,
        help='The text alignment.')
    parser.add_argument(
        '--background_color', type=str, default=_DEFAULT_BACKGROUND_COLOR,
        help='The background color of the output table.')
    parser.add_argument(
        '--borders', type=str,
        choices=[
            _Borders.ALL.value,
            _Borders.HORIZONTAL.value,
            _Borders.VERTICAL.value,
            _Borders.INSIDE.value,
            _Borders.INSIDE_HORIZONTAL.value,
            _Borders.INSIDE_VERTICAL.value,
            _Borders.NONE.value,
        ],
        default=_Borders.ALL.value,
        help='How to draw the table borders.')
    args = parser.parse_args()
    global _verbose
    _verbose = args.verbose
    render(args.input, args.output,
           args.header_row, args.first_column,
           args.row_height, args.column_widths,
           args.line_width, args.line_color,
           args.font, args.font_size,
           args.font_color, _TextAlign(args.text_align),
           args.background_color, _Borders(args.borders))


if __name__ == '__main__':
    main()
