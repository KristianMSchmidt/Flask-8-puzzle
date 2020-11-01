from Puzzle import Puzzle
from utils import convert_solution_string, string_to_grid

# Example 1: 3x3 puzzle
def example_1():
    grid = [[6,3,4],
            [8,5,2],
            [1,7,0]]
    puzzle = Puzzle(3,3, grid) 
    print("New puzzle:\n", puzzle)
    puzzle.update_puzzle("luru")
    print("Puzzle after a few moves:\n", puzzle)
    
    solution_string, cost, num_expanded_nodes, max_search_depth, running_time, max_ram_usage \
        = puzzle.solve_puzzle("gbfs", print_results=True)
    print("Moves to solution:\nn", convert_solution_string(solution_string))
#example_1()

#Example 2: Joe Warrens 4x4-puzzle. 
def example2():
    """
    This is a difficuelt puzzle and the choice of search algorithm now really matterns. 
    It's prof Joe Warrens challenge puzzle of size 4x4. 
    Optimal solution is about 80 moves.
    """    
    Joes_puzzle=Puzzle(4, 4, [[15, 11, 8, 12], \
                                [14, 10, 9, 13], \
                                [2, 6, 1, 4], \
                                [3, 7, 5, 0]])

    #Solve using Gready Best Fist Search. This is really fast (about 0.2s on my machine)
    #but finds a solution w. relatively many moves (206 moves)
    #Joes_puzzle.solve_puzzle("gbfs",print_results=True)

    #Solve using A*-search w. Manhattan heuristics
    #This takes longer time to calculate, but te solution will be shorter (fewer moves)
    Joes_puzzle.solve_puzzle("gbfs", print_results=True)

    #Solve using Breadth First Search
    #Joes_puzzle.solve_puzzle("bfs",print_results=True)
example2()