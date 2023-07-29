import itertools
import time

def get_row_index(index, width):
    row = int(index / width)
    output = []
    for i in range(width):
        value = row * width + i
        output.append(value)
    return output

def get_row(assignment, index, width):
    row_indices = get_row_index(index, width)
    row = [assignment.get(i, None) for i in row_indices]
    return row

def get_col_index(index, height):
    col = index % height
    result = []
    for i in range(height):
        value = col + i * height
        result.append(value)
    return result

def get_col(assignment, index, height):
    col_indices = get_col_index(index, height)
    col = [assignment.get(i, None) for i in col_indices]
    return col

def is_consistent(assignment, index, value, row_clues, col_clues, width, height):
    row = get_row(assignment, index, width)
    col = get_col(assignment, index, height)

    row[index % width] = value
    col[int(index / width)] = value

    row_clue = row_clues[int(index / width)]
    col_clue = col_clues[index % height]

    count_row = [len(list(block_size)) for cell, block_size in itertools.groupby(row) if cell == 1]

    count_col = [len(list(block_size)) for cell, block_size in itertools.groupby(col) if cell == 1]

    if None not in row and count_row != row_clue:
        return False

    if None not in col and count_col != col_clue:
        return False

    return True

def variable_selection_heuristic(domains):
    remaining_values = float('inf')
    selected_index = -1

    for i, domain in enumerate(domains):
        if len(domain) > 1 and len(domain) < remaining_values:
            remaining_values = len(domain)
            selected_index = i

    if selected_index != -1:
        return selected_index
    else:
        return len(domains)

def forward_checking(domains, width, height, row_clues, col_clues, node_counter):
    index = variable_selection_heuristic(domains)

    if index == len(domains):
        return domains, node_counter

    node_counter += 1

    for value in domains[index]:
        assignment = {i: domains[i][0] for i in range(index)}

        if is_consistent(assignment, index, value, row_clues, col_clues, width, height):
            new_domains = [domain.copy() for domain in domains]
            new_domains[index] = [value]

            for i in range(index + 1, len(domains)):
                new_domains[i] = [v for v in domains[i] if is_consistent(assignment, i, v, row_clues, col_clues, width, height)]

            if all(new_domains[i] for i in range(index + 1, len(domains))):
                result, new_node_counter = forward_checking(new_domains, width, height, row_clues, col_clues, node_counter)
                if result:
                    return result, new_node_counter

    return None, node_counter

def nonogram_solver(row_clues, col_clues):
    width = len(col_clues)
    height = len(row_clues)
    domains = []
    for _ in range(width * height):
        domains.append([False, True])

    new_domains, node_counter = forward_checking(domains, width, height, row_clues, col_clues, 0)

    if new_domains:
        assignment = {i: new_domains[i][0] for i in range(len(new_domains))}
        grid = [[assignment[row * width + col] for col in range(width)] for row in range(height)]
        return grid, node_counter
    else:
        print("No solution found")
        return None, node_counter

def main():

    row_clues = [[4], [8], [10], [1, 1, 2, 1, 1], [1, 1, 2, 1, 1], [1, 6, 1], [6], [2, 2], [4], [2]]
    col_clues = [[4], [2], [7], [3, 4], [7, 2], [7, 2], [3, 4], [7], [2], [4]]

    solution, node_counter = nonogram_solver(row_clues, col_clues)

    if solution:
        for row in solution:
            row_str = ""
            for cell in row:
                if cell == 1:
                    row_str += "⬛"
                else:
                    row_str += "⬜"
            print(row_str)
    
    print(f"Nodes: {node_counter}")

start_time = time.time()
main()
print("Time: %s seconds" % (time.time() - start_time))