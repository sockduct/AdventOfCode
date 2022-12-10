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
# INFILE = r'\working\github\sockduct\aoc\2022\d7p1t1.txt'
INFILE = 'd7p1.txt'
MAX_DIR_SIZE = 100_000


import json


def directory_sizes(tree, directories=None, cwd=None):
    if not directories:
        directories = {}
    if not cwd:
        cwd = []
    for key, value in tree.items():
        if isinstance(value, dict):
            directories[key] = 0
            cwd.append(key)
            directory_sizes(tree[key], directories, cwd)
            cwd.pop()
            if cwd:
                directories[cwd[-1]] += directories[key]
        elif isinstance(value, int):
            directories[cwd[-1]] += value
        else:
            raise ValueError(f'Key {key} contains unexpected value {value}.')

    return directories


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
    result = directory_sizes(tree)

    # Discard all directories with size > MAX_DIR_SIZE:
    filtered = dict(filter(lambda item: item[1] <= MAX_DIR_SIZE, result.items()))

    # Calculate sum of sizes of remaining directories:
    total = sum(filtered.values())

    print(f'\nTotal space for directories smaller than {MAX_DIR_SIZE:,}:  {total:,}\n')

    # Debugging
    print(f'Directories and their total size:\n{json.dumps(result, indent=4, sort_keys=True)}')
    print(f'\nDirectories <= {MAX_DIR_SIZE:,}:\n{json.dumps(filtered, indent=4, sort_keys=True)}')
    print(f'\nDirectory structure:\n{json.dumps(tree, indent=4, sort_keys=True)}')
    return tree, result, filtered


if __name__ == '__main__':
    main()
