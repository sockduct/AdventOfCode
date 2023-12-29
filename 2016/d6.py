#! /usr/bin/env python3


'''
Repetition codes
* Look at each column and find the most common character
'''


INFILE = 'd6.txt'
# INFILE = 'd6t1.txt'


# Libraries
from collections import Counter
from pathlib import Path


# Module
def get_mcc_col(data: list[str]) -> str:
    word = []
    for col in range(len(data[0])):
        col_data = [row[col] for row in data]
        # Counter.most_common returns a list of tuples
        # Extract the character (first tuple element) from the first tuple:
        word.append(Counter(col_data).most_common(1)[0][0])

    return ''.join(word)


def main() -> None:
    data = []
    cwd = Path(__file__).parent
    with open(cwd/INFILE) as infile:
        data.extend(line.strip() for line in infile)

    word = get_mcc_col(data)
    print(f'Error-corrected message:  {word}')


if __name__ == '__main__':
    main()
