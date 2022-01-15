#! /usr/bin/env python3.10

from pprint import pprint

# INFILE = 'd11p1t1.txt'
INFILE = 'd11p1.txt'

'''
* Octopus grid - each octopus has energy level from 0-9
* Steps:
  * Energy level of each octopus increases by 1
  * Any octopus with energy level > 9 flashes
    * This increases energy level of all adjacent octopuses by 1 including
      diagonally adjacent
    * If the above causes any octopus to have energy level > 9, it also flashes
    * Process continues as long as new octopuses have energy level > 9
    * But octopus can only flash once per step
  * Any octopus that flashed has energy level set to 0
'''
def flash(matrix, row, col):
    rows = len(matrix)
    cols = len(matrix[0])
    flashes = 1
    matrix[row][col] = 0

    # Recursively increment adjacent cells and look for flashes
    for adjrow in range(row - 1, row + 2):
        if 0 <= adjrow < rows:
            for adjcol in range(col - 1, col + 2):
                if 0 <= adjcol < cols:
                    if matrix[adjrow][adjcol] != 0:
                        matrix[adjrow][adjcol] += 1
                    if matrix[adjrow][adjcol] > 9:
                        flashes += flash(matrix, adjrow, adjcol)

    return flashes


def main(verbose=False):
    with open(INFILE) as infile:
        matrix = [[int(i) for i in line.strip()] for line in infile]

    # steps = 100
    steps = 1000
    flashes = 0
    all_flash = False
    # For each step - increment every value in matrix:
    for step in range(steps):
        if verbose:
            print(f'\nStep {step}, Matrix:')
            pprint(matrix)
        for row in matrix:
            for col in range(len(row)):
                row[col] += 1

        # Check for values > 9:
        for row in range(len(matrix)):
            for col in range(len(matrix[row])):
                if matrix[row][col] > 9:
                    flashes += flash(matrix, row, col)

        if not sum(sum(row) for row in matrix):
            all_flash = True
            break

        if verbose:
            print(f'Total flashes so far:  {flashes}')

    if all_flash:
        print(f'After {step + 1} steps, all octopuses flashed!')
    else:
        print(f'After {steps} steps, total flashes:  {flashes}')


if __name__ == '__main__':
    main()
