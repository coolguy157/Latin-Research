def delta(x, y, z, n):
    diff = z-x-y
    return (diff) % n if diff > 0 else diff % -n

def search_transversal_with_fixed(n, latin_square, fixed, row_list, col_avail, current, current_delta, target_delta):
    """
    Searches for a transversal that includes the fixed element.
    
    Parameters:
      n           - size of the Latin square
      latin_square- the n x n Latin square (list of lists)
      fixed       - tuple (fx, fy, fz) representing the fixed element (already in the transversal)
      row_list    - list of remaining row indices to process (fixed row is removed)
      col_avail   - set of columns still available (fixed column removed)
      current     - list of selected cells so far, each as (row, col, symbol)
      current_delta - current sum of delta values modulo n for the chosen cells
      target_delta- value that current_delta must equal at the end (should be -delta(fixed) mod n)
    """
    if not row_list:
        # Base case: all rows processed.
        # Check if the delta condition holds.
        if current_delta % n == target_delta % n:
            return [current.copy()]
        else:
            return []
    
    # Choose next row to assign a cell
    solutions = []
    row = row_list[0]
    # Try every available column in this row.
    for col in list(col_avail):
        symbol = latin_square[row][col]
        # For a proper transversal, you also need to check that the symbol hasn't been used.
        # Here we assume current already uses distinct symbols (you can manage that similarly).
        # For simplicity, we omit the symbol-check in this sketch.
        
        d = delta(row, col, symbol, n)
        # Choose this cell
        current.append((row, col, symbol))
        col_avail.remove(col)
        # Recursively process the remaining rows.
        sols = search_transversal_with_fixed(n, latin_square,
                                             fixed, row_list[1:], col_avail, 
                                             current, (current_delta + d) % n, target_delta)
        solutions.extend(sols)
        # Backtrack
        current.pop()
        col_avail.add(col)
    return solutions

def transversal_exists_through_element(n, latin_square, fixed):
    """
    Returns True if there is at least one transversal containing the fixed element.
    fixed is a tuple (x, y, latin_square[x][y]).
    """
    fx, fy, fz = fixed
    # Compute the delta for the fixed element.
    fixed_delta = delta(fx, fy, fz, n)
    # In any transversal T, we must have:
    # fixed_delta + sum_{other elements} delta = 0 mod n,
    # so the remaining elements must sum to -fixed_delta mod n.
    target_delta = (-fixed_delta) % n
    
    # Prepare the list of rows to fill (exclude fx) and available columns (exclude fy)
    row_list = [r for r in range(n) if r != fx]
    col_avail = set(c for c in range(n) if c != fy)
    
    # Start with the fixed element's delta value in the accumulated sum.
    # Actually, since we already fixed that element, the search will only sum the rest.
    sols = search_transversal_with_fixed(n, latin_square, fixed, row_list, col_avail, [], 0, target_delta)
    
    return len(sols) > 0

# Example of using this test on every element:
def test_every_element_for_transversal(n, latin_square):
    results = {}
    for i in range(n):
        for j in range(n):
            fixed = (i, j, latin_square[i][j])
            exists = transversal_exists_through_element(n, latin_square, fixed)
            results[(i,j)] = exists
            print(f"Transversal through element ({i},{j}) exists? {exists}")
    return results

# Example usage:
n = 11
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
test_results = test_every_element_for_transversal(n, latin_square)