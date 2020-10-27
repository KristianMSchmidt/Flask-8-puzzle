from python.Puzzle import Puzzle
from python.utils import string_to_grid, convert_solution_string

p=Puzzle(5,5)
p.update_puzzle("rrrdddlluurrddlll")
print(p)

p.solve_puzzle("ast_naive", print_results = True)