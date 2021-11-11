"""
Unittesting of Puzzle class methods.
"""
import unittest
from Puzzle import Puzzle
from puzzle_collection import eight_puzzles
from heapq import heappush, heappop
import time

do_slow_tests = True

class Test_simple_methods(unittest.TestCase):

    def test_current_position(self):
        p = Puzzle(3,3)
        self.assertEqual(p.current_position(0,0), (0,0))
        self.assertEqual(p.current_position(0,1), (0,1))
        self.assertEqual(p.current_position(2,1), (2,1))
        p._grid = [
            [1,0,2],
            [8,4,5],
            [6,7,3]
        ]
        self.assertEqual(p.current_position(0,0), (0,1))
        self.assertEqual(p.current_position(0,1), (0,0))
        self.assertEqual(p.current_position(1,0), (2,2))
        self.assertEqual(p.current_position(2,2), (1,0))
    
    def test_manhattan_distance(self):        
        p = Puzzle(3,3)
        self.assertEqual(p.manhattan_dist(), 0)   # Manhattan distance of solved puzzle should be 0.
        
        p._grid = [
            [1,0,2],
            [3,4,5],
            [6,7,8]
        ]
        self.assertEqual(p.manhattan_dist(), 1) 
        
        p._grid = [
            [2,1,0],
            [3,4,5],
            [6,7,8]
        ]
        self.assertEqual(p.manhattan_dist(), 2) 
        
        p._grid = [
            [2,0,1],
            [3,4,5],
            [6,7,8]
        ]
        self.assertEqual(p.manhattan_dist(), 3) 
        
        p._grid = [
            [6,1,2],
            [3,4,5],
            [0,7,8]
        ]
        self.assertEqual(p.manhattan_dist(), 2) 
        
        p._grid = [
            [6,1,2],
            [3,7,5],
            [0,4,8]
        ]
        self.assertEqual(p.manhattan_dist(), 4) 
        
        p._grid = [
            [6,1,2],
            [3,7,5],
            [0,4,8]
        ]
        self.assertEqual(p.manhattan_dist(), 4) 
        
        p._grid = [
            [6,8,7],
            [3,1,2],
            [4,0,5]
        ]
        expected = 2 + 3 + 3 + 0 + 1 + 1 + 2 + 0 + 1      # = 13

        self.assertEqual(p.manhattan_dist(), expected) 
        
        p._grid = [
            [8,7,6],
            [1,4,2],
            [5,3,0]
        ]
        expected = 4 + 2 + 4 + 2 + 0 + 1 + 3 + 2    # = 18
        self.assertEqual(p.manhattan_dist(), expected) 
        
    def test_heap(self):
        """ 
        Just a test that I understand exactly how heappush of heappop works
        heappop should return the minimal element in the set
        
        """
        frontier = [] 
        heappush(frontier, (0, 0))
        heappush(frontier, (0, 1))
        self.assertEqual(heappop(frontier), (0, 0))
        self.assertEqual(heappop(frontier), (0, 1))

        frontier = [] 
        heappush(frontier, (0, 1))
        heappush(frontier, (0, 0))
        self.assertEqual(heappop(frontier), (0, 0))
        self.assertEqual(heappop(frontier), (0, 1))
        
        
        p0 = Puzzle(3,3)
        p1 = Puzzle(3,3)
        p2 = Puzzle(3,3)
        p3 = Puzzle(3,3)
        p4 = Puzzle(3,3)

        frontier = [] 
        heappush(frontier, (0, p0))
        heappush(frontier, (1, p1))
        heappush(frontier, (2, p2))
        heappush(frontier, (3, p3))
        heappush(frontier, (4, p4))
        self.assertEqual(heappop(frontier), (0, p0))
        self.assertEqual(heappop(frontier), (1, p1))
        self.assertEqual(heappop(frontier), (2, p2))
        self.assertEqual(heappop(frontier), (3, p3))
        self.assertEqual(heappop(frontier), (4, p4))
        
        frontier = [] 
        heappush(frontier, (4, p0))
        heappush(frontier, (3, p1))
        heappush(frontier, (2, p2))
        heappush(frontier, (1, p3))
        heappush(frontier, (0, p4))
        self.assertEqual(heappop(frontier), (0, p4))
        self.assertEqual(heappop(frontier), (1, p3))
        self.assertEqual(heappop(frontier), (2, p2))
        self.assertEqual(heappop(frontier), (3, p1))
        self.assertEqual(heappop(frontier), (4, p0))

        
    def test_update_puzzle(self):
        p = Puzzle(3,3)
        self.assertEqual(p._grid[0][0], 0)
        self.assertEqual(p._grid[0][1], 1)
        p.update_puzzle('r')
        self.assertEqual(p._grid[0][0], 1)
        self.assertEqual(p._grid[0][1], 0)
        self.assertEqual(p._grid[0][2], 2)
        p.update_puzzle('r')
        self.assertEqual(p._grid[0][0], 1)
        self.assertEqual(p._grid[0][1], 2)
        self.assertEqual(p._grid[0][2], 0)
        p.update_puzzle('dd')
        self.assertEqual(p._grid[0][0], 1)
        self.assertEqual(p._grid[0][1], 2)
        self.assertEqual(p._grid[0][2], 5)
        self.assertEqual(p._grid[1][2], 8)
        self.assertEqual(p._grid[2][2], 0)
        p.update_puzzle('lu')
        self.assertEqual(p._grid[0][0], 1)
        self.assertEqual(p._grid[0][1], 2)
        self.assertEqual(p._grid[0][2], 5)
        self.assertEqual(p._grid[1][2], 8)
        self.assertEqual(p._grid[2][2], 7)
        self.assertEqual(p._grid[2][1], 4)
        self.assertEqual(p._grid[1][1], 0)
        expected = [
            [1,2,5],
            [3,0,8],
            [6,4,7]
            ]
        self.assertEqual(p._grid, expected)
        
    def test_valid_directions(self):
        # up, down, left, right
        p = Puzzle(3,3)
        self.assertEqual(p.valid_directions(), ["d", "r"])
        p._grid = [
            [1,2,5],
            [3,0,8],
            [6,4,7]
            ]
        self.assertEqual(p.valid_directions(), ["u", "d", "l", "r"])

        p._grid = [
            [1,0,5],
            [3,4,8],
            [6,4,7]
            ]
        self.assertEqual(p.valid_directions(), ["d", "l", "r"])
        
        p._grid = [
            [1,4,0],
            [3,0,8],
            [6,4,7]
            ]
        self.assertEqual(p.valid_directions(), ["d", "l"])
        
        p._grid = [
            [1,4,3],
            [3,2,8],
            [6,4,0]
            ]
        self.assertEqual(p.valid_directions(), ["u", "l"])
        
        p._grid = [
            [1,4,3],
            [3,2,8],
            [0,4,5]
            ]
        self.assertEqual(p.valid_directions(), ["u", "r"])
        
        p._grid = [
            [1,4,3],
            [0,2,8],
            [3,4,5]
            ]
        self.assertEqual(p.valid_directions(), ["u", "d", "r"])

    def test_recover_path(self):
        p = Puzzle(4,4) # start out with initial grid = solved grid
        p1 = p.clone()
        p1.update_puzzle("r")
        p1._last_move = "r"
        p1._parent = p
        self.assertEqual("r", p1.recover_path())
        p2 = p1.clone()
        p2.update_puzzle("d")
        p2._last_move = "d"
        p2._parent = p1
        self.assertEqual("rd", p2.recover_path())
        p3 = p2.clone()
        p3.update_puzzle("d")
        p3._last_move = "d"
        p3._parent = p2
        self.assertEqual("rdd", p3.recover_path())
        p = Puzzle(3,3, [[1,2,3],[4,5,6],[7,9,0]]) # start out other initial grid
        p1 = p.clone()
        p1.update_puzzle("l")
        p1._last_move = "l"
        p1._parent = p
        self.assertEqual("l", p1.recover_path())
        p2 = p1.clone()
        p2.update_puzzle("l")
        p2._last_move = "l"
        p2._parent = p1
        self.assertEqual("ll", p2.recover_path())
        p3 = p2.clone()
        p3.update_puzzle("u")
        p3._last_move = "u"
        p3._parent = p2
        self.assertEqual("llu", p3.recover_path())

    def test_is_solved(self):
        p = Puzzle(4,4)
        self.assertTrue(p.is_solved())
        p = Puzzle(4,4)
        p.update_puzzle("ddr")
        self.assertFalse(p.is_solved())

if do_slow_tests:
    class Test_DFS(unittest.TestCase):
        #Recall that algorithm search in this prefered order of directions u,d,l,r

        def test_solve_puzzle_dfs(self):
            #Let's start out by testing a puzzle, that is already solved.
            p = Puzzle(3,3) 
            path_to_goal, num_expanded_nodes, max_search_depth = p.solve_puzzle_dfs()
            self.assertTrue(p.is_solved)
            self.assertEqual(path_to_goal, "")
            self.assertEqual(max_search_depth, 0)
            self.assertEqual(num_expanded_nodes, 0)
            
            #Now a more interesting example
            #Because of the search order (udlr), depth-first search should be lucky to immediately find the easy solution here. 
        
            p = Puzzle(3,3)
            p._grid = [
                [3,1,2],
                [6,4,5],
                [0,7,8]
            ]
            path_to_goal, num_expanded_nodes, max_search_depth = p.solve_puzzle_dfs()
            self.assertTrue(p.is_solved)
            self.assertEqual(path_to_goal, "uu")
            self.assertEqual(max_search_depth, 2)
            self.assertEqual(num_expanded_nodes, 2)
            
            #
            # #Because of the search order (udlr), depth-first search should be lucky to immediately find the easy solution here. 
            p = Puzzle(3,3)
            p._grid = [
                [1,4,2],
                [3,7,5],
                [6,0,8]
            ]
            path_to_goal, num_expanded_nodes, max_search_depth = p.solve_puzzle_dfs()
            self.assertTrue(p.is_solved)
            self.assertEqual(path_to_goal, "uul")  
            self.assertEqual(max_search_depth, 3)
            self.assertEqual(num_expanded_nodes, 3)
            
            
            #Now, let's simply test that all eightpuzzles are solved - plus some basic sanity control
            for grid in eight_puzzles: 
                puzzle = Puzzle(3,3, grid)
                path_to_goal, num_expanded_nodes, max_search_depth = puzzle.solve_puzzle_dfs()
                self.assertTrue(p.is_solved)
                self.assertTrue(len(path_to_goal) > 0)
                self.assertTrue(max_search_depth >= len(path_to_goal))
                self.assertTrue(num_expanded_nodes >= max_search_depth)

    class Test_BFS(unittest.TestCase):
        #Recall that algorithm search in this prefered order of directions u,d,l,r

        def test_solve_puzzle_bfs(self):
            #Let's start out by testing a puzzle, that is already solved.
            p = Puzzle(3,3) 
            path_to_goal, num_expanded_nodes, max_search_depth = p.solve_puzzle_bfs()
            self.assertTrue(p.is_solved)
            self.assertEqual(path_to_goal, "")
            self.assertEqual(max_search_depth, 0)
            self.assertEqual(num_expanded_nodes, 0)
            
            p = Puzzle(3,3)
            p._grid = [
                [3,1,2],
                [6,4,5],
                [0,7,8]
            ]
            path_to_goal, num_expanded_nodes, max_search_depth = p.solve_puzzle_bfs()
            self.assertTrue(p.is_solved)
            self.assertEqual(path_to_goal, "uu")
        
            
            p = Puzzle(3,3)
            p._grid = [
                [1,4,2],
                [3,7,5],
                [6,0,8]
            ]
            path_to_goal, num_expanded_nodes, max_search_depth = p.solve_puzzle_bfs()
            self.assertTrue(p.is_solved)
            self.assertEqual(path_to_goal, "uul")  
            
            
            #Now, let's simply test that all eightpuzzles are solved - plus some basic sanity control
            for grid in eight_puzzles: 
                puzzle = Puzzle(3,3, grid)
                path_to_goal, num_expanded_nodes, max_search_depth = puzzle.solve_puzzle_bfs()
                self.assertTrue(puzzle.is_solved)
                self.assertTrue(len(path_to_goal) > 0)
                self.assertTrue(max_search_depth >= len(path_to_goal))
                self.assertTrue(num_expanded_nodes >= max_search_depth)
    
    class Test_GBFS(unittest.TestCase):
       
        def test_solve_puzzle_gbfs(self):
            #Let's start out by testing a puzzle, that is already solved.
            p = Puzzle(3,3) 
            path_to_goal, num_expanded_nodes, max_search_depth = p.solve_puzzle_gbfs()
            self.assertTrue(p.is_solved)
            self.assertEqual(path_to_goal, "")
            self.assertEqual(max_search_depth, 0)
            self.assertEqual(num_expanded_nodes, 0)
            
            #Now, let's simply test that all eightpuzzles are solved - plus some basic sanity control
            for grid in eight_puzzles: 
                puzzle = Puzzle(3,3, grid)
                path_to_goal, num_expanded_nodes, max_search_depth = puzzle.solve_puzzle_gbfs()
                self.assertTrue(puzzle.is_solved)
                self.assertTrue(len(path_to_goal) > 0)
                self.assertTrue(max_search_depth >= len(path_to_goal))
                self.assertTrue(num_expanded_nodes >= max_search_depth)
    
    class Test_AST(unittest.TestCase):
            
        def test_solve_puzzle_ast(self):
            #Let's start out by testing a puzzle, that is already solved.
            p = Puzzle(3,3) 
            path_to_goal, num_expanded_nodes, max_search_depth = p.solve_puzzle_ast()
            self.assertTrue(p.is_solved)
            self.assertEqual(path_to_goal, "")
            self.assertEqual(max_search_depth, 0)
            self.assertEqual(num_expanded_nodes, 0)
            start_time = time.time()
            #Now, let's simply test that all eightpuzzles are solved - plus some basic sanity control
            for grid in eight_puzzles: 
                puzzle = Puzzle(3,3, grid)
                path_to_goal, num_expanded_nodes, max_search_depth = puzzle.solve_puzzle_ast()
                self.assertTrue(puzzle.is_solved)
                self.assertTrue(len(path_to_goal) > 0)
                self.assertTrue(max_search_depth >= len(path_to_goal))
                self.assertTrue(num_expanded_nodes >= max_search_depth)
            #print(time.time() - start_time)
if __name__ == '__main__':
    unittest.main()
    

    


