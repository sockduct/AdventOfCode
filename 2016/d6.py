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
def get_mcc_col(data: list[str], least: bool=False) -> str:
    word = []
    for col in range(len(data[0])):
        col_data = [row[col] for row in data]
        # Counter.most_common returns a list of tuples
        # Extract the character (first tuple element) from the first tuple:
        letter_freq = Counter(col_data).most_common()
        letter = letter_freq[-1][0] if least else letter_freq[0][0]
        word.append(letter)

    return ''.join(word)


def main() -> None:
    data: list[str] = []
    cwd = Path(__file__).parent
    with open(cwd/INFILE) as infile:
        data.extend(line.strip() for line in infile)

    # Part 1:
    # word = get_mcc_col(data)
    #
    # Part 2:
    word = get_mcc_col(data, least=True)
    print(f'Error-corrected message:  {word}')


if __name__ == '__main__':
    main()
