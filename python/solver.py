from Puzzle import Puzzle
from utils import convert_solution_string, string_to_grid

if __name__ == "__main__":
    # Example 1
    p = Puzzle(3,3); p.update_puzzle("rrddlur");
    solution_string, cost, num_expanded_nodes, max_search_depth, running_time, max_ram_usage \
        = p.solve_puzzle("bfs", print_results=True)
    print(convert_solution_string(solution_string))

    #Example 2: Joe Warrens challenge puzzle of size 4x4. Optimal solution is about 80 moves.
    Joes_puzzle=Puzzle(4, 4, [[15, 11, 8, 12], \
                              [14, 10, 9, 13], \
                              [2, 6, 1, 4], \
                              [3, 7, 5, 0]])
    #Joes_puzzle.solve_puzzle("gbfs",print_results=True)
    print(string_to_grid("6,1,8,4,0,2,7,3,5"))