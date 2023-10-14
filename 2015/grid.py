#! /usr/bin/env python3


'''
Simple grid class
'''


from collections import namedtuple


class Grid:
    def __init__(self, x, y, val=bool):
        self.x = x
        self.y = y
        if val.__name__ == 'bool':
            self.simple = True
            default_init = (True, False, lambda x: not x)
        elif val.__name__ == 'int':
            self.simple = False
            default_init = (1, 0, 2)
        else:
            raise ValueError(f'Expected val of bool|int, got "{val.__name__}"')

        self.vals = namedtuple('Values', 'on off toggle', defaults=default_init)()
        self.grid = [[self.vals.off for _ in range(x)] for _ in range(y)]

    def __repr__(self):
        return f'Grid({self.x}, {self.y})'

    def __str__(self):
        # Limit to first 10x10
        xover = False
        yover = False

        if self.x > 10:
            x = 10
            xover = True
        else:
            x = self.x

        if self.y > 10:
            y = 10
            yover = True
        else:
            y = self.y

        out = ''
        for row in range(y):
            for col in range(x):
                out += f'{int(self.grid[row][col])}'
            if xover:
                out += '...'
            out += '\n'

        if yover:
            out += '...\n'

        return out

    def status(self):
        enabled = sum(sum(row) for row in self.grid)
        disabled = self.x * self.y - enabled

        return enabled, disabled

    def update(self, p1, p2, op):
        match op:
            case 'on':
                if self.simple:
                    alt = False
                    val = self.vals.on
                else:
                    alt = True
                    val = lambda x: x + self.vals.on
            case 'off':
                if self.simple:
                    alt = False
                    val = self.vals.off
                else:
                    alt = True
                    val = lambda x: x - 1 if x > 1 else 0
            case 'toggle':
                alt = True
                val = self.vals.toggle if self.simple else (lambda x: x + 2)
            case _:
                raise ValueError(f'Expected on|off|toggle, got "{op}"')

        if isinstance(p1, (list, tuple)):
            for y in range(p1[1], p2[1] + 1):
                for x in range (p1[0], p2[0] + 1):
                    self.grid[y][x] = val(self.grid[y][x]) if alt else val
        else:
            self.grid[p2][p1] = val(self.grid[p2][p1]) if alt else val

    def on(self, p1, p2):
        self.update(p1, p2, 'on')

    def off(self, p1, p2):
        self.update(p1, p2, 'off')

    def toggle(self, p1, p2):
        self.update(p1, p2, 'toggle')
