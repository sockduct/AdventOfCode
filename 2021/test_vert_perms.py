from itertools import permutations

test_vert = ('x', 'y', 'z')
test_perm = (1, 2, 3)
valid_results = {(1, 2, 3): ('x', 'y', 'z'), (1, 3, 2): ('x', 'z', 'y'),
                 (2, 1, 3): ('y', 'x', 'z'), (2, 3, 1): ('y', 'z', 'x'),
                 (3, 1, 2): ('z', 'x', 'y'), (3, 2, 1): ('z', 'y', 'x')}

def vert_transform(vertex, offsets):
    x_index = offsets.index(1) if offsets.count(1) else offsets.index(-1)
    y_index = offsets.index(2) if offsets.count(2) else offsets.index(-2)
    z_index = offsets.index(3) if offsets.count(3) else offsets.index(-3)

    new_vertex = [None, None, None]
    new_vertex[x_index] = vertex[x_index]
    new_vertex[y_index] = vertex[y_index]
    new_vertex[z_index] = vertex[z_index]

    xoff = offsets[x_index]
    yoff = offsets[y_index]
    zoff = offsets[z_index]

    if xoff == -1:
        new_vertex[x_index] = -new_vertex[x_index]
    if yoff == -2:
        new_vertex[y_index] = -new_vertex[y_index]
    if zoff == -3:
        new_vertex[z_index] = -new_vertex[z_index]

    return tuple(new_vertex)

def vert_transform2(vertex, offset):
    sign = [-1 if e < 0 else 1 for e in offset]
    indices = [abs(e) for e in offset]

    return tuple(vertex[e - 1] * s for e, s in zip(indices, sign))

def vert_transform3(vertex, offset):
    sign = lambda x: -1 if x < 0 else 1

    return tuple(vertex[abs(offind) - 1] * sign(offind) for offind in offset)

if __name__ == '__main__':
    # Function to test:
    ##test_func = vert_transform
    ##test_func = vert_transform2
    test_func = vert_transform3

    # Test:
    for key, val in valid_results.items():
        assert (res := test_func(test_vert, key)) == val, (f'vert_transform{test_vert, key} '
               f'=> {res}, should be {val}')

    # If all is well:
    print('All tests passed.')
