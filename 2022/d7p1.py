#! /usr/bin/env python3


'''
No space left on device
* Input - terminal output
  * line starts with "$" = command
  * command cd = change directory, arg = <dir>|..|/
  * ls = list, output = dir <dir>|<#> <file>
* Determine total size of each directory (recursively add up file sizes)
  * e.g., in example:
    * e = 584, a = 94,853, d = 24,933,642, / = 48,381,165
* First find all directories with total size of at most 100,000
* Then calculate sum of their total sizes
  * e.g., in example:
    * a + e = 95,437
'''


# INFILE = 'd7p1t1.txt'
INFILE = r'\working\github\sockduct\aoc\2022\d7p1t1.txt'
# INFILE = 'd7p1.txt'
MAX_DIR_SIZE = 100_000


from pprint import pprint


class File:
    def __init__(self, name, size):
        self.name = name
        self.size = size

    def __repr__(self):
        return f'<File({self.name}, size={self.size:,})>'


def get_directory(tree, cwd):
    target_dir = None
    for entry in cwd:
        target_dir = target_dir[entry] if target_dir else tree[entry]
    return target_dir


def get_entries(target_dir, lines, index):
    '''
    ls output = dir <dir>|<#> <file>
        * <dir> = \w+
        # Where <#> is the size:
        * <#> = \d+
        * <file = \w+(?:\.\w+)?
    * end of output is another command (^$) or EOF
    '''
    while index < len(lines):
        match lines[index].split():
            case ['dir', dir_entry]:
                target_dir[dir_entry] = {}
            case [number, file_entry]:
                target_dir[file_entry] = int(number)
            case ['$', *command]:
                break
            case _:
                raise ValueError(f'Unexpected value:  {lines[index]}')

        index += 1

    return index


def main():
    '''
    Parsing lines:
    * ^$ = command
        * cd <dir>|..|/
        * ls
    * everything else = command output
    '''
    with open(INFILE) as infile:
        lines = infile.readlines()

    tree = {}
    cwd = None
    index = 0
    while index < len(lines):
        tokens = lines[index].split()
        match tokens:
            case ['$', 'cd', '/']:
                tree['/'] = {}
                cwd = ['/']
            case ['$', 'cd', '..']:
                _ = cwd.pop()
                if not cwd:
                    raise ValueError('cd .. goes "above" root')
            case ['$', 'cd', dir_entry]:
                cwd.append(dir_entry)
                target_dir = get_directory(tree, cwd)
            case ['$', 'ls']:
                target_dir = get_directory(tree, cwd)
                index = get_entries(target_dir, lines, index + 1)
                continue
            case _:
                raise ValueError(f'Unexpected value:  {tokens}')

        index += 1

    # Find total (recursive) size of each directory:
    # Find all directories first???
    ...

    # Discard all directories with size > MAX_DIR_SIZE:
    ...

    # Calculate sum of sizes of remaining directories:
    ...

    pprint(tree)


if __name__ == '__main__':
    main()
