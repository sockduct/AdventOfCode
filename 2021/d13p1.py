#! /usr/bin/env python3.10


from multiprocessing.sharedctypes import Value


INFILE = 'd13p1t1.txt'
# INFILE = 'd13p1.txt'


class Matrix():
    def __init__(self, x, y):
        self._x = x + 1
        self._y = y + 1
        self._matrix = [['.'] * self._x for _ in range(self._y)]

    def __repr__(self):
        return f'<Matrix({self._x}, {self._y})>'

    def __str__(self):
        return ''.join(' '.join(row) + '\n' for row in self._matrix)

    def add_coords(self, coords):
        for x, y in coords:
            self._matrix[y][x] = '#'

    def count(self):
        return sum(x == '#' for row in self._matrix for x in row)

    def fold(self, folds):
        for axis, line in folds:
            if axis == 'x':
                # Sanity check
                for row in self._matrix:
                    if row[line] == '#':
                        raise ValueError('Attempted fold on non-empty line')
                    row[line] = '|'
                print(f'Current:\n{self}\n')

                '''
                Finish fold values and reset x below...
                '''
                # Fold values in:
                for left_col, right_col in enumerate(range(self._x - 1, line, -1)):
                    for y, val in enumerate(self._matrix):
                        if val == '#':
                            ...

                # Reset x:
            elif axis == 'y':
                # Sanity check
                if '#' in self._matrix[line]:
                    raise ValueError('Attempted fold on non-empty line')
                self._matrix[line] = ['-'] * self._x
                print(f'Current:\n{self}\n')

                # Fold values in
                for top_row, bottom_row in enumerate(range(self._y - 1, line, -1)):
                    for x, val in enumerate(self._matrix[bottom_row]):
                        if val == '#':
                            self._matrix[top_row][x] = val

                # Remove lines from fold down:
                for row in range(self._y - 1, line - 1, -1):
                    del self._matrix[row]

                # Reset y:
                self._y = line
            else:
                raise ValueError('Unexpected value:  {axis} - expecting x or y')


def main():
    max_x = 0
    max_y = 0
    coords = []
    folds = []
    with open(INFILE) as infile:
        for line in infile:
            if ',' in line:
                x, y = map(int, line.strip().split(','))
                if x > max_x:
                    max_x = x
                if y > max_y:
                    max_y = y
                coords.append((x, y))
            elif '=' in line:
                _, _, val = line.strip().split()
                axis, line = val.split('=')
                folds.append((axis, int(line)))
            elif line.strip() != '':
                raise ValueError('Unexpected values in input:  {line}')

    matrix = Matrix(max_x, max_y)
    matrix.add_coords(coords)
    print(matrix)
    matrix.fold(folds)
    print(matrix)
    print(f'Matrix count:  {matrix.count()}')


if __name__ == '__main__':
    main()
