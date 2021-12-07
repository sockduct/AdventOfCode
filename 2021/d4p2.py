#! /usr/bin/env python3.10

INFILE = 'd4p1.txt'
# INFILE = 'd4p1t1.txt'

class BingoBoard():
    def __init__(self, data):
        '''
        data is a list of lists of ints (matrix):
        [[ 1,  2,  3,  4,  5],
         [ 6,  7,  8,  9, 10],
         [11, 12, 13, 14, 15],
         [16, 17, 18, 19, 20],
         [21, 22, 23, 24, 25]]
        '''
        self.board = []
        self.map = {}
        for row, cols in enumerate(data):
            self.board.append({num: False for num in cols})
            # Only need row number not column number because rows are dicts
            # accessed via key (number - which we already have):
            for num in cols:
                self.map[num] = row

    def __repr__(self):
        first = next(iter(self.board[0]))
        middle = [i for i in self.board[2]].pop(2)
        last = [i for i in self.board[4]].pop()
        return f'<BingoBoard([[{first}, ... {middle}, ... {last}]])>'

    def __str__(self):
        output = (' B   I   N   G   O\n'
                  '===================\n')
        for row in self.board:
            for num, stat in row.items():
                state = '* ' if stat else '  '
                output += f'{num:2}{state}'
            output += '\n'

        return output

    def count(self):
        'Specific to challenge - calculate sum of all unmarked (False) numbers'
        total = 0

        for row in self.board:
            for key, val in row.items():
                if not val:
                    total += key

        return total

    def drawn(self, number, verbose=False):
        'If number on board, mark as drawn (True)'
        '''
        # Avoid since in real Bingo, a number can be drawn which isn't on
        # a particular playing board:
        if number not in self.map:
            raise KeyError(f'Number ({number}) not on board')
        '''
        if number not in self.map:
            if verbose:
                print(f'Warning:  Number ({number}) not on board')
            return

        row = self.map[number]
        self.board[row][number] = True

    def is_bingo(self):
        'Check each row and column to see if all members True'
        for row in self.board:
            if all(row.values()):
                return True

        # Get an iterator for each row to allow iterating through columns:
        # Alternatively, could use numpy.array which allows accessing
        # columns via self.board[:,col]
        rowiters = [iter(row) for row in self.board]
        for _ in range(5):
            col = [self.board[row][next(key)] for row, key in enumerate(rowiters)]
            if all(col):
                return True

        return False

def test_board():
    board = BingoBoard([list(range(1,6)), list(range(6,11)), list(range(11,16)),
                        list(range(21,26)), list(range(26,31))])
    print(board)

def main():
    boards = []
    buffer = []
    with open(INFILE) as ifile:
        drawn_numbers = map(int, ifile.readline().strip().split(','))

        counter = 0
        for line in ifile:
            if line.strip() == '':
                continue
            buffer.append([int(i) for i in line.split()])
            counter += 1
            if counter == 5:
                boards.append(BingoBoard(buffer))
                counter = 0
                buffer.clear()

    counter = 0
    boards_left = len(boards)
    purge = []
    for num in drawn_numbers:
        counter += 1
        purge.sort(reverse=True)
        for target in purge:
            boards.pop(target)
        purge.clear()
        for index, board in enumerate(boards):
            board = boards[index]
            board.drawn(num)
            '''
            if counter >= 5:
                print(f'Number drawn:  {num}\nBoard:\n{board}')
            '''
            if counter >= 5 and board.is_bingo():
                boards_left -= 1
                purge.append(index)
                if boards_left == 0:
                    print(f'Winning Board:\n{board}\nScore:  {board.count() * num}')
                    return

if __name__ == '__main__':
    main()
