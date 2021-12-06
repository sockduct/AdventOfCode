#! /usr/bin/env python3.10

# INFILE = 'd2p1t1.txt'
INFILE = 'd2p1.txt'

def main():
    horizon_pos = 0
    depth_pos = 0
    aim_pos = 0

    with open(INFILE) as ifile:
        for line in ifile:
            direction, distance = line.split()
            distance = int(distance)

            # Pattern matching requires Python v3.10+
            match direction:
                case 'forward':
                    horizon_pos += distance
                    depth_pos += aim_pos * distance
                case 'down':
                    aim_pos += distance
                case 'up':
                    aim_pos -= distance

    print(f'Results:\nAim Position:  {aim_pos}\n'
          f'Horizontal Position:  {horizon_pos}\n'
          f'Depth Position:  {depth_pos}\n'
          f'Multiplied:  {horizon_pos * depth_pos}')

if __name__ == '__main__':
    main()
