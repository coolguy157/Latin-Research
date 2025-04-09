import random

# Order of the Latin Square to be checked
n=11

def has_transversal(square):
    """
    Checks if the given Latin square has a complete transversal.
    A transversal is a selection of n entries (one per row and column)
    with all symbols distinct.
    """
    n = len(square)
    used_cols = [False] * n

    def backtrack(row, used_symbols):
        if row == n:
            return True
        for col in range(n):
            if not used_cols[col]:
                symbol = square[row][col]
                if symbol in used_symbols:
                    continue
                used_cols[col] = True
                used_symbols.add(symbol)
                if backtrack(row + 1, used_symbols):
                    return True
                used_cols[col] = False
                used_symbols.remove(symbol)
        return False

    return backtrack(0, set())

def row_containing_sym(L, c, x):
    r1 = -1
    r2 = -1

    for r in range(n):
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

    for c in range(n):
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
    seed = [[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
            [1, 0, 3, 2, 5, 4, 7, 6, 9, 10, 8],
            [2, 3, 0, 1, 6, 7, 4, 5, 10, 8, 9],
            [3, 2, 1, 0, 7, 8, 9, 10, 4, 5, 6],
            [4, 5, 6, 7, 0, 9, 10, 8, 1, 2, 3],
            [5, 4, 7, 6, 1, 10, 8, 9, 0, 3, 2],
            [6, 7, 8, 9, 10, 0, 1, 2, 3, 4, 5],
            [8, 9, 10, 4, 3, 6, 5, 0, 2, 1, 7],
            [9, 10, 5, 8, 2, 3, 0, 1, 6, 7, 4],
            [10, 6, 9, 5, 8, 2, 3, 4, 7, 0, 1],
            [7, 8, 4, 10, 9, 1, 2, 3, 5, 6, 0]] # randomly chosen seed for the generator
    
    print(f"Searching for a Latin square of order {n} without a complete transversal...")
    
    count = 0
    generator = generateSquare(seed)
    while True:
        count += 1
        seed = next(generator)
        if count % 1000 == 0:
            print(f"Checked {count} Latin squares...")

        if not has_transversal(seed):
            print("Found a Latin square without a complete transversal:")
            for row in seed:
                print(row)
            break

    print("No Latin square without a complete transversal was found in the searched space.")


if __name__ == "__main__":
    main()