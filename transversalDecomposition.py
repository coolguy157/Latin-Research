import ast
import sys

# Global counter for tracking iterations in the backtracking search.
iterations = 0
n = 11

def load_transversals(filename):
    transversals = []
    try:
        with open(filename, "r") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    transversal = ast.literal_eval(line)
                    # Convert each transversal into a set of (row, col) pairs.
                    cells = {(t[0], t[1]) for t in transversal}
                    if len(cells) != n:
                        print("Warning: Invalid transversal (wrong number of cells):", transversal)
                        continue
                    transversals.append(cells)
                except Exception as e:
                    print("Error parsing line:", line, "\n", e)
                    continue
    except FileNotFoundError:
        print(f"Error: File {filename} not found.")
        sys.exit(1)
    
    print(f"Loaded {len(transversals)} transversals.")
    return transversals

def search_decomposition(transversals, selected, used_cells, start_index):
    global iterations
    iterations += 1
    if iterations % 100000 == 0:
        print(f"Progress: iterations={iterations}, current selected count={len(selected)}")
        
    # check if transversals cover the entire square.
    if len(selected) == n:
        if len(used_cells) == n * n:
            return selected
        return None

    # Try candidates from the current start_index.
    for i in range(start_index, len(transversals)):
        candidate = transversals[i]
        if candidate & used_cells:
            continue
        selected.append(candidate)
        new_used = used_cells | candidate
        result = search_decomposition(transversals, selected, new_used, i + 1)
        if result is not None:
            return result
        selected.pop()
    
    return None

def main():
    global iterations
    transversals = load_transversals("transversals.txt")
    print(f"Starting search for a decomposition into {n} disjoint transversals...")
    solution = search_decomposition(transversals, selected=[], used_cells=set(), start_index=0)
    print(f"Total iterations: {iterations}")
    if solution is not None:
        print("A valid decomposition into distinct transversals was found!")
        for idx, t in enumerate(solution):
            sorted_t = sorted(list(t))
            print(f"Transversal {idx+1}: {sorted_t}")
    else:
        print("No valid transversal decomposition was found.")

if __name__ == "__main__":
    main()