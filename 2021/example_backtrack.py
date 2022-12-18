'''
Example backtracking - generate subsets
This is fixed to generate subsets of 1 - #...
'''

MAXCANDIDATES = 100	 # Max possible next extensions
NMAX = 100	         # Maximum solution size
finished = False     # Found all solutions yet?


def backtrack(a, k, n):
    c = []  # candidates for next position
    nc = 0  # next position candidate count

    if is_a_solution(a, k, n):
        process_solution(a, k, n)
    else:
        k += 1
        nc = construct_candidates(a, k, n, c, nc)
        for i in range(nc):
            while len(a) < k + 1:
                a.append(False)
            a[k] = c[i]
            make_move(a, k, n)
            backtrack(a, k, n)
            unmake_move(a, k, n)

            if (finished):
                return  # terminate early


def construct_candidates(a, k, n, c, nc):
    if len(c) >= 1:
        c[0] = True
    else:
        c.append(True)

    if len(c) >= 2:
        c[1] = False
    else:
        c.append(False)

    nc = 2

    return nc


def generate_subsets(n):
    a = []  # solution vector

    backtrack(a, 0, n)


def is_a_solution(a, k, n):
    return (k == n)


def make_move(a, k, n):
    pass


def process_solution(a, k, n):
    print('{', end='')
    for i in range(1, k + 1):
        if (a[i] == True):
            print(f' {i}', end='')

    print(' }')


def unmake_move(a, k, n):
    pass


if __name__ == '__main__':
    generate_subsets(2)
