# table2svg

A command-line utility to render tabular data to an SVG table.

## Usage

Print the usage info:

```shell
./table2svg.py -h
```

## Examples

For the [example CSV data](examples/example.csv):

```csv
Product,Component,Programming Language
Smart Box,Mobile APP,Swift
Smart Box,Front-end,JavaScript
Smart Box,Back-end,Golang
Smart Box,Data Persistent Service,"Golang, MySQL"
```

The following command generates the default output:

```shell
./table2svg.py examples/example.csv
```

![](examples/1.svg)

You can adjust the table style with the command-line options like
`--column_widths`, `--row_height`, `--font`, `--borders`, etc.:

```shell
./table2svg.py examples/example.csv --header_row --first_column --column_widths 200 200 400 --row_height 60 --font Serif --font_size 24 --borders horizontal
```

![](examples/2.svg)

You can also render a colorful SVG table, with the options like
`--background_color`, `--line_width`, `--line_color`, `--font_color`, etc.:

```shell
./table2svg.py examples/example.csv --background_color '#cef' --line_width 5 --line_color '#9cf' --font_color '#339'
```

![](examples/3.svg)
