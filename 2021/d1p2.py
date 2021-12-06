INFILE = 'd1p1.txt'

def main():
    prev = None
    prev1 = None
    prev2 = None
    current = 0
    increases = 0

    with open(INFILE) as infile:
        for number in infile:
            number = int(number)
            if prev1 and prev2:
                current = number + prev1 + prev2
            if prev and current > prev:
                increases += 1
                prev = current
            elif current:
                prev = current
            if prev1:
                prev2 = prev1
            prev1 = number

    print(f'Increases:  {increases}')

if __name__ == '__main__':
    main()
