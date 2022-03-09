#! /usr/bin/env python3.10


MAX_VELOCITY = 250


'''
To do:
* Initial map isn't quite right - doesn't print last row
* Add starting point to map
* Add step function to Launcher
* Add plot function after stepping
* Add calculator to figure out trajectories
'''
class Launcher():
    def __init__(self, x, y):
        '''
        Submarine probe launcher
        x = initial forward velocity, integer, [0, MAX_VELOCITY]
        y = initial upward velocity (downward if negative), integer,
            [-MAX_VELOCITY, MAX_VELOCITY]

        Probe launched from (0, 0) - "ground level"

        Probe moves in steps - for each step:
        * probe's x position increases by its x velocity
        * probe's y position increases by its y velocity
        * Drag decreases the probe's velocity by 1 towards 0 (if velocity is
          negative then it increases to 0), velocity doesn't change once its 0
        * Gravity decreases probe's y velocity by 1

        Goal:  Have probe land within target area after any step
        '''
        # Original values:
        self.init_x = x
        self.init_y = y

        # Current values after stepping:
        self._x = x
        self._y = y

    def __repr__(self):
        return f'<Launcher({self.init_x=}, {self.init_y=}, {self.x=}, {self.y=})>'

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

    def __repr__(self):
        return (f'<Map({self.tx1=}, {self.tx2=}, {self.ty1=}, {self.ty2=}, {self.height=}, '
                f'{self.cols=}, {self.rows=})>')

    def __str__(self):
        col = 0
        matrix = ''
        for elmt in self.grid:
            matrix += elmt
            col += 1
            if col == self.cols:
                matrix += '\n'
                col = 0

        return f'{matrix}'

    '''
    This is the wrong approach
    ### Start at self.ty2, self.tx1 and fill out map from there...
    '''
    def _init_grid(self):
        self.grid = ['.'] * (self.cols * self.rows)
        row = self.height
        col = 0
        for _ in self.grid:
            if self.ty1 <= row <= self.ty2 and self.tx1 <= col <= self.tx2:
                self.set(col, abs(row - self.height), 'T')
            col += 1
            if col > self.cols:
                col = 0
                row -= 1

    def _init_height(self):
        height = max(self.launcher.y, 0)
        if height > 0:
            for i in range(1, height):
                height += i

        self.height = height

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
