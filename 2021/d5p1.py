#! /usr/bin/env python3.10

from collections.abc import Iterable


INFILE = 'd5p1t1.txt'
# INFILE = 'd5p1.txt'

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
        self.grid = ['.'] * (rows * cols)

    def __repr__(self):
        return f'<Matrix({self.rows} X {self.cols})>'

    def __str__(self):
        col = 0
        matrix = ''
        for elmt in self.grid:
            matrix += str(elmt)
            col += 1
            if col == self.cols:
                matrix += '\n'
                col = 0
        return f'{matrix}'

    def inc(self, x, y):
        point = (self.rows * y) + x
        if self.grid[point] == '.':
            self.grid[point] = 0
        else:
            self.grid[point] += 1

def main():
    lines = []

    with open(INFILE) as ifile:
        for line in ifile:
            res = [pair.split(',') for pair in line.split('->')]
            lines.append(Line(points=res))

    maxx = max(line.maxx() for line in lines)
    maxy = max(line.maxy() for line in lines)
    matrix = Matrix(maxx, maxy)

    for line in lines:
        status = line.ishor() or line.isver()
        print(f'{line}, horizontal or vertical? {status}')

    for i in range(maxx):
        matrix.inc(i, i)
    for i in range(maxx):
        matrix.inc(i, i)
    print(matrix)

if __name__ == '__main__':
    main()
