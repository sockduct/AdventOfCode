#! /usr/bin/env python3.10

# INFILE = 'd4p1.txt'
INFILE = 'd4p1t1.txt'

class BingoBoard():
    def __init__(self, data):
        '''
        data is a list of lists or ints (matrix):
        [[ 1,  2,  3,  4,  5],
         [ 6,  7,  8,  9, 10],
         [11, 12, 13, 14, 15],
         [16, 17, 18, 19, 20],
         [21, 22, 23, 24, 25]]
        '''
        #self.data = data
        self.board = []
        self.map = {}
        for row, cols in enumerate(data):
            self.board.append({num: False for num in cols})
            for col, num in enumerate(cols):
                self.map[num] = (row, col)

    # This is really a __str__ function, but convenient...
    def __repr__(self):
        output = (' B   I   N   G   O\n'
                  '===================\n')
        for row in self.board:
            for num, stat in row.items():
                state = '* ' if stat else '  '
                output += f'{num:2}{state}'
            output += '\n'

        return output

    def drawn(self, number):
        'If number on board, mark as drawn (True)'
        if number not in self.map:
            raise KeyError(f'Number ({number}) not on board')

        row, col = self.map[number]
        self.board[row][number] = True

    def is_bingo(self):
        'Check each row and column to see if all members True'
        for row in self.board:
            if all(row.values()):
                return True

        # Get an iterator for each row to allow iterating through columns:
        rowiters = [iter(row) for row in self.board]
        return any(all([next(rowiters[0]), next(rowiters[1]), next(rowiters[2]),
                    next(rowiters[3]), next(rowiters[4])]) for _ in range(5))

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

    counter = 0
    for num in drawn_numbers:
        counter += 1
        for board in boards:
            board.drawn(num)
            if counter >= 5 and board.is_bingo():
                print(board)
                return

if __name__ == '__main__':
    main()
