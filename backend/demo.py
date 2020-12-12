"""
Command-line demo of puzzle class and solution algorithms
"""
from backend.Puzzle import Puzzle

# Example 1: 3x3 puzzle
def example1():
    grid = [[6,3,4],
            [8,5,2],
            [1,7,0]]
    puzzle = Puzzle(3,3, grid) 
    print("New puzzle:\n", puzzle)
    puzzle.update_puzzle("luru")
    print("Puzzle after a few moves:\n", puzzle)

    #Solve puzzle using Breath First Search:
    puzzle.solve_puzzle("bfs", print_results=True)

#Example 2: 4x4-puzzle. 
def example2():
    """
    This is a difficult puzzle and the choice of search algorithm now really matters. 
    Optimal solution is about 80 moves.
    """    
    Joes_puzzle=Puzzle(4, 4, [[15, 11, 8, 12], \
                                [14, 10, 9, 13], \
                                [2, 6, 1, 4], \
                                [3, 7, 5, 0]])

    #Solve using Greedy Best Fist Search. This is really fast (about 0.2s on my machine)
    #but finds a solution w. relatively many moves (206 moves)
    Joes_puzzle.solve_puzzle("gbfs",print_results=True)

    #Solve using A*-search w. Manhattan heuristics
    #This takes longer time to calculate, but te solution will be shorter (fewer moves)
    #Joes_puzzle.solve_puzzle("ast", print_results=True)

if __name__ == "__main__":
    example1()