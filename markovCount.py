import random

n=11 # Order of the square to be checked

def count_transversals(square, limit):
    n = len(square)
    used_cols = [False] * n
    count = 0

    def backtrack(row, used_symbols):
        nonlocal count
        # Early exit if we've exceeded the limit.
        if count > limit:
            count+=9999 # Set count to a large value so it doesn't flag as a new minuimum 
            return

        if row == n:
            count += 1
            return

        for col in range(n):
            if not used_cols[col]:
                symbol = square[row][col]
                if symbol in used_symbols:
                    continue
                used_cols[col] = True
                used_symbols.add(symbol)
                backtrack(row + 1, used_symbols)
                used_cols[col] = False
                used_symbols.remove(symbol)

    backtrack(0, set())
    return count

def row_containing_sym(L, c, x):
    r1 = -1
    r2 = -1

    for r in range(len(L)):
        if r1 >= 0 and r2 >= 0:
            break

        if L[r][c] == x and r1 < 0:
            r1 = r
            continue

        if L[r][c] == x and r2 < 0:
            r2 = r
            break

    assert r1 >= 0 and r2 >= 0

    return r1 if (random.random() < 0.5) else r2

def column_containing_sym(L, r, x):
    c1 = -1
    c2 = -1

    for c in range(len(L)):
        if c1 >= 0 and c2 >= 0:
            break

        if L[r][c] == x and c1 < 0:
            c1 = c
            continue

        if L[r][c] == x and c2 < 0:
            c2 = c
            break

    assert c1 >= 0 and c2 >= 0

    return c1 if (random.random() < 0.5) else c2

def generateSquare(L_start):
    """Generator for a sequence of uniformly distributed latin squares,
    given L_start as the initial latin square.

    This code implements the Markov chain algorithm of Jacobson and Matthews (1996), 
    based on the sagemath implementation in Python.

    REFERENCES:

    Mark T. Jacobson and Peter Matthews, "Generating uniformly
    distributed random Latin squares", Journal of Combinatorial Designs, 4 (1996).  
    https://doi.org/10.1002/(SICI)1520-6610(1996)4:6%3C405::AID-JCD3%3E3.0.CO;2-J
    The SageMath Developers. (2025). SageMath (Version 10.7.beta0) [Computer software].
    https://doi.org/10.5281/zenodo.8042260"""
    
    r1 = r2 = c1 = c2 = x = y = z = -1
    proper = True

    from copy import copy
    L = copy(L_start)

    L_cer = [[None] * n for _ in range(n)]
    L_erc = [[None] * n for _ in range(n)]

    while True:
        if proper:
            # Update the other two conjugates
            for r in range(n):
                for c in range(n):
                    e = L[r][c]

                    L_cer[c][e] = r
                    L_erc[e][r] = c

            yield L

            r1 = random.randint(0, n-1)
            c1 = random.randint(0, n-1)
            x = L[r1][c1]

            y = x
            while y == x:
                y = random.randint(0, n-1)


            c2 = L_erc[y][r1]
            r2 = L_cer[c1][y]

            L[r1][c1] = y
            L[r1][c2] = x
            L[r2][c1] = x

            # Now deal with the unknown point.
            # We want to form z + (y - x)
            z = L[r2][c2]

            if z == x:
                L[r2][c2] = y
            else:
                # z and y have positive coefficients
                # x is the improper term with a negative coefficient
                proper = False
        else:  # improper square,
            # L[r2, c2] = y + z - x
            # y and z are proper while x is the
            # improper symbol in the cell L[r2, c2].

            r1 = row_containing_sym(L, c2, x)
            c1 = column_containing_sym(L, r2, x)

            # choose one of the proper symbols
            # uniformly at random (we will use whatever
            # lands in variable y).
            if (random.random() < 0.5):
                y, z = z, y

            # Add/subtract the symbolic difference (y - x)
            L[r2][c2] = z
            L[r1][c2] = y
            L[r2][c1] = y

            if L[r1][c1] == y:
                L[r1][c1] = x
                proper = True
            else:  # got another improper square
                z = L[r1][c1]
                x, y = y, x
                r2 = r1
                c2 = c1

                # Now we have L[r2, c2] = z+y-x as
                # usual
                proper = False  # for emphasis

def main():
    min_transversals = 3126
    seed = [[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
            [1, 0, 3, 2, 5, 4, 7, 6, 9, 10, 8],
            [2, 3, 0, 1, 6, 7, 4, 5, 10, 8, 9],
            [3, 2, 1, 0, 7, 8, 9, 10, 4, 5, 6],
            [4, 5, 6, 7, 0, 9, 10, 8, 1, 2, 3],
            [5, 4, 7, 6, 1, 10, 8, 9, 0, 3, 2],
            [6, 7, 8, 9, 10, 0, 1, 2, 3, 4, 5],
            [8, 9, 10, 4, 2, 3, 5, 1, 6, 0, 7],
            [10, 6, 5, 8, 9, 2, 3, 4, 7, 1, 0],
            [9, 8, 4, 10, 3, 6, 2, 0, 5, 7, 1],
            [7, 10, 9, 5, 8, 1, 0, 3, 2, 6, 4]]
    min_square = None
    print(f"Searching for the minimum number of transversals in Latin squares of order {n}...")
    
    count = 0
    generator = generateSquare(seed)
    while True:
        count += 1
        latin = next(generator)
        if count % 1000 == 0:
            print(f"Checked {count} Latin squares...")

        num_trans = count_transversals(latin, min_transversals)
        
        # Update minimum if needed.
        if num_trans <= min_transversals:
            min_transversals = num_trans
            min_square = latin
            print(f"New minimum found: {min_transversals} transversals")
            print("Latin square achieving this:")
            for row in min_square:
                print(row)
            # Stop if a Latin square with no transversal is found.
            if min_transversals == 0:
                print("Found a Latin square with 0 transversals:")
                for row in latin:
                    print(row)
                break


if __name__ == "__main__":
    main()