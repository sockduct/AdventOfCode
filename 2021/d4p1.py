#! /usr/bin/env python3.10

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

    def __repr__(self):
        output = ' B   I   N   G   O\n'
        for row in self.board:
            for num, stat in row.items():
                state = '* ' if stat else '  '
                output += f'{num:2}{state}'
            output += '\n'

        return output

    def drawn(self, number):
        'If number on board, mark as drawn (True)'
        ...

    def is_bingo(self):
        'Check each row and column to see if all members True'
        ...

def main():
    board = BingoBoard([list(range(1,6)), list(range(6,11)), list(range(11,16)),
                        list(range(21,26)), list(range(26,31))])
    print(board)

if __name__ == '__main__':
    main()
