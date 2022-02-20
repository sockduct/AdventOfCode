#! /usr/bin/env python3.10


INFILE = 'd16p1t1.txt'
# INFILE = 'd16p1.txt'


'''
Transmission:  D2FE28 - literal value packet
Convert into binary:
110100101111111000101000
VVVTTTAAAAABBBBBCCCCC
* 1st 3 bits the version (6)
* 2nd 3 bits the type (4 = literal value packet)
  * Types other than 4 are operators that perform calculations on contained
    sub-packets
* 1 or more groups of 5 bits:
  * Leading 1 + 4 bits = non-last digit group
  * Leading 0 + 4 bits = last digit group
  * Concatenate all digit groups, stripping first bit to find number (2021)
* Ignore trailing 0's


Transmission:  38006F45291200 operator packet type 0 with two sub-packets:
00111000000000000110111101000101001010010001001000000000
VVVTTTILLLLLLLLLLLLLLLAAAAAAAAAAABBBBBBBBBBBBBBBB
* 1st 3 bits the version (1)
* 2nd 3 bits the type is something other than 4 = operator packet (6)
* 3rd 1 bit for non type-4 packets is length type indicator bit (0)
  * Bit = 0:  Next 15 bits are bit length of sub-packets
  * Bit = 1:  Next 11 bits are number of sub-packets
* 4th 15 bits contain length of sub-packets (27)
* 5th 11 bits contain first sub-packet (10)
* 6th 16 bits contain second sub-packet (20)
* Ignore trailing 0's

11010001010     0101001000100100
AAAAAAAAAAA     BBBBBBBBBBBBBBBB
VVVTTTGGGGG     VVVTTTAAAAABBBBB

v=110, 6        v=010, 2
t=100, 4        t=100, 4
g=01010, 10     g=00010100, 20


Transmission:  EE00D40C823060 operator packet type 1 iwth three sub-packets:
11101110000000001101010000001100100000100011000001100000
VVVTTTILLLLLLLLLLLAAAAAAAAAAABBBBBBBBBBBCCCCCCCCCCC
* 1st 3 bits the version (7)
* 2nd 3 bits the type is something other than 4 = operator packet (3)
* 3rd 1 bit for non type-4 packets is length type indicator bit (1)
  * Bit = 0:  Next 15 bits are bit length of sub-packets
  * Bit = 1:  Next 11 bits are number of sub-packets
* 4th 11 bits contain number of sub-packets (3)
* 5th 11 bits contain first sub-packet (1)
* 6th 11 bits contain second sub-packet (2)
* 7th 11 bits contain third sub-packet (3)
* Ignore trailing 0's


Answer for problem 1:
Parse the hierarchy of the packets throughout the transmission and add up all of
the version numbers.
'''
class Packet():
    def __init__(self, hexdata):
        self.hexdata = hexdata
        self.bindata = bin(int(hexdata, 16))[2:]

    def __repr__(self):
        return f'<Packet({self.hexdata})>'

    def get_lval(self, data):
        pointer = 0
        bindata = ''

        while pointer < len(data):
            if data[pointer] == '1':
                bindata += data[pointer + 1:pointer + 5]
                pointer += 5
            # Last digit group:
            elif data[pointer] == '0':
                bindata += data[pointer + 1:pointer + 5]
                pointer += 5
                break
            else:
                raise ValueError(f'Expected value of 0 or 1, got {data[pointer]}')

        return int(bindata, 2), pointer

    def process(self):
        pointer = 0
        plen = len(self.bindata)
        new_packet = True

        while pointer < plen:
            if new_packet:
                pver = self.bindata[pointer:pointer + 3]
                ptype = self.bindata[pointer + 3:pointer + 6]
                pointer += 6

                # Literal value packet:
                if ptype == '100':
                    pdigit, inc = self.get_lval(self.bindata[pointer:])
                    pointer += inc
                # Operator packet:
                else:
                    pind = self.bindata[pointer + 6]
                    if pind == '0':
                        ...
                    elif pind == '1':
                        ...
                    else:
                        raise ValueError(f'Expected value of 0 or 1, got {pind}')

                if int(self.bindata[pointer:], 2) == 0:
                    pzeros = plen - pointer
                    break
                else:
                    raise ValueError('Unexpected non-zero trailing digits:  '
                                    f'{self.bindata[pointer:]}')

        print(f'Found packet:\nVersion={int(pver, 2)}, Type={int(ptype, 2)}, Digit={pdigit}, '
              f'Trailing Zeros={pzeros}')


def main():
    packet = Packet('D2FE28')
    packet.process()


if __name__ == '__main__':
    main()
