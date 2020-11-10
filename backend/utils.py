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