import time, queue, psutil
from heapq import heappush, heappop

class Puzzle:
    """
    Class that holds state of puzzle, methods for moving tiles and methods for solving the puzzle
    with various search strategies. Puzzle can be of any height and width. If no initial grid is given
    the puzzle is initialized its solved state.
    """
    def __init__(self, puzzle_height, puzzle_width, initial_grid = None,
                last_move = "", search_depth = 0, parent = None):
        self._last_move = last_move # Only counting moves that are part of solution proces
        self._search_depth = search_depth
        self._height = puzzle_height
        self._width = puzzle_width
        self._parent = parent
        self._grid = [[col + puzzle_width * row
                       for col in range(self._width)]
                      for row in range(self._height)]
        if initial_grid != None:
           for row in range(puzzle_height):
               for col in range(puzzle_width):
                   self._grid[row][col] = initial_grid[row][col]

    def __str__(self):
        """
        String representaion for puzzle
        """
        ans = ""
        for row in range(self._height):
            ans += str(self._grid[row])
            ans += "\n"
        return ans
    
    def __lt__(self, other):
        """
        Formal size comparison of puzzles. 
        Needed for heappush and heappop to be stable.
        """
        return self
                 
    def clone(self):
        """
        Make a copy of the puzzle to update during solving
        Returns a Puzzle object
        """
        new_puzzle = Puzzle(self._height, self._width, self._grid, self._last_move, 
                            self._search_depth, self._parent)
        return new_puzzle

    ########################################################
    # Core puzzle methods

    def current_position(self, solved_row, solved_col):
        """
        Locate the current position of the tile that will be at
        position (solved_row, solved_col) when the puzzle is solved
        Returns a tuple of two integers.
        """
        solved_value = (solved_col + self._width * solved_row)

        for row in range(self._height):
            for col in range(self._width):
                if self._grid[row][col] == solved_value:
                    return (row, col)
        assert False, "Value " + str(solved_value) + " not found"

    def update_puzzle(self, move_string):
        """
        Updates the puzzle state based on the provided move string
        """
        zero_row, zero_col = self.current_position(0, 0)
        for direction in move_string:
            if direction == "l":
                assert zero_col > 0, "move off grid: " + direction
                self._grid[zero_row][zero_col] = self._grid[zero_row][zero_col - 1]
                self._grid[zero_row][zero_col - 1] = 0
                zero_col -= 1
            elif direction == "r":
                assert zero_col < self._width - 1, "move off grid: " + direction
                self._grid[zero_row][zero_col] = self._grid[zero_row][zero_col + 1]
                self._grid[zero_row][zero_col + 1] = 0
                zero_col += 1
            elif direction == "u":
                assert zero_row > 0, "move off grid: " + direction
                self._grid[zero_row][zero_col] = self._grid[zero_row - 1][zero_col]
                self._grid[zero_row - 1][zero_col] = 0
                zero_row -= 1
            elif direction == "d":
                assert zero_row < self._height - 1, "move off grid: " + direction
                self._grid[zero_row][zero_col] = self._grid[zero_row + 1][zero_col]
                self._grid[zero_row + 1][zero_col] = 0
                zero_row += 1
            else:
                assert False, "invalid direction: " + direction

    ##################################################################
    # Methods for puzzle solving

    def valid_directions(self):
        """
        Returns list of possible (and sound) directions to move in - in "UDLR" (up, down, left, right) order
        """
        zero_row, zero_col = self.current_position(0, 0)

        last_move = self._last_move

        valid_directions = []

        if zero_row > 0 and last_move != "d":
            valid_directions.append("u")
        if zero_row < self._height - 1 and last_move != "u":
            valid_directions.append("d")
        if zero_col > 0 and last_move != "r":
            valid_directions.append("l")
        if zero_col < self._width - 1 and last_move != "l":
            valid_directions.append("r")
        return valid_directions

    def recover_path(self):
        """
        Recovers path taken from startnode to the node in question.
        """
        reverse_path_to_goal = ""
        node = self
        while node._last_move != "":
            reverse_path_to_goal += node._last_move
            node = node._parent
        path_to_goal = reverse_path_to_goal[::-1] #reverse order
        return path_to_goal

    def is_solved(self):
        """
        Cheks is self is the desired goal_state
        """
        #This is the general code that works for all grid sizes:
        for row in range(self._height):
            for col in range(self._width):
               if self._grid[row][col] != col + self._width * row:
                   return False
        return True
    
    def solve_puzzle_bfs(self):
        """
        Solves the puzzle using Breadth-First search. 
        
        The search does not use any heuristics, so it is "stupid" uninformed serach. 
        
        Implementation is almost identical to the Depth-First-Search below, but using a queue
        (first in-first out) rather that a stack ensures breadth-first quality of the search.        
        By it's very nature, breath-first search is guaranteed to find the shortest possible 
        solution (however not in the shortest possible time).  
        """
        frontier = queue.Queue() #q.put(x), q.get_nowait()
        frontier.put(self)

        # Set of board positions that are already in frontier/queue or have been there earlier. I use
        # a set datastructure for fast lookups
        in_frontier_or_explored = set([str(self._grid)])

        num_expanded_nodes = 0  #Total number of nodes, that have been in focus of attention
                                #I.e. the nodes whose solution_state has been checked and whose
                                #children has been added to the queue
        max_search_depth = 0

        while not frontier.empty():
            #Remove node from queue
            node = frontier.get(False)
            #print(node.recover_path())
      

            #Check if solution is found
            if node.is_solved():
                path_to_goal = node.recover_path()
                return path_to_goal, num_expanded_nodes, max_search_depth

            # Expand the node.
            #   To expand a given node, we generate successor nodes adjacent to the current node, and add them to the
            #   frontier set. Note that if these successor nodes are already in the frontier, or have already been
            #   visited, then they should not be added to the frontier again.
            num_expanded_nodes += 1
            valid_directions = node.valid_directions()
            for direction in valid_directions:
                #Enqueue in UDLR order; dequeuing results in UDLR order
                child = node.clone()
                child.update_puzzle(direction)
                child_game_state = str(child._grid)
                child._search_depth += 1

                if child_game_state in in_frontier_or_explored:
                    continue
                    # note that we can safely skip further search from current node, 
                    # as the previous time we had the same game state, the node had 
                    # lower search depth than the current node (because of breath-first-search)
                child._last_move = direction
                child._parent = node
                frontier.put(child)
                in_frontier_or_explored.add(child_game_state)

            #Check current search depth:
            current_search_depth = node._search_depth + 1

            if current_search_depth > max_search_depth:
                max_search_depth = current_search_depth


    def solve_puzzle_dfs(self):
        """
        Solves the puzzle using Depth-First Search. No heuristics used. 
        
        Search is implemented with a stack (last-in first-out).
        
        Please note that depth-first search is really a quite stupid search strategy for
        solving puzzles of this type - I only implement it to compare results with better algorithms. 
        """
        # Initialize stack (I use list datastructure to do this)
        stack = [self]  # the stack is "the frontier"

        # Set of board positions that are already in frontier/queue or have been there earlier. I use
        # a set datastructure for fast lookups
        in_frontier_or_explored = set([str(self._grid)])

        num_expanded_nodes = 0  #Total number of nodes, that have been in focus of attention
                                #I.e. the nodes whose solution_state has been checked and whose
                                #children has been added to the stack
        max_search_depth = 0
        count = 0
        
        while stack:
            # Remove node from stack
            node = stack.pop()   # pop returns (and deletes) the last element in the list 
            #print(node._search_depth)
            #print(node.recover_path())
      

            #Check if solution is found
            if node.is_solved():
                path_to_goal = node.recover_path()
                return path_to_goal, num_expanded_nodes, max_search_depth

            # Expand the node.
            #   To expand a given node, we generate successor nodes adjacent to the current node, and add them to the
            #   frontier set. Note that if these successor nodes are already in the frontier, or have already been
            #   visited, then they should not be added to the frontier again.

            num_expanded_nodes += 1

            valid_directions = node.valid_directions()
         
            #Push onto the stack in reverse-UDLR order; popping off results in UDLR order.
            for direction in reversed(valid_directions):
               
                child = node.clone()
                child.update_puzzle(direction)
                child_game_state = str(child._grid)
                child._search_depth += 1  
                current_search_depth = child._search_depth 

                if child_game_state in in_frontier_or_explored:
                    # Note that we discard the child if the game state is already being explored even
                    # if the search-depth of the current child might be shorter. 
                    # It wouldn't be too difficult to change this, but it would make
                    # the algorithm slower.  
                    continue
                
                # One one easily add a condition like this to stop search depths from being ridiculously long.
                # I could also make the depth first serach iterative, will still longer max-depths (as in 
                # my implementation of 2048-game. However, for now, I would like the depth first search
                # to bee really vanilla depth first search to see the extreme case.)
                #if current_search_depth > 200:
                 #   continue
             
                child._last_move = direction
                child._parent = node
                stack.append(child)
                in_frontier_or_explored.add(child_game_state)

            if current_search_depth > max_search_depth:
                max_search_depth = current_search_depth
            
    
    def manhattan_dist(self):
        """
        Computes the total manhattan-distance between the given puzzle and the solved game state.
        This is a measure for how close the current puzzle is to being solved. 
        For each tile in grid, calcute how many moves it would take to get the tile to its 
        right position. Add it all up.        
        """
        answer = 0
        for row in range(self._height):
            for col in range(self._width):
                if not (row, col) == (0, 0):  #zero-tile should not be part of the sum
                    current_row, current_col = self.current_position(row, col)
                    answer += abs(col-current_col) + abs(row - current_row)
        return answer
    
    def solve_puzzle_gbfs(self):
        """
        Solves the puzzle using greedy_best_first_search with Manhattan-heuristics.
        
        Gready-best search simply chooses to follow the nodes, which at any given time
        looks most promissing (closest to solved state from current state). It does not care about how long
        the final solution will be. 
        
        The found solution will be short (not necessarily the shortest) and found in very short time.
        """
        frontier = [] # The "frontier". I use heap to do fast extract minimums
        heappush(frontier, (self.manhattan_dist(), self))
        max_search_depth = 0
        num_expanded_nodes = 0  #Total number of nodes, that have been in focus of attention
                                #I.e. the nodes whose solution_state has been checked and whose
                                #children has been added to the stack
        
        # Set of board positions that are already in frontier/queue or have been there earlier. I use
        # a set datastructure for fast lookups
        in_frontier_or_explored = set([str(self._grid)])

        while frontier:
            #Remove node from heap
            _, node = heappop(frontier) #heappop pics node with least Manhattan distance to the solved state
                                        # Note that this algorithm does not care about how many
                                        # moves have already been used to get to the current state. It's just
                                        # about getting to the goal in as few moves as possible from NOW.
                                        # This is the "greedy best-first" quality of the search
            #print(node.recover_path())
      

            #Check if solution is found
            if node.is_solved():
                path_to_goal = node.recover_path()
                return path_to_goal, num_expanded_nodes, max_search_depth
            
            #Add node-grid to closed set 
            in_frontier_or_explored.add(str(node._grid))
            
            # Expand the node.
            #   To expand a given node, we generate successor nodes adjacent to the current node, and add them to the
            #   frontier set. Note that if these successor nodes are already in the frontier, or have already been
            #   visited, then they should not be added to the frontier again.
            num_expanded_nodes += 1
            valid_directions = node.valid_directions()
            for direction in valid_directions:
                child = node.clone()
                child.update_puzzle(direction)
                child_game_state = str(child._grid)

                if child_game_state in in_frontier_or_explored: 
                    # already met a node with this grid
                    continue

                child._last_move = direction
                child._search_depth += 1
                child._parent = node
                heappush(frontier, (child.manhattan_dist(), child))
                in_frontier_or_explored.add(child_game_state)
                # Note that I add each child to the heap/frontier if it is not in the closed
                # list (this makes the heap quite long)

            # Update current search depth:
            current_search_depth = node._search_depth + 1

            if current_search_depth > max_search_depth:
                max_search_depth = current_search_depth


    def solve_puzzle_ast(self):
        """
        Solves the puzzle using A*-search with Manhattan distance heuristic.
        
        Like breath-first search, this is guaranteed to find the shortest path to the solved state. 
        And it it is pretty fast in most cases. 
                
        From wiki: 
        "At each iteration of its main loop, A* needs to determine which of its paths
        to extend. It does so based on the cost of the path and an estimate of the cost required
        to extend the path all the way to the goal. Specifically, A* selects the path that minimizes
        f(n)=g(n)+h(n)
        where n is the next node on the path, g(n) is the cost of the path from the start node to n, 
        and h(n) is a heuristic function that estimates the cost of the cheapest path from n to the
        goal. A* terminates when the path it chooses to extend is a path from start to goal or if
        there are no paths eligible to be extended. The heuristic function is problem-specific. 
        If the heuristic function is admissible, meaning that it never overestimates the actual cost
        to get to the goal, A* is guaranteed to return a least-cost path from start to goal."   
        """
        frontier = [] 
        # The frontier keeps the nodes waiting to be expanded by the search algorithm. I use
        # a heap datastructure to do fast extraction of minima
        heappush(frontier, (self.manhattan_dist() + self._search_depth, self))
        
        max_search_depth = 0

        closed = set()  # to contain grids of nodes that have been expanded already
        num_expanded_nodes = 0
               
        while frontier:
            #Remove node from heap
            _, node = heappop(frontier)   #extracting node where manhattan-distance + search_depth is lowests
            #print(node.recover_path())
      
            #Check if solution is found
            if node.is_solved():
                path_to_goal = node.recover_path()
                return path_to_goal, num_expanded_nodes, max_search_depth

            #Add node's grid to closed set
            closed.add(str(node._grid))

            # Expand the node.
            #   To expand a given node, we generate successor nodes adjacent to the current node, and add them to the
            #   frontier set. Note that if these successor nodes are already in the frontier, or have already been
            #   visited, then they should not be added to the frontier again.
            num_expanded_nodes += 1
            valid_directions = node.valid_directions()
            for direction in valid_directions:
                child = node.clone()
                child.update_puzzle(direction)
                c_grid = str(child._grid)
                child._search_depth += 1

                if c_grid in closed: #already evaluated
                    continue
              
                child._last_move = direction
                child._parent = node
                score = child.manhattan_dist() + child._search_depth
                heappush(frontier, (score, child))
                
            #Check current search depth:
            current_search_depth = node._search_depth + 1

            if current_search_depth > max_search_depth:
                max_search_depth = current_search_depth
                
    def solve_puzzle(self, method, print_results = False):
        """
        Takes a puzzle object and a method ("bfs", "dfs" or "ast" or "gbfs") and returns
        path_to_goal, num_expanded_nodes, max_search_depth, running_time and memory_usage
        
        Optionally prints out search information to the use
        """
        if print_results:
            print("Solving below puzzle using {}-search:\n{}".format(method, self))

        start_time = time.time()

        if method == "bfs":
            path_to_goal, num_expanded_nodes, max_search_depth = self.solve_puzzle_bfs()
        elif method == "dfs":
            path_to_goal, num_expanded_nodes, max_search_depth = self.solve_puzzle_dfs()
        elif method == "ast":
            path_to_goal, num_expanded_nodes, max_search_depth = self.solve_puzzle_ast()
        elif method == "gbfs":
            path_to_goal, num_expanded_nodes, max_search_depth = self.solve_puzzle_gbfs()
        else:
            print("Unknown solution method")

        running_time = time.time() - start_time

        memory_usage =psutil.Process().memory_info().rss/float(1000000)

        if print_results:
            print("")
            print("Search details:")
            #print "Calculated solution string:'{}'".format(path_to_goal))
            print("Length of solution path:", len(path_to_goal))
            print("Total number of expanded nodes", num_expanded_nodes)
            print("Max search depth:", max_search_depth)
            print("Running time of search:", running_time, "seconds")
            print("Max_RAM_usage (in millions):", memory_usage)
            print("")
            print("Control of solution:")
            self.update_puzzle(path_to_goal)
            print("Puzzle after applying solution string:\n",self)
            assert(self.is_solved()), "Puzzle not properly solved!"

        return path_to_goal, num_expanded_nodes, max_search_depth, running_time, memory_usage

if __name__ =="__main__":
    from puzzle_collection import eight_puzzles, fifteen_puzzles
    p = Puzzle(4,4)
    p._grid = fifteen_puzzles[1]
    p.solve_puzzle("bfs", True)