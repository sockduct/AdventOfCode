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
# INFILE = r'\working\github\sockduct\aoc\2022\d7p1.txt'
INFILE = 'd7p1.txt'
MAX_DIR_SIZE = 100_000
MIN_REQ_SPACE = 30_000_000
TOTAL_DISK_SPACE = 70_000_000


import json


def directory_sizes(tree, directories=None, cwd=None):
    '''
    Add a depth component to deal with directories at different depths with the
    same name
    '''
    if not directories:
        directories = {}
    if not cwd:
        cwd = []
    for key, value in tree.items():
        if isinstance(value, dict):
            cwd.append(key)
            dirent = f'{key}_{len(cwd)}'
            directories[dirent] = 0
            directory_sizes(tree[key], directories, cwd)
            cwd.pop()
            if cwd:
                dirent_parent = f'{cwd[-1]}_{len(cwd)}'
                directories[dirent_parent] += directories[dirent]
        elif isinstance(value, int):
            dirent_parent = f'{cwd[-1]}_{len(cwd)}'
            directories[dirent_parent] += value
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
    dir_sizes = directory_sizes(tree)

    # Discard all directories with size > MAX_DIR_SIZE:
    filtered_dirs = dict(filter(lambda item: item[1] <= MAX_DIR_SIZE, dir_sizes.items()))

    # Part 2 - Find directory that will free up at least MIN_REQ_SPACE
    # * Available space = MAX_DIR_SIZE - size of '/'
    avail_space = TOTAL_DISK_SPACE - dir_sizes['/_1']

    # * Required space = MIN_REQ_SPACE - Available space
    req_space = MIN_REQ_SPACE - avail_space

    # * Find smallest directory >= Required space
    sorted_dirs = dict(sorted(dir_sizes.items(), key=lambda item: item[1]))
    match_dirs = {key: value for key, value in sorted_dirs.items() if value >= req_space}
    smallest_match = list(match_dirs.items())[0]

    # Calculate sum of sizes of remaining directories:
    total = sum(filtered_dirs.values())

    print(f'\nPart 1 - Total space for directories smaller than {MAX_DIR_SIZE:,}:  {total:,}')
    print(f'Part 2 - Size of smallest directory freeing up enough space:  {smallest_match[1]:,} '
          f'({smallest_match[0]})\n')

    # Debugging
    '''
    print(f'Directories and their total size:\n{json.dumps(dir_sizes, indent=4, sort_keys=True)}')
    print(f'\nDirectories <= {MAX_DIR_SIZE:,}:\n{json.dumps(filtered_dirs, indent=4, sort_keys=True)}')
    print(f'\nDirectory structure:\n{json.dumps(tree, indent=4, sort_keys=True)}')
    return tree, dir_sizes, filtered_dirs
    '''


if __name__ == '__main__':
    main()
