"""
Part of udacity AI Nanodegree

Parameters
----------
grid : string
    The sudoku puzzle to solve, left to right, top to bottom

Returns
-------
dictionary
    Dictionary representation of the solved sudoku puzzle, False if unsuccessful

"""
ASSIGNMENTS = []

ROWS = 'ABCDEFGHI'
COLS = '123456789'


def cross(matrix_a, matrix_b):
    "Cross product of elements in A and elements in B."
    return [s + t for s in matrix_a for t in matrix_b]


BOXES = cross(ROWS, COLS)

ROW_UNITS = [cross(r, COLS) for r in ROWS]
COLUMN_UNITS = [cross(ROWS, c) for c in COLS]
SQUARE_UNITS = [cross(rs, cs) for rs in ('ABC', 'DEF', 'GHI')
                for cs in ('123', '456', '789')]

DIAG_UNITS = [[s + COLS[idx] for idx, s in enumerate(ROWS)]]
DIAG_UNITS.append([s + COLS[len(COLS) - (idx + 1)]
                   for idx, s in enumerate(ROWS)])
UNITLIST = ROW_UNITS + COLUMN_UNITS + SQUARE_UNITS + DIAG_UNITS
UNITS = dict((s, [u for u in UNITLIST if s in u]) for s in BOXES)
PEERS = dict((s, set(sum(UNITS[s], [])) - set([s])) for s in BOXES)


def assign_value(values, box, value):
    """
    Please use this function to update your values dictionary!
    Assigns a value to a given box. If it updates the board record it.
    """

    # Don't waste memory appending actions that don't actually change any
    # values
    if values[box] == value:
        return values

    values[box] = value
    if len(value) == 1:
        ASSIGNMENTS.append(values.copy())
    return values


def naked_twins(values):
    import pdb

    """Eliminate values using the naked twins strategy.
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}

    Returns:
        the values dictionary with the naked twins eliminated from peers.
    """
    # Find all instances of naked twins
    # A naked twin - when a box has two possible values, and there is another box in the same
    # unit with only the same two possibilities
    # print("INPUT")
    # display(values)
    # print("//////////////////////")
    # two_remain = [box for box in BOXES if len(values[box]) == 2]
    # for box in two_remain:
    #     flatten = {item for sublist in UNITS[box] for item in sublist if values[
    #         item] == values[box] and item != box}

    #     if len(flatten) == 1:
    #         # Eliminate the naked twins as possibilities for their peers
    #         twin = flatten.pop()
    #         kill_list = {target for target in PEERS if target !=
    #                      box and target != twin}
    #         for target in kill_list:
    #             # if "2" in values[target]:
    #             #     import pdb; pdb.set_trace()
    #             values = assign_value(values, target, ''.join(
    #                 c for c in values[target] if c not in values[twin]))
    #     # flatten = {item for item in }
    #     # print("Box", box, values[box])
    #     # for b in flatten:
    #     #     print(b, values[b])

    # print("OUTPUT")
    # display(values)
    # print("//////////////////////")
    # return values
    # for unit_key in UNITS.keys():
    #     for unit in UNITS[unit_key]:
    #         print(unit_key,unit)
    for unit in UNITLIST:
        two_remain = [box for box in unit if len(values[box]) == 2]
        pairs = [box for box in two_remain if len([b for b in two_remain if values[box] == values[b]]) == 2]
        if len(pairs) == 2:
            # Naked twins found, eliminate their values from all others in the unit
            targets = [box for box in unit if box not in pairs]
            for box in targets:
                values = assign_value(values,box, ''.join(ch for ch in values[box] if ch not in values[pairs[0]]))                
    return values

def grid_values(grid):
    """
    Convert grid into a dict of {square: char} with '123456789' for empties.
    Args:
        grid(string) - A grid in string form.
    Returns:
        A grid in dictionary form
            Keys: The boxes, e.g., 'A1'
            Values: The value in each box, e.g., '8'.
            If the box has no value, then the value will be '123456789'.
    """
    chars = []
    digits = '123456789'
    for character in grid:
        if character in digits:
            chars.append(character)
        if character == '.':
            chars.append(digits)
    assert len(chars) == 81
    return dict(zip(BOXES, chars))


def display(values):
    """
    Display the values as a 2-D grid.
    Args:
        values(dict): The sudoku in dictionary form
    """
    width = 1 + max(len(values[s]) for s in BOXES)
    line = '+'.join(['-' * (width * 3)] * 3)
    for row in ROWS:
        print(''.join(values[row + c].center(width) + ('|' if c in '36' else '')
                      for c in COLS))
        if row in 'CF':
            print(line)
    return


def eliminate(values):
    """
    Go through all the boxes, and whenever there is a box with a value,
    eliminate this value from the values of all its peers.
    Input: A sudoku in dictionary form.
    Output: The resulting sudoku in dictionary form.
    """
    solved_values = [box for box in values.keys() if len(values[box]) == 1]
    for box in solved_values:
        digit = values[box]
        for peer in PEERS[box]:
            #values[peer] = values[peer].replace(digit, '')
            values = assign_value(values, peer, values[
                                  peer].replace(digit, ''))
    return values


def only_choice(values):
    """
    Go through all the units, and whenever there is a unit with a value
    that only fits in one box, assign the value to this box.
    Input: A sudoku in dictionary form.
    Output: The resulting sudoku in dictionary form.
    """
    for unit in UNITLIST:
        for digit in '123456789':
            dplaces = [box for box in unit if digit in values[box]]
            if len(dplaces) == 1:
                #values[dplaces[0]] = digit
                values = assign_value(values, dplaces[0], digit)
    return values


def reduce_puzzle(values):
    """
    Iterate eliminate() and only_choice(). If at some point,
    there is a box with no available values, return False.
    If the sudoku is solved, return the sudoku.
    If after an iteration of both functions, the sudoku remains the same, return the sudoku.
    Input: A sudoku in dictionary form.
    Output: The resulting sudoku in dictionary form.
    """
    solved_values = [box for box in values.keys() if len(values[box]) == 1]
    stalled = False
    while not stalled:
        solved_values_before = len(
            [box for box in values.keys() if len(values[box]) == 1])
        values = eliminate(values)
        values = only_choice(values)
        solved_values_after = len(
            [box for box in values.keys() if len(values[box]) == 1])
        stalled = solved_values_before == solved_values_after
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
    return values


def search(values):
    "Using depth-first search and propagation, create a search tree and solve the sudoku."
    # First, reduce the puzzle using the previous function
    values = reduce_puzzle(values)

    if values is False:
        return False

    if all(len(values[s]) == 1 for s in BOXES):
        return values

    n, s = min((len(values[s]), s) for s in BOXES if len(values[s]) > 1)

    for value in values[s]:
        new_sudoku = values.copy()
        new_sudoku[s] = value
        attempt = search(new_sudoku)
        if attempt:
            return attempt


def solve(grid):
    """
    Find the solution to a Sudoku grid.
    Args:
        grid(string): a string representing a sudoku grid.
            Example: '2.............62....1....7...6..8...3...9...7...6..
            4...4....8....52.............3'
    Returns:
        The dictionary representation of the final sudoku grid. False if no solution exists.
    """
    initial_values = grid_values(grid)
    return search(initial_values)


if __name__ == '__main__':
    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    display(solve(diag_sudoku_grid))
    # for idx, val in enumerate(ROWS):
    #     print(idx, val)
    try:
        from visualize import visualize_assignments
        visualize_assignments(ASSIGNMENTS)

    except SystemExit:
        pass
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')
