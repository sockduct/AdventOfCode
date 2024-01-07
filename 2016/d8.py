#! /usr/bin/env python3


'''
Decode a series of instructions
* Screen is 50 x 6, all positions start off
* Three operations:
    * rect AxB - turns on all of the pixels in a rectangle at the top-left of the
      screen which is A wide and B tall.
    * rotate row y=A by B - shifts all of the pixels in row A (0 is the top row)
      right by B pixels. Pixels that would fall off the right end appear at the
      left end of the row.
    * rotate column x=A by B - shifts all of the pixels in column A (0 is the
      left column) down by B pixels. Pixels that would fall off the bottom appear
      at the top of the column.
'''


INFILE = 'd8.txt'
# INFILE = 'd8t1.txt'


# Libraries:
from pathlib import Path

# Local:
from grid import Grid


# Module:
def get_gridsize(commands: list[str]) -> tuple[int, int]:
    max_x = 2
    max_y = 2
    for cmd in commands:
        match cmd.split():
            case ['rect', size]:
                x, y = map(int, size.split('x'))
                # Add 1 as want grid to be at least 1 bigger than needed:
                if x + 1 > max_x:
                    max_x = x + 1
                if y + 1 > max_y:
                    max_y = y + 1
            case ['rotate', 'row', rownum, 'by', num]:
                row = int(rownum.split('=')[1])
                if row + 1 > max_y:
                    max_y = row + 1
            case ['rotate', 'column', colnum, 'by', num]:
                col = int(colnum.split('=')[1])
                if col + 1 > max_x:
                    max_x = col + 1
            case _:
                raise ValueError(f'Unexpected command:  {line}')

    return max_x, max_y


def parse_cmd(line: str, grid: Grid) -> None:
    match line.split():
        case ['rect', size]:
            x, y = map(int, size.split('x'))
            # Zero-based, so subtract 1 from x and y:
            grid.on((0, 0), (x - 1, y - 1))
        case ['rotate', 'row', rownum, 'by', num]:
            row = int(rownum.split('=')[1])
            amount = int(num)
            grid.rotate_row(row, amount)
        case ['rotate', 'column', colnum, 'by', num]:
            col = int(colnum.split('=')[1])
            amount = int(num)
            grid.rotate_col(col, amount)
        case _:
            raise ValueError(f'Unexpected command:  {line}')


def main(verbose: bool=True) -> None:
    commands = []
    cwd = Path(__file__).parent
    with open(cwd/INFILE) as infile:
        commands.extend(line.strip() for line in infile)

    # Hard code for initial test, then auto-detect:
    # grid = Grid(7, 3)
    cols, rows = get_gridsize(commands)
    if verbose:
        print(f'Based on commands, {cols} x {rows} grid will be created.')
    grid = Grid(cols, rows)

    for cmd in commands:
        parse_cmd(cmd, grid)
        if verbose:
            print(grid)

    print(f'Number of lit pixels:  {grid.status()[0]:,}')


if __name__ == '__main__':
    main()
