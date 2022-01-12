#! /usr/bin/env python3.10

# INFILE = 'd10p1t1.txt'
INFILE = 'd10p1.txt'

'''
Rules:
* If a chunk opens with (, it must close with ).
* If a chunk opens with [, it must close with ].
* If a chunk opens with {, it must close with }.
* If a chunk opens with <, it must close with >.

Scoring:
): 3 points
]: 57 points
}: 1197 points
>: 25137 points
'''

VALID_OPEN = '([{<'
VALID_CLOSE = ')]}>'
SCORE = {')': 3, ']': 57, '}': 1197, '>': 25137}


def matching_pair(pair):
    match pair:
        case ('(', ')') | ('[', ']') | ('{', '}') | ('<', '>'):
            return True
        case _:
            return False


def get_match(char):
    match char:
        case '(':
            return ')'
        case '[':
            return ']'
        case '{':
            return '}'
        case '<':
            return '>'
        case _:
            return None


def main(verbose=False):
    dataset = []
    with open(INFILE) as infile:
        for line in infile:
            dataset.append(line.strip())

    stack = []
    score = 0
    status = dict(corrupt=0, incomplete=0, valid=0, total=0)

    for i, line in enumerate(dataset):
        valid = True
        for char in line:
            if char in VALID_OPEN:
                stack.append(char)
            elif char in VALID_CLOSE:
                top = stack.pop()
                if not matching_pair((top,char)):
                    if verbose:
                        print(f'Corrupted Line ({i}):  Expected {get_match(top)}, got {char}')
                    score += SCORE[char]
                    status['corrupt'] += 1
                    valid = False
                    break
        if valid:
            if stack:
                if verbose:
                    print(f'Line ({i}) incomplete!')
                status['incomplete'] += 1
                stack.clear()
            else:
                if verbose:
                    print(f'Line {i} valid')
                status['valid'] += 1
        status['total'] += 1


    for key, val in status.items():
        print(f'{key}:  {val}')
    print(f'Syntax error score:  {score}')


if __name__ == '__main__':
    main()
