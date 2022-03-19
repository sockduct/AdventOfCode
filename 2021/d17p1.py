#! /usr/bin/env python3.10


# INFILE = 'd17p1t1.txt'
INFILE = 'd17p1.txt'
MAX_VELOCITY = 250


# Standard Library
from itertools import product
import re

# 3rd Party Library
from colorama import init, Fore, Style


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
        return f'<Launcher(x-pos={self.x}, y-pos={self.y}, x-vel={self.chg_x}, y-vel={self.chg_y})>'

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
        self.grid_init = False

    def __repr__(self):
        return (f'<Map({self.tx1=}, {self.tx2=}, {self.ty1=}, {self.ty2=}, {self.height=}, '
                f'{self.cols=}, {self.rows=})>')

    def __str__(self):
        if not self.grid_init:
            self.init_grid()
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
                self.set(col, abs(row - self.height), f'{Fore.LIGHTBLUE_EX}S{Style.RESET_ALL}')
            if self.ty1 <= row <= self.ty2 and self.tx1 <= col <= self.tx2:
                self.set(col, abs(row - self.height), f'{Fore.CYAN}T{Style.RESET_ALL}')
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

    def get(self, x, y):
        if not self.grid_init:
            self.init_grid()
        return self.grid[(self.cols * y) + x]

    def get_result(self):
        while True:
            # Initial coordinate already plotted, start with a step:
            self.launcher.step()
            col, row = self.launcher.coords
            row_check = abs(row - self.height)
            if col >= self.cols or row_check >= self.rows:
                break
            if self.ty1 <= row <= self.ty2 and self.tx1 <= col <= self.tx2:
                return True

        return False

    def init_grid(self):
        self.grid_init = True
        self._init_grid()
        self.overlay_trajectory()
        # Initialize colorama:
        init()

    def overlay_trajectory(self):
        while True:
            # Initial coordinate already plotted, start with a step:
            self.launcher.step()
            col, row = self.launcher.coords
            row = abs(row - self.height)
            if col >= self.cols or row >= self.rows:
                break
            if self.get(col, row) == f'{Fore.CYAN}T{Style.RESET_ALL}':
                self.set(col, row, f'{Fore.LIGHTGREEN_EX}#{Style.RESET_ALL}')
            else:
                self.set(col, row, f'{Fore.MAGENTA}#{Style.RESET_ALL}')

    def set(self, x, y, value):
        if not self.grid_init:
            self.init_grid()
        point = (self.cols * y) + x
        self.grid[point] = value


def xdist(n):
    '''Calculate n + n - 1 + n - 2 + ... + 2 + 1'''
    if n < 1:
        raise ValueError(f'n must be > 0, got {n}')
    return n + (n * (n - 1))//2


def calc_launch_limits(target):
    launch_limits = dict(xmin=0, xmax=target['x2'],
                         ymin=target['y1'], ymax=(abs(target['y1']) - 1))
    for x in range(1, target['x2'] + 1):
        if target['x1'] <= (xval := xdist(x)) <= target['x2']:
            if launch_limits['xmin'] == 0:
                launch_limits['xmin'] = x
                break
        elif xval > target['x2']:
            break

    return launch_limits


def main(verbose=False):
    # Testing:
    '''
    for x1, x2, y1, y2, l1, l2 in ((20, 30, -10, -5, 7, 2),
                                   (20, 30, -10, -5, 6, 3),
                                   (20, 30, -10, -5, 9, 0),
                                   (20, 30, -10, -5, 17, -4),
                                   (20, 30, -10, -5, 6, 9)):
        target = dict(x1=x1, x2=x2, y1=y1, y2=y2)
        launcher = Launcher(l1, l2)
        print(f'Launcher:  {launcher.chg_x}, {launcher.chg_y}')
        map = Map(target, launcher)
        print(f'{map}\n')
        # Reset values:
        launcher = Launcher(l1, l2)
        map = Map(target, launcher)
        print(f'Success:  {map.get_result()}')
    '''

    with open(INFILE) as infile:
        for line in infile:
            if (res := re.match(r'target area: x=(-?\d+)\.\.(-?\d+), y=(-?\d+)\.\.(-?\d+)', line)):
                x1, x2, y1, y2 = res.groups()
                break

    target = dict(x1=int(x1), x2=int(x2), y1=int(y1), y2=int(y2))
    '''
    Calculate resulting distance with initial velocity of x:
    x + x(x - 1)/2
    Use above to calculate x values within x1 - x2 target range

    Calculate max height:
    * Launch at +y, when comes back to 0 at -y, then goes -y - 1 down
      i.e., if launch at 10, at 0 goes -11 - so +y < y1
    Calculate min height:
    * Launch at -y, -y must be <= y1
    Calculate y values within y1 - y2 target range (Note:  y1 is lower)
    '''
    ### Need to come up with launch values:
    launch_limits = calc_launch_limits(target)
    launch_pairs = list(product(range(launch_limits['xmin'], launch_limits['xmax'] + 1),
                                range(launch_limits['ymin'], launch_limits['ymax'] + 1)))
    if verbose:
        print(f'Launch Pairs:  {launch_pairs}')
    print(f'Total Launch Pairs:  {len(launch_pairs)}')
    # for i, (x, y) in enumerate(launch_pairs):
    valid_pairs = []
    for x, y in launch_pairs:
        launcher = Launcher(x, y)
        if verbose:
            print(f'Launcher:  {launcher.chg_x}, {launcher.chg_y}')
        map = Map(target, launcher)
        res = map.get_result()
        if verbose:
            print(f'Success:  {res}')
        if res:
            valid_pairs.append((x, y))
        '''
        # Reset Values:
        if res:
            launcher = Launcher(x, y)
            map = Map(target, launcher)
            print(f'{map}\n')
        if i >= 50:
            break
        '''

    print(f'Found {len(valid_pairs)} valid launch pairs.')


if __name__ == '__main__':
    main()
