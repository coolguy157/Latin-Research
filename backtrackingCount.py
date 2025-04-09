def count_transversals(square, limit=None):
    n = len(square)
    used_cols = [False] * n
    count = 0

    def backtrack(row, used_symbols):
        nonlocal count
        # Early exit if we've exceeded the limit.
        if limit is not None and count > limit:
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


def generate_latin_squares(n):
    """
    Generates all Latin squares of order n (normalized so that the first row is [0,1,...,n-1])
    using a backtracking algorithm.
    """
    square = [[None] * n for _ in range(n)]
    # Fix the first row to reduce symmetry.
    square[0] = list(range(n))

    def valid(row, col, value):
        # Check if 'value' already appears in this row (up to col)
        if value in square[row][:col]:
            return False
        # Check the column for previous rows
        for r in range(row):
            if square[r][col] == value:
                return False
        return True

    def backtrack(cell):
        if cell == n * n:
            # Found a complete Latin square; yield a deep copy.
            yield [row[:] for row in square]
            return

        row, col = divmod(cell, n)
        # If first row is already fixed, skip it.
        if row == 0:
            yield from backtrack(cell + 1)
        else:
            for value in range(n):
                if valid(row, col, value):
                    square[row][col] = value
                    yield from backtrack(cell + 1)
            # Reset the cell before backtracking further.
            square[row][col] = None

    # Start from cell index n (since row 0 is already fixed)
    yield from backtrack(n)


def main():
    # Latin square order
    n = 11
    print(f"Searching for the minimum number of transversals in Latin squares of order {n}...")

    min_transversals = 3255
    min_square = None
    count = 0

    for latin in generate_latin_squares(n):
        count += 1
        if count < 2000: # burn first 2000 squares, as we have precomputed this to obtain the 3255 metric (simple initial speedup)
            continue
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
            print()
            # Stop if a Latin square with no transversal is found.
            if min_transversals == 0:
                print("Found a Latin square with 0 transversals:")
                for row in latin:
                    print(row)
                print()
                return

    print(f"Minimum number of transversals found: {min_transversals}")
    print("Latin square achieving this:")
    for row in min_square:
        print(row)


if __name__ == "__main__":
    main()