def convert_solution_string(sol_str):
    path_to_goal = []
    for index, letter in enumerate(sol_str):
        if letter == "u":
            path_to_goal.append("Up")
        elif letter == "d":
            path_to_goal.append("Down")
        elif letter == "l":
            path_to_goal.append("Left")
        else:
            path_to_goal.append("Right")
    return path_to_goal

def string_to_grid(grid_string):
    """
    Helper function to use when initial board is given as string.
    Assumes that puzzle has size 3x3.
    """
    input_state = list(map(int, grid_string.split(",")))
    grid = [[0 for _ in range(3)] for _ in range(3)]

    for row in range(3):
        for col in range(3):
            grid[row][col] = input_state[col + row*3]
    return grid
