import itertools

def find_decomposition(latin_square):
    n = len(latin_square)
    # col_assigned[c][t] is True if column c already has a cell with transversal label t.
    col_assigned = [[False] * n for _ in range(n)]
    # transversal_symbols[t] is a set of symbols already used in transversal t.
    transversal_symbols = [set() for _ in range(n)]
    # decomposition[r][c] will store the transversal label assigned to cell (r, c)
    # Only one cell in each row gets each transversal label; you could also keep track of the chosen positions.
    decomposition = [[None] * n for _ in range(n)]
    solutions = []

    def search(row):
        if row == n:
            # At this point, we have assigned a transversal label to every cell in every row.
            # We now extract the cells that form each transversal.
            transversals = {t: [] for t in range(n)}
            for r in range(n):
                for c in range(n):
                    t = decomposition[r][c]
                    if t is not None:
                        transversals[t].append((r, c, latin_square[r][c]))
            solutions.append(transversals)
            return
        
        # For the current row, try every permutation of transversal labels.
        # The permutation assigns, for each column j in row, a transversal number perm[j].
        for perm in itertools.permutations(range(n)):
            valid = True
            # For checking validity without updating global state, first pass.
            for c in range(n):
                t = perm[c]
                symbol = latin_square[row][c]
                if col_assigned[c][t]:
                    valid = False
                    break
                if symbol in transversal_symbols[t]:
                    valid = False
                    break
            if not valid:
                continue

            # If valid, commit the assignment.
            for c in range(n):
                t = perm[c]
                decomposition[row][c] = t
                col_assigned[c][t] = True
                transversal_symbols[t].add(latin_square[row][c])
            
            search(row + 1)

            # Backtrack: remove the assignment for the current row.
            for c in range(n):
                t = perm[c]
                decomposition[row][c] = None
                col_assigned[c][t] = False
                transversal_symbols[t].remove(latin_square[row][c])
    
    search(0)
    return solutions

# Example usage:
latin_square = [
    [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
    [1, 0, 3, 2, 5, 4, 7, 6, 9, 10, 8],
    [2, 3, 0, 1, 6, 7, 4, 5, 10, 8, 9],
    [3, 2, 1, 0, 7, 8, 9, 10, 4, 5, 6],
    [4, 5, 6, 7, 0, 9, 10, 8, 1, 2, 3],
    [5, 4, 7, 6, 1, 10, 8, 9, 0, 3, 2],
    [6, 7, 8, 9, 10, 0, 1, 2, 3, 4, 5],
    [8, 9, 10, 4, 2, 3, 5, 1, 6, 0, 7],
    [10, 6, 5, 8, 9, 2, 3, 4, 7, 1, 0],
    [7, 10, 9, 5, 8, 1, 0, 3, 2, 6, 4],
    [9, 8, 4, 10, 3, 6, 2, 0, 5, 7, 1]
]

solutions = find_decomposition(latin_square)

if solutions:
    print("Found at least one transversal decomposition.")
    # Show one solution as an example:
    example = solutions[0]
    for t in range(len(example)):
        print(f"Transversal {t}: {example[t]}")
else:
    print("No transversal decomposition found.")