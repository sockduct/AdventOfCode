#! /usr/bin/env python3.10

from collections.abc import Iterable


# INFILE = 'd5p1t1.txt'
INFILE = 'd5p1.txt'

class Line():
    def __init__(self, x1=0, y1=0, x2=0, y2=0, *, points=None):
        if points and isinstance(points, Iterable):
            (x1, y1), (x2, y2) = points
        self.x1 = int(x1)
        self.y1 = int(y1)
        self.x2 = int(x2)
        self.y2 = int(y2)

    def __repr__(self):
        return f'<Line{{({self.x1}, {self.y1}), ({self.x2}, {self.y2})}}>'

    def __str__(self):
        return f'{{({self.x1}, {self.y1}), ({self.x2}, {self.y2})}}'

    def end(self):
        return (self.x2, self.y2)

    def ishor(self):
        return self.y1 == self.y2

    def isver(self):
        return self.x1 == self.x2

    def maxx(self):
        return max(self.x1, self.x2)

    def maxy(self):
        return max(self.y1, self.y2)

    def minx(self):
        return min(self.x1, self.x2)

    def miny(self):
        return min(self.y1, self.y2)

    def start(self):
        return (self.x1, self.y1)

class Matrix():
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        # self.grid = ['.'] * (rows * cols)
        self.grid = [0] * (rows * cols)

    def __repr__(self):
        return f'<Matrix({self.rows} X {self.cols})>'

    def __str__(self):
        col = 0
        matrix = ''
        for elmt in self.grid:
            if elmt == 0:
                elmt = '.'
            matrix += str(elmt)
            col += 1
            if col == self.cols:
                matrix += '\n'
                col = 0
        return f'{matrix}'

    def geval(self, val):
        'Find number of points greater than or equal to val'
        return sum(num >= val for num in self.grid)

    def inc(self, x, y):
        'Increment point (x, y) - e.g., 0 -> 1 -> 2 -> ...'
        point = (self.rows * y) + x
        '''
        if self.grid[point] == '.':
            self.grid[point] = 1
        else:
            self.grid[point] += 1
        '''
        self.grid[point] += 1

def test_matrix(matrix, lines):
    for line in lines:
        status = line.ishor() or line.isver()
        print(f'{line}, horizontal or vertical? {status}')

    for i in range(matrix.rows):
        matrix.inc(i, i)
    for i in range(matrix.rows):
        matrix.inc(i, i)
    print(matrix)

def main(verbose=False):
    lines = []

    with open(INFILE) as ifile:
        for line in ifile:
            res = [pair.split(',') for pair in line.split('->')]
            lines.append(Line(points=res))

    maxx = max(line.maxx() for line in lines) + 1
    maxy = max(line.maxy() for line in lines) + 1
    matrix = Matrix(maxx, maxy)

    # test_matrix(matrix, lines)

    for line in lines:
        if line.ishor():
            if verbose:
                print(f'Processing horiztonal line {line}')
            x1, x2 = (line.x1, line.x2) if line.x2 >= line.x1 else (line.x2, line.x1)
            for pos in range(x1, x2 + 1):
                matrix.inc(pos, line.y1)
        elif line.isver():
            if verbose:
                print(f'Processing vertical line {line}')
            y1, y2 = (line.y1, line.y2) if line.y2 >= line.y1 else (line.y2, line.y1)
            for pos in range(y1, y2 + 1):
                matrix.inc(line.x1, pos)
        else:
            if verbose:
                print(f'Skipping {line}...')

    print('Result:')
    if verbose:
        print(matrix)
    print(f'Points of 2 or more intersecting lines:  {matrix.geval(2)}')

if __name__ == '__main__':
    main()
