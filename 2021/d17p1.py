#! /usr/bin/env python3.10


MAX_VELOCITY = 250


'''
To do:
* Add calculator to figure out trajectories
'''
class Launcher():
    def __init__(self, x, y):
        '''
        Submarine probe launcher
        x = initial forward velocity, integer, [0, MAX_VELOCITY]
        y = initial upward velocity (downward if negative), integer,
            [-MAX_VELOCITY, MAX_VELOCITY]

        Probe launched from (0, 0) - "Starting point/ground level"

        See step function for details

        Goal:  Have probe land within target area after any step
        '''
        # Original values:
        self.orig_x = x
        self.orig_y = y

        # Increment/decrement values:
        self.chg_x = x
        self.chg_y = y

        # Initial/current values (changed by stepping):
        self._x = 0
        self._y = 0

    def __repr__(self):
        return f'<Launcher({self.x=}, {self.y=})>'

    @property
    def coords(self):
        return (self._x, self._y)

    '''
    Probe moves in steps - for each step:
    * probe's x position increases by its x velocity
    * probe's y position increases by its y velocity
    * Drag decreases the probe's velocity by 1 towards 0 (if velocity is
        negative then it increases to 0), velocity doesn't change once its 0
    * Gravity decreases probe's y velocity by 1
    '''
    def step(self):
        # Position change:
        self._x += self.chg_x
        self._y += self.chg_y

        # Drag and gravity:
        if self.chg_x > 0:
            self.chg_x -= 1
        elif self.chg_x < 0:
            self.chg_x += 1
        self.chg_y -= 1

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, value):
        self._x = value

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, value):
        self._y = value


class Map():
    def __init__(self, target, launcher):
        self.tx1 = target['x1']
        self.tx2 = target['x2']
        self.ty1 = target['y1']
        self.ty2 = target['y2']
        self.launcher = launcher
        self._init_height()
        self.cols = self.tx2 + 1
        self.rows = self.height + abs(self.ty1) + 1
        self._init_grid()
        self.overlay_trajectory()

    def __repr__(self):
        return (f'<Map({self.tx1=}, {self.tx2=}, {self.ty1=}, {self.ty2=}, {self.height=}, '
                f'{self.cols=}, {self.rows=})>')

    def __str__(self):
        col = 0
        height = self.height
        header1 = '{}         '
        header2 = '0123456789'
        row_label_width = '   '  # Spaces match zero-padding number after height below
        header_multiple = self.cols//len(header2)
        header_trailer = self.cols % len(header2)

        # Header row 1:
        matrix = f'{row_label_width}'
        for section in range(header_multiple + 1):
            header = header1.format(' ') if section == 0 else header1.format(section)
            matrix += f'{header}'

        # Header row 2:
        matrix += f'\n{row_label_width}'
        matrix += f'{header2}' * header_multiple + header2[:header_trailer]
        matrix += '\n'

        # Col prefix + rows:
        for elmt in self.grid:
            if col == 0:
                matrix += f'{height: 3}'
            matrix += elmt
            col += 1
            if col == self.cols:
                height -= 1
                matrix += '\n'
                col = 0

        return f'{matrix}'

    def _init_grid(self):
        self.grid = ['.'] * (self.cols * self.rows)
        row = self.height
        col = 0
        for _ in self.grid:
            if row == 0 and col == 0:
                self.set(col, abs(row - self.height), 'S')
            if self.ty1 <= row <= self.ty2 and self.tx1 <= col <= self.tx2:
                self.set(col, abs(row - self.height), 'T')
            col += 1
            if col == self.cols:
                col = 0
                row -= 1

    def _init_height(self):
        height = max(self.launcher.orig_y, 0)
        if height > 0:
            for i in range(1, height):
                height += i

        self.height = height

    def overlay_trajectory(self):
        while True:
            # Initial coordinate already plotted, start with a step:
            self.launcher.step()
            col, row = self.launcher.coords
            row = abs(row - self.height)
            if col >= self.cols or row >= self.rows:
                break
            self.set(col, row, '#')

    def set(self, x, y, value):
        point = (self.cols * y) + x
        self.grid[point] = value


def main():
    target = dict(x1=20, x2=30, y1=-10, y2=-5)
    launcher = Launcher(7, 2)
    map = Map(target, launcher)
    print(map)


if __name__ == '__main__':
    main()
