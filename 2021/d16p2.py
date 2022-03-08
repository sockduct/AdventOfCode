#! /usr/bin/env python3.10


INFILE = 'd16p1.txt'


from math import prod
from operator import lt, gt, eq
import re


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


Packet Types:
* 0 - sum of sub-packets
* 1 - product of sub-packets
* 2 - minimum of sub-packets
* 3 - maximum of sub-packets
* 4 - literal value packet
* 5 - > packet:  1 if 1st sub-packet > 2nd sub-packet else 0, always have 2
                 sub-packets
* 6 - < packet:  1 if 1st sub-packet < 2nd sub-packet else 0, always have 2
                 sub-packets
* 7 - = to packet:  1 if 1st sub-packet == 2nd sub-packet else 0, always have
                    2 sub-packets


Answer for problem 2:
Calculate the value of the expression represented by packet
'''
class Packet():
    def __init__(self, hexdata):
        self.hexdata = hexdata
        # This needs to be a multiple of 4, but this conversion strips leading
        # 0's, so we need to add them back:
        self.bindata = bin(int(hexdata, 16))[2:]
        if (extra_ditits := len(self.bindata) % 4) > 0:
            self.bindata = '0' * (4 - extra_ditits) + self.bindata

        # Check for leading 0's:
        if (leading_zeroes := re.match(r'(0+)', self.hexdata)):
            self.bindata = '0' * (len(leading_zeroes.group(1)) * 4) + self.bindata

        self._pointer = 0

    def __repr__(self):
        return f'<Packet({self.hexdata})>'

    def _calc_helper(self, item, values, op, value_stack, arg_count=0):
        packet_count = 1
        bit_count = item['bit_len']

        if item.get('packets'):
            item_type = 'packets'
            item_count = item['packets']
        elif item.get('bits'):
            item_type = 'bits'
            item_count = item['bits']

        '''
        Cases:
        1) Packet/bit count in op packet = payload
        2) Packet/bit count in op packet < payload (warning and discard extras)
        3) Packet/bit count in op packet > payload:
           Add from value_stack - exception if insufficient data
        '''

        if item_type == 'packets':
            value_count = len(values)
        elif item_type == 'bits':
            value_count = sum(value[1] for value in values)
        else:
            raise ValueError(f'Expected item type of packets or bits ({item})')

        if item_count == value_count:
            packet_count += len(values)
            if arg_count and (packet_count - 1) > arg_count:
                raise ValueError(f'Value count greater than argument count:  {arg_count=},'
                                 f' {packet_count=}, {item_count=}, {value_count=}')
            bit_count += sum(value[1] for value in values)
            if op.__module__ == '_operator':
                res = int(op(*[value[0] for value in values]))
            else:
                res = op(value[0] for value in values)
        elif item_count < value_count:
            value_tally = 0
            value_subset = []
            while values:
                value_subset.append(value_item := values.pop(0))
                value_tally += value_item[1] if item_type == 'bits' else 1
                packet_count += 1
                if arg_count and (packet_count - 1) > arg_count:
                    raise ValueError(f'Value count greater than argument count:  {arg_count=},'
                                     f' {packet_count=}, {item_count=}, {value_count=}')
                bit_count += value_item[1]
                if value_tally == item_count:
                    break
                elif value_tally > item_count:
                    raise ValueError('Value tally exceeds item count')
            if op.__module__ == '_operator':
                res = int(op(*[value[0] for value in value_subset]))
            else:
                res = op(value[0] for value in value_subset)

            while values:
                value_item = values.pop()
                value_stack.append((value_item[0], dict(packet_count=1, bit_count=value_item[1])))
        elif item_count > value_count and value_stack:
            value_tally = value_count
            value_subset = values.copy()
            packet_count += len(values)
            arg_count_items = len(values)
            bit_count += sum(value[1] for value in values)
            while True:
                value_item = value_stack.pop()
                if 'packet_count' in value_item[1]:
                    packet_count += value_item[1]['packet_count']
                else:
                    packet_count += 1
                arg_count_items += 1
                if arg_count and arg_count_items > arg_count:
                    raise ValueError(f'Value count greater than argument count:  {arg_count=},'
                                    f' {packet_count=}, {item_count=}, {value_count=}')
                bit_count += value_item[1]['bit_count']
                value_subset.append(value_item)
                value_tally += value_item[1]['bit_count'] if item_type == 'bits' else 1
                if value_tally == item_count:
                    break
                elif value_tally > item_count:
                    raise ValueError('Value tally exceeds item count')
            if op.__module__ == '_operator':
                res = int(op(*[value[0] for value in value_subset]))
            else:
                res = op(value[0] for value in value_subset)
        else:
            raise ValueError(f'Insufficient number of arguments ({item=}, {value_stack=})')

        return (res, dict(packet_count=packet_count, bit_count=bit_count))

    def calculate(self, op_stack):
        '''
        * 0 - sum of sub-packets
        * 1 - product of sub-packets
        * 2 - minimum of sub-packets
        * 3 - maximum of sub-packets
        * 4 - literal value packet
        * 5 - > packet:  1 if 1st sub-packet > 2nd sub-packet else 0
        * 6 - < packet:  1 if 1st sub-packet < 2nd sub-packet else 0
        * 7 - = to packet:  1 if 1st sub-packet == 2nd sub-packet else 0
        '''
        value_stack = []
        while op_stack:
            item = op_stack.pop()
            match (key := list(item.keys())[0]):
                case 0:
                    res = self._calc_helper(item, item[key], sum, value_stack)
                case 1:
                    res = self._calc_helper(item, item[key], prod, value_stack)
                case 2:
                    res = self._calc_helper(item, item[key], min, value_stack)
                case 3:
                    res = self._calc_helper(item, item[key], max, value_stack)
                case 4:
                    res = item[4]
                    raise Exception('Why do I exist?  I\'m never called!')
                case 5:
                    res = self._calc_helper(item, item[key], gt, value_stack, arg_count=2)
                case 6:
                    res = self._calc_helper(item, item[key], lt, value_stack, arg_count=2)
                case 7:
                    res = self._calc_helper(item, item[key], eq, value_stack, arg_count=2)
                case _: raise ValueError('Expected type in range 0-7, got {ptype}')

            value_stack.append(res)

        print(f'Operations stack:  {op_stack}')
        print(f'Result:  {res}')
        return res


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
        more_nonzeroes = True
        op_stack = []

        while self._pointer < plen and more_nonzeroes:
            bit_start = self._pointer
            pver = int(self.bindata[self._pointer:self._pointer + 3], 2)
            ptype = int(self.bindata[self._pointer + 3:self._pointer + 6], 2)
            match ptype:
                case 0: pdescr = 'sum packet'
                case 1: pdescr = 'product packet'
                case 2: pdescr = 'minimum packet'
                case 3: pdescr = 'maximum packet'
                case 4: pdescr = 'literal-value packet'
                case 5: pdescr = 'greater-than packet'  # T|F - 2 packets
                case 6: pdescr = 'less-than packet'  # T|F - 2 packets
                case 7: pdescr = 'equal-to packet'  # T|F - 2 packets
                case _: raise ValueError(f'Expected type in range 0-7, got {ptype}')
            self._pointer += 6

            # Literal value packet:
            if ptype == 4:
                pdigit = self.get_lval()
                poptlv = ('digit', pdigit)  # Packet operation - type, length, value
                bit_len = self._pointer - bit_start
                if not op_stack:
                    op_stack.append((pdigit, bit_len))
                else:
                    list(op_stack[-1].values())[0].append((pdigit, bit_len))
            # Operator packet:
            else:
                # Get length type indicator bit:
                pind = self.bindata[self._pointer]
                self._pointer += 1

                # Next 15 bits are bit length of sub-packets
                if pind == '0':
                    poptlv = ('bits', int(self.bindata[self._pointer:self._pointer + 15], 2))
                    self._pointer += 15
                    # Process sub-packet(s) in next iteration...
                # Next 11 bits are number of sub-packets
                elif pind == '1':
                    poptlv = ('packets', int(self.bindata[self._pointer:self._pointer + 11], 2))
                    self._pointer += 11
                    # Process sub-packet(s) in next iteration...
                # Parse error/invalid packet:
                else:
                    raise ValueError(f'Expected value of 0 or 1, got {pind}')

                bit_len = self._pointer - bit_start
                op_stack.append({ptype: [], poptlv[0]: poptlv[1], 'bit_len': bit_len})


            digits_left = plen - self._pointer
            if digits_left == 0:
                poprem = ('nothing remaining', digits_left)
            elif int(self.bindata[self._pointer:], 2) == 0:
                poprem = ('zeroes', digits_left)  # Packet operation - what's remaining
                more_nonzeroes = False
            else:
                poprem = ('non-zeroes', digits_left)

            print(f'Found packet:  Version={pver}, Type={ptype} ({pdescr}), Value={poptlv[1]} '
                  f'({poptlv[0]}), Bit length={bit_len}, Remaining Digits='
                  f'{poprem[1]} ({poprem[0]})')

        return self.calculate(op_stack)


def main():
    # Test data:
    '''
    for packet_data, expected_result in (
        ('C200B40A82', 3),  # Finds the sum of 1 and 2, resulting in the value 3
        ('04005AC33890', 54),  # Finds the product of 6 and 9, resulting in the value 54
        ('880086C3E88112', 7),  # Finds the minimum of 7, 8, and 9, resulting in the value 7
        ('CE00C43D881120', 9),  # Finds the maximum of 7, 8, and 9, resulting in the value 9
        ('D8005AC2A8F0', 1),  # Produces 1, because 5 is less than 15
        ('F600BC2D8F', 0),  # Produces 0, because 5 is not greater than 15
        ('9C005AC2F8F0', 0),  # Produces 0, because 5 is not equal to 15
        ('9C0141080250320F1802104A08', 1)  # Produces 1, because 1 + 3 = 2 * 2
    ):

        print(f'\nRead in packet:  {packet_data}')
        packet = Packet(packet_data)
        res = packet.process()
        assert res[0] == expected_result
    print('\n')
    '''

    # Actual data:
    with open(INFILE) as infile:
        packet_data = infile.read().strip()

    packet = Packet(packet_data)
    packet.process()


if __name__ == '__main__':
    main()
