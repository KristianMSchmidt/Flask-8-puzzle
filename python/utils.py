def convert_solution_string(sol_str):
    """
    Converts eg. 'rdlul' to 'Right Down Left Up Left' 
    """
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
    Takes a grid_string of the kind "[[1,2,3],[4,5,6],[7,8,0]] " and converts it to
    a list of lists [[1,2,3],[4,5,6],[7,8,9]] 
    Assumes that puzzle has size 3x3. 
    """
    grid_string = ''.join(c for c in grid_string if c not in '[]')
    int_list = list(map(int, grid_string.split(",")))
    grid = [[0 for _ in range(3)] for _ in range(3)]
    for row in range(3):
        for col in range(3):
            grid[row][col] = int_list[col + row*3]
    return grid


