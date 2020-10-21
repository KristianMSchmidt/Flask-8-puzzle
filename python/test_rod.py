def test_dfs():
    test_puzzle1 = Puzzle(3,3, string_to_grid("6,1,8,4,0,2,7,3,5"))
    test_puzzle2 = Puzzle(3,3, string_to_grid("8,6,4,2,1,3,5,7,0"))
    print("")
    print(":::: Testing Depth First Search :::::")
    print("Test case 1")
    path, depth, num_expanded, max_depth = test_puzzle1.solve_puzzle_dfs()
    print("Calculated", depth, num_expanded, max_depth)
    print( "Expected", 46142, 51015, 46142)
    test_puzzle1.update_puzzle(path)
    print("Puzzle solved?", test_puzzle1.is_solved())
    #print "Correct path_to_goal: ['Up', 'Left', 'Down', ... , 'Up', 'Left', 'Up', 'Left']"

    print("Test case 2")
    path, depth, num_expanded, max_depth = test_puzzle2.solve_puzzle_dfs()
    print("Calculated", depth, num_expanded, max_depth)
    print("Expected", 9612, 9869, 9612)
    test_puzzle2.update_puzzle(path)
    print("Puzzle solved?", test_puzzle2.is_solved())

    #print "Correct path_to_goal is ['Up', 'Up', 'Left', ..., , 'Up', 'Up', 'Left']"
def test_bfs():
    test_puzzle1 = Puzzle(3,3, string_to_grid("6,1,8,4,0,2,7,3,5"))
    test_puzzle2 = Puzzle(3,3, string_to_grid("8,6,4,2,1,3,5,7,0"))
    

    print("")
    print(":::: Testing Bredth First Search :::::")
    print("Test case 1")
    path, depth, num_expanded, max_depth = test_puzzle1.solve_puzzle_bfs()
    print("Calculated", depth, num_expanded, max_depth)
    print("Expected", 20, 54094, 21)
    print("Correct path?", convert_solution_string(path) == ['Down', 'Right', 'Up', 'Up', 'Left', 'Down', 'Right', 'Down', 'Left', 'Up', 'Left', 'Up', 'Right', 'Right', 'Down', 'Down', 'Left', 'Left', 'Up', 'Up'])

    print("Test case 2")
    path, depth, num_expanded, max_depth = test_puzzle2.solve_puzzle_bfs()
    print("Calculated", depth, num_expanded, max_depth)
    print("Expected", 26, 166786, 27)
    print("Correct path?", convert_solution_string(path) == ['Left', 'Up', 'Up', 'Left', 'Down', 'Right', 'Down', 'Left', 'Up', 'Right', 'Right', 'Up', 'Left', 'Left', 'Down', 'Right', 'Right', 'Up', 'Left', 'Down', 'Down', 'Right', 'Up', 'Left', 'Up', 'Left'])

def test_ast():
    test_puzzle1 = Puzzle(3,3, string_to_grid("6,1,8,4,0,2,7,3,5"))
    test_puzzle2 = Puzzle(3,3, string_to_grid("8,6,4,2,1,3,5,7,0"))
    print("")
    print(":::: Testing A* search :::::")
    print("Test case 1")
    path, depth, num_expanded, max_depth = test_puzzle1.solve_puzzle_ast()
    print("Calculated", depth, num_expanded, max_depth)
    print("Expected", 20, "approx 696", 20)
    print("Correct path?", convert_solution_string(path) == ['Down', 'Right', 'Up', 'Up', 'Left', 'Down', 'Right', 'Down', 'Left', 'Up', 'Left', 'Up',
    'Right', 'Right', 'Down', 'Down', 'Left', 'Left', 'Up', 'Up'])
    print("Test case 2")
    path, depth, num_expanded, max_depth = test_puzzle2.solve_puzzle_ast()
    print("Calculated", depth, num_expanded, max_depth)
    print("Expected", 26, "approx 1585", 26)
    print("Correct path?", convert_solution_string(path) == ['Left', 'Up', 'Up', 'Left', 'Down', 'Right', 'Down', 'Left', 'Up', 'Right', 'Right', 'Up', 'Left', 'Left',
     'Down', 'Right', 'Right', 'Up', 'Left', 'Down', 'Down', 'Right',
      'Up', 'Left', 'Up', 'Left'])


    print("")
    print(":::::Testing A* NAIVE implementation:::")
    print("Test case 1")
    path, depth, num_expanded, max_depth = test_puzzle1.solve_puzzle_ast_naive()
    print("Calculated", depth, num_expanded, max_depth)
    print("Expected", 20, "approx 696", 20)
    print("Correct path?", convert_solution_string(path) == ['Down', 'Right', 'Up', 'Up', 'Left', 'Down', 'Right', 'Down', 'Left', 'Up', 'Left', 'Up',
    'Right', 'Right', 'Down', 'Down', 'Left', 'Left', 'Up', 'Up'])

    print("Test case 2")
    path, depth, num_expanded, max_depth = test_puzzle2.solve_puzzle_ast_naive()
    print("Calculated", depth, num_expanded, max_depth)
    print("Expected", 26, "approx 1585", 26)
    print("Correct path?", convert_solution_string(path) == ['Left', 'Up', 'Up', 'Left', 'Down', 'Right', 'Down', 'Left', 'Up', 'Right', 'Right', 'Up', 'Left', 'Left',
     'Down', 'Right', 'Right', 'Up', 'Left', 'Down', 'Down', 'Right',
      'Up', 'Left', 'Up', 'Left'])





def test_ast_versions():
    import random
    p = Puzzle(3, 3)

    for i in range(1000):
        direction = random.choice(p.valid_directions())
        p.update_puzzle(direction)

    p_copy1 = p.clone()
    p_copy2 = p.clone()
    p_copy3 = p.clone()

    print("")
    print(":::: Testing 3 different A*search implementations :::")
    print("Sloppy version:", p_copy1.solve_puzzle_ast())
    print("More strict version:", p_copy2.solve_puzzle_ast_alternative())
    print("Naive, slow strict version:", p_copy2.solve_puzzle_ast_naive())
    print("I don't know why the to last versions are any different in output")

def solve_assignment():
    """
    This function is called, when script is run from command prompt with input of the kind:
    $ python driver.py <method> <board>
    Example given:
    $ python driver.py bfs 0,8,7,6,5,4,3,2,1
    It solves the puzzle with the specified search and writes data to the file output.txt
    """
    method = sys.argv[1]
    initial_grid = string_to_grid(sys.argv[2])
    P = Puzzle(3, 3, initial_grid)
    solution_string, cost, num_expanded_nodes, max_search_depth, running_time, max_ram_usage = P.solve_puzzle(method, False)
    running_time = "{0:.8f}".format(running_time)
    max_ram_usage = "{0:.8f}".format(max_ram_usage)

    fh = open('output.txt', 'w')
    fh.write("path_to_goal: {}\n".format(convert_solution_string(solution_string)))
    fh.write("cost_of_path: {}\n".format(cost))
    fh.write("nodes_expanded: {}\n".format(num_expanded_nodes))
    fh.write("search_depth: {}\n".format(cost))
    fh.write("max_search_depth: {}\n".format(max_search_depth))
    fh.write("running_time: {}\n".format(running_time))
    fh.write("max_ram_usage: {}\n".format(max_ram_usage))
    fh.close()

    # Sneak preview output to txt file
    print ("path_to_goal: {}\n".format(convert_solution_string(solution_string)))
    print ("cost_of_path: {}\n".format(cost))
    print ("nodes_expanded: {}\n".format(num_expanded_nodes))
    print ("search_depth: {}\n".format(cost))
    print ("max_search_depth: {}\n".format(max_search_depth))
    print ("running_time: {}\n".format(running_time))
    print ("max_ram_usage: {}\n".format(max_ram_usage))