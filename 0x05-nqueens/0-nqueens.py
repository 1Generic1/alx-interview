#!/usr/bin/python3
'''N-Queens Challenge'''

import sys


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: nqueens N")
        sys.exit(1)

    try:
        n = int(sys.argv[1])
    except ValueError:
        print('N must be a number')
        exit(1)

    if n < 4:
        print('N must be at least 4')
        exit(1)

    solutions = []
    placed_queens = []  # coordinates format [row, column]
    stop = False
    r = 0
    c = 0

    # iterate thru rows
    while r < n:
        goback = False
        # iterate thru columns
        while c < n:
            # check is current column is safe
            safe = True
            for cord in placed_queens:
                col = cord[1]
                if(col == c or col + (r-cord[0]) == c or
                        col - (r-cord[0]) == c):
                    safe = False
                    break

            if not safe:
                if c == n - 1:
                    goback = True
                    break
                c += 1
                continue

            # place queen
            cords = [r, c]
            placed_queens.append(cords)
            # if last row, append solution and reset all to last unfinished row
            # and last safe column in that row
            if r == n - 1:
