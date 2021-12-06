INFILE = 'd1p1.txt'

def main():
    prev = None
    increases = 0

    with open(INFILE) as infile:
        for number in infile:
            number = int(number)
            if prev and number > prev:
                increases += 1
            prev = number

    print(f'Increases:  {increases}')

if __name__ == '__main__':
    main()
