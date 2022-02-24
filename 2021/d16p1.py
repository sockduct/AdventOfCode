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
        # This needs to be a multiple of 4, but this conversion strips leading
        # 0's, so we need to add them back:
        self.bindata = bin(int(hexdata, 16))[2:]
        self.bindata = '0' * (len(self.bindata) % 4) + self.bindata

        self._pointer = 0

    def __repr__(self):
        return f'<Packet({self.hexdata})>'

    def get_lval(self):
        bindata = ''

        while self._pointer < len(self.bindata):
            # Digit group, more follow:
            if self.bindata[self._pointer] == '1':
                bindata += self.bindata[self._pointer + 1:self._pointer + 5]
                self._pointer += 5
            # Last digit group:
            elif self.bindata[self._pointer] == '0':
                bindata += self.bindata[self._pointer + 1:self._pointer + 5]
                self._pointer += 5
                break
            # Parse error/invalid packet:
            else:
                raise ValueError(f'Expected value of 0 or 1, got {self.bindata[self._pointer]}')

        return int(bindata, 2)

    def process(self):
        plen = len(self.bindata)

        sub_packets = False
        while self._pointer < plen:
            pver = int(self.bindata[self._pointer:self._pointer + 3], 2)
            ptype = int(self.bindata[self._pointer + 3:self._pointer + 6], 2)
            self._pointer += 6

            # Literal value packet:
            if ptype == 4:
                pdigit = self.get_lval()
                poptlv = ('digit', pdigit)  # Packet operation - type, length, value
            # Operator packet:
            else:
                # Get length type indicator bit:
                pind = self.bindata[self._pointer]
                self._pointer += 1

                sub_packets = True
                # Next 15 bits are bit length of sub-packets
                if pind == '0':
                    poptlv = ('bits', int(self.bindata[self._pointer:self._pointer + 15], 2))
                    self._pointer += 15
                    # Process sub-packet(s) in next iteration...
                    ### Count/limit bits processed to bit number?
                # Next 11 bits are number of sub-packets
                elif pind == '1':
                    poptlv = ('packets', int(self.bindata[self._pointer:self._pointer + 11], 2))
                    self._pointer += 11
                    # Process sub-packet(s) in next iteration...
                    ### Count/limit bits processed to packet number?
                # Parse error/invalid packet:
                else:
                    raise ValueError(f'Expected value of 0 or 1, got {pind}')

            digits_left = plen - self._pointer
            if int(self.bindata[self._pointer:], 2) == 0:
                poprem = ('zeroes', digits_left)  # Packet operation - what's remaining
                break
            else:
                poprem = ('non-zeroes', digits_left)
                # raise ValueError('Unexpected non-zero trailing digits:  {self.bindata[self._pointer:]}')
                ### Temporary...
                break

        print(f'Found packet:\nVersion={pver}, Type={ptype}, Value={poptlv[1]} '
              f'({poptlv[0]}), Remaining Digits={poprem[1]} ({poprem[0]})')

        '''
        if sub_packets:
            print(f'Subpackets present:\nDigit={pdigit}')
        '''

        # Is packet processed (only 0's remain?)
        return poprem[0] == 'zeroes'


def main():
    for packet_data in ('D2FE28', '38006F45291200', 'EE00D40C823060', '8A004A801A8002F478',
                        '620080001611562C8802118E34', 'C0015000016115A2E0802F182340',
                        'A0016C880162017C3686B18A3D4780'):
        print(f'\nRead in packet:  {packet_data}')
        packet = Packet(packet_data)
        while not packet.process():
            continue


if __name__ == '__main__':
    main()
