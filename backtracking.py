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
    # latin square order
    n = 9 
    
    print(f"Searching for a Latin square of order {n} without a complete transversal...")
    
    count = 0
    for latin in generate_latin_squares(n):
        count += 1
        if count % 1000 == 0:
            print(f"Checked {count} Latin squares...")
        if not has_transversal(latin):
            print("Found a Latin square without a complete transversal:")
            for row in latin:
                print(row)
            return

    print("No Latin square without a complete transversal was found in the searched space.")


if __name__ == "__main__":
    main()