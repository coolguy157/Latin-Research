def print_transversals(square):
    n = len(square)
    used_cols = [False] * n
    count = 0

    with open('transversals.txt', 'w') as f:
        def backtrack(row, used_symbols, current_transversal):
            nonlocal count
            if row == n:
                f.write(str(current_transversal) + '\n')
                count += 1
                return

            for col in range(n):
                if not used_cols[col]:
                    symbol = square[row][col]
                    if symbol in used_symbols:
                        continue

                    used_cols[col] = True
                    used_symbols.add(symbol)
                    backtrack(row + 1, used_symbols, current_transversal + [(row, col, symbol)])
                    used_cols[col] = False
                    used_symbols.remove(symbol)

        backtrack(0, set(), [])

    return count


# Define the Latin square.
latin_square = [[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
                [1, 0, 3, 2, 5, 4, 7, 6, 9, 10, 8],
                [2, 3, 0, 1, 6, 7, 4, 5, 10, 8, 9],
                [3, 2, 1, 0, 7, 8, 9, 10, 4, 5, 6],
                [4, 5, 6, 7, 0, 9, 10, 8, 1, 2, 3],
                [5, 4, 7, 6, 1, 10, 8, 9, 0, 3, 2],
                [6, 7, 8, 9, 10, 0, 1, 2, 3, 4, 5],
                [8, 9, 10, 4, 2, 3, 5, 1, 6, 0, 7],
                [10, 6, 5, 8, 9, 2, 3, 4, 7, 1, 0],
                [7, 10, 9, 5, 8, 1, 0, 3, 2, 6, 4],
                [9, 8, 4, 10, 3, 6, 2, 0, 5, 7, 1]]

if __name__ == '__main__':
    print(f"Total transversals found: {print_transversals(latin_square)}")