import time, queue, psutil
from heapq import heappush, heappop

class Puzzle:
    """
    Initialize puzzle. Returns a Puzzle object
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
        This is needed for "heappush" in solve-algorithms to be stable. 
        """
        return self

    def clone(self):
        """
        Make a copy of the puzzle to update during solving
        Returns a Puzzle object
        """
        new_puzzle = Puzzle(self._height, self._width, self._grid, self._last_move, self._search_depth, self._parent)
        return new_puzzle

    ########################################################
    # Core puzzle methods

    def current_position(self, solved_row, solved_col):
        """
        Locate the current position of the tile that will be at
        position (solved_row, solved_col) when the puzzle is solved
        Returns a tuple of two integers
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
        Recovers path takes from startnode to the node in question.
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

    def solve_puzzle_dfs(self):
        """
        Solves the puzzle using Depth-First Search.
        """
        #initialize stack (I use lists)
        stack = [self]  #the stack is "the frontier"

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
            node = stack.pop()

            #Check if solution is found
            if node.is_solved():
                path_to_goal = node.recover_path()
                return path_to_goal, len(path_to_goal), num_expanded_nodes, max_search_depth

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
                    continue

                child._last_move = direction
                child._parent = node
                stack.append(child)
                in_frontier_or_explored.add(child_game_state)


            if current_search_depth > max_search_depth:
                max_search_depth = current_search_depth
                #print "current max search depth", max_search_depth

    def solve_puzzle_bfs(self):
        """
        Solves the puzzle using Breadth-First search.
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

            #Check if solution is found
            if node.is_solved():
                path_to_goal = node.recover_path()
                return path_to_goal, len(path_to_goal), num_expanded_nodes, max_search_depth

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

                child._last_move = direction
                child._parent = node
                frontier.put(child)
                in_frontier_or_explored.add(child_game_state)

            #Check current search depth:
            current_search_depth = node._search_depth + 1

            if current_search_depth > max_search_depth:
                max_search_depth = current_search_depth

    def manhattan_dist(self):
        """
        Computes the total manhattan-distance between the given puzzle and the solved game state.
        """
        answer = 0

        #Calculate first row separately, as zero_tile should not be part of sum:
        for col in range(1, self._width):
            current_row, current_col = self.current_position(0,col)
            answer += abs(col-current_col) + current_row

        #Now the rest of the rows
        for row in range(1, self._height):
            for col in range(self._width):
                current_row, current_col = self.current_position(row,col)
                answer += abs(col-current_col) + abs(row - current_row)

        return answer


    def solve_puzzle_ast_naive(self):
        """
        Solves the puzzle using A*search with Manhattan-distance heuristics.
        Naive brute force version for test purposes
        """
        frontier = [(self.manhattan_dist() + self._search_depth, 0, self)]

        closed = set()

        frontier_memory = set([str(self._grid)])

        max_search_depth = 0

        while frontier:
            #Remove node from frontier
            x,y,node = min(frontier)
            frontier.remove((x,y,node))

            #Check if solution is found
            if node.is_solved():
                path_to_goal = node.recover_path()
                num_expanded_nodes = len(closed) + 1
                return path_to_goal, len(path_to_goal), num_expanded_nodes, max_search_depth

            #Add node to closed set and remove it from frontier_dict
            node_grid = str(node._grid)
            closed.add(node_grid)

            # Expand the node.
            #   To expand a given node, we generate successor nodes adjacent to the current node, and add them to the
            #   frontier set. Note that if these successor nodes are already in the frontier, or have already been
            #   visited, then they should not be added to the frontier again.
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

                if direction == "u": dir_priority = 0
                if direction == "d": dir_priority = 1
                if direction == "l": dir_priority = 2
                if direction == "r": dir_priority = 3

                #If the child is not in the closed list, if chosen to add it to the frontier
                #nomatter it is an interely new game state or if a similar game_state is already in the fronter
                # This is not wrong (I think), but it makes the heap a bit longer.
                # The suggested solution is to update the heap (using key_down-techniques),
                # if the game state is already there, but with a
                # higher search_depth
                child_info = (child.manhattan_dist() + child._search_depth, dir_priority, child)

                if not c_grid in frontier_memory:
                    frontier.append(child_info)
                    frontier_memory.add(c_grid)

                else:
                    for x,y,z in frontier:
                        if str(z._grid) == c_grid and (x,y,z) > child_info:
                            frontier.remove((x,y,z))
                            frontier.append(child_info)

                #Check current search depth:
                current_search_depth = node._search_depth + 1

            if current_search_depth > max_search_depth:
                max_search_depth = current_search_depth


    def solve_puzzle_ast(self):
        """
        Solves the puzzle using A*-search with Manhattan distance heuristic.
        I add each child to the heap/frontier if it is not in the closed list (nb: this makes the heap longer)
        In case of ties (same Manhattan Distance), this version keeps the ULDR-order.
        
        NB: Below implementations are probably better (both faster and more correct.
        """
        frontier = [] # The "frontier". I use heap to do fast extract minimums

        heappush(frontier, (self.manhattan_dist() + self._search_depth, 0, self))

        max_search_depth = 0

        closed = set()

        while frontier:
            #Remove node from heap
            _,_, node = heappop(frontier)

            #Check if solution is found
            if node.is_solved():
                path_to_goal = node.recover_path()
                num_expanded_nodes = len(closed) + 1
                return path_to_goal, len(path_to_goal), num_expanded_nodes, max_search_depth

            #Add node to closed set and remove it from frontier_dict
            node_grid = str(node._grid)
            closed.add(node_grid)

            # Expand the node.
            #   To expand a given node, we generate successor nodes adjacent to the current node, and add them to the
            #   frontier set. Note that if these successor nodes are already in the frontier, or have already been
            #   visited, then they should not be added to the frontier again.
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
        
                #to maintain UDLR-order in case of ties, we add 0 for u, 1 for d, 2 for l, 3 for r 
                if direction == "u": dir_priority = 0
                if direction == "d": dir_priority = 1
                if direction == "l": dir_priority = 2
                if direction == "r": dir_priority = 3

                #If the child is not in the closed list, if chosen to add it to the frontier
                #nomatter it is an interely new game state or if a similar game_state is already in the fronter
                # This is not wrong (I think), but it makes the heap a bit longer.
                # The suggested solution is to update the heap (using key_down-techniques),
                # if the game state is already there, but with a
                # higher search_depth
                heappush(frontier, (child.manhattan_dist() + child._search_depth, dir_priority, child))

            #Check current search depth:
            current_search_depth = node._search_depth + 1

            if current_search_depth > max_search_depth:
                max_search_depth = current_search_depth

    def solve_puzzle_ast_alternative(self):
        """
        Solves the puzzle using A*search with Manhattan-distance heuristics.  
        In case of ties, this version keeps the ULDR-order.
        This version is different (and probably  better) than the above. In this version,
        I mark the "oudated" game-states in the frontier and ignore them, when they are picked. 
        In other word, I use the approach suggested in this thread:
        "Though the heapq module does not support changing the priority of a particular element of the heap
        (a necessary operation for the A* search family of algorithms), such an element can be marked as invalid and
         a new element can be added with different priority. Any element marked as invalid that makes it to the top
         of the heap can simply be popped off and ignored.
        Users who haven't seen this trick before might mistakenly think the heapq module does not provide
        sufficient operations to implement A* search.
        Please see the recent thread on comp.lang.python for more background:
        http://groups.google.com/group/comp.lang.python/browse_frm/thread/8adc3ce8d2219647"
        """
        frontier = [] # The "frontier". I use heap to do fast extract minimums

        heappush(frontier, (self.manhattan_dist() + self._search_depth, 0, self))

        max_search_depth = 0

        closed = set()

        #I make this hash to deal with the case, when a node with same game state is already in frontier.
        #    minimal_search_depth_with_this_grid = 0
        frontier_hash = {str(self._grid): [0, self]}

        while frontier:
            #Remove node from heap
            _,_, node = heappop(frontier)
            state = str(node._grid)
            while frontier_hash[state][0] != node._search_depth:
                _,_,node = heappop(frontier)
                state = str(node._grid)

            #Check if solution is found
            if node.is_solved():
                path_to_goal = node.recover_path()
                num_expanded_nodes = len(closed) + 1
                return path_to_goal, len(path_to_goal), num_expanded_nodes, max_search_depth

            #Add node to closed set and remove it from frontier_dict
            node_grid = str(node._grid)
            closed.add(node_grid)

            # Expand the node.
            #   To expand a given node, we generate successor nodes adjacent to the current node, and add them to the
            #   frontier set. Note that if these successor nodes are already in the frontier, or have already been
            #   visited, then they should not be added to the frontier again.
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

                #to maintain UDLR-order in case of ties, we add 0 for u, 1 for d, 2 for l, 3 for r 
                if direction == "u": dir_priority = 0
                if direction == "d": dir_priority = 1
                if direction == "l": dir_priority = 2
                if direction == "r": dir_priority = 3

                if c_grid not in frontier_hash: #New node to explore
                    heappush(frontier, (child.manhattan_dist() + child._search_depth, dir_priority, child))
                    frontier_hash[c_grid] = [child._search_depth, child]

                else: #child's gamestate is in frontier. #If child is the best option so far, we mark this
                      #before we add the child to the heap
                    min_search_depth = frontier_hash[c_grid][0]
                    if child._search_depth < min_search_depth:
                        #print child._search_depth, frontier_hash[c_grid]
                        frontier_hash[c_grid][0] = child._search_depth
                        heappush(frontier, (child.manhattan_dist() + child._search_depth, dir_priority, child))
                        frontier_hash[c_grid].append(child)

                #Update current search_depth
                current_search_depth = node._search_depth + 1

            if current_search_depth > max_search_depth:
                max_search_depth = current_search_depth

    def solve_puzzle_gbfs(self):
        """
        Solves the puzzle using greedy_best_first_search with Manhattan-heuristics.
        This is to find a short solution (not necessarily the shortest) in the minimal time.
        I add each child to the heap/frontier if it is not in the closed
        list (nb: this makes the heap longer)
        """
        frontier = [] # The "frontier". I use heap to do fast extract minimums
        heappush(frontier, (self.manhattan_dist(), self))
        max_search_depth = 0

        closed = set()

        while frontier:
            #Remove node from heap
            _, node = heappop(frontier)

            #Check if solution is found
            if node.is_solved():
                path_to_goal = node.recover_path()
                num_expanded_nodes = len(closed) + 1
                return path_to_goal, len(path_to_goal), num_expanded_nodes, max_search_depth

            #Add node to closed set and remove it from frontier_dict
            node_grid = str(node._grid)
            closed.add(node_grid)

            # Expand the node.
            #   To expand a given node, we generate successor nodes adjacent to the current node, and add them to the
            #   frontier set. Note that if these successor nodes are already in the frontier, or have already been
            #   visited, then they should not be added to the frontier again.
            valid_directions = node.valid_directions()
            for direction in valid_directions:
                child = node.clone()
                child.update_puzzle(direction)
                c_grid = str(child._grid)

                if c_grid in closed: #already evaluated
                    continue

                child._last_move = direction
                child._search_depth += 1
                child._parent = node

                #If the child is not in the closed list, if chosen to add it to the frontier
                #nomatter it is an interely new game state or if a similar game_state is already in the fronter
                # This is not wrong (I think), but it makes the heap a bit longer.
                # The suggested solution is to update the heap (using key_down-techniques),
                # if the game state is already there, but with a
                # higher search_depth
                heappush(frontier, (child.manhattan_dist(), child))

            #Check current search depth:
            current_search_depth = node._search_depth + 1

            if current_search_depth > max_search_depth:
                max_search_depth = current_search_depth

    def solve_puzzle_rigid(self):
        """
        This solution method is very different from the ones above. The solution is not found by
        search, but by a rigid solution algorithm that always works. 
        This method is fast (short calculation time), but the number of moves in the 
        solution will probably be longer than the number of moves found by the best search algorithms. 
        """
        

    def solve_puzzle(self, method, print_results = False):
        """
        Takes a puzzle object and a method ("bfs", "dfs" or "ast_alt" or "gbfs") and returns
        the triple: solution_string, num_expanded_nodes, max_search_depth
        """
        if print_results:
            print("Solving below puzzle using {}-search:\n{}".format(method, self))

        start_time = time.time()

        if method == "bfs":
            #depth is number of moves in path_to_goal
            path_to_goal, depth, num_expanded_nodes, max_search_depth = self.solve_puzzle_bfs()
        elif method == "dfs":
            path_to_goal, depth, num_expanded_nodes, max_search_depth = self.solve_puzzle_dfs()
        elif method == "ast_naive":
            path_to_goal, depth, num_expanded_nodes, max_search_depth = self.solve_puzzle_ast_naive()
        elif method == "ast":
            path_to_goal, depth, num_expanded_nodes, max_search_depth = self.solve_puzzle_ast()
        elif method == "ast_alt":
            path_to_goal, depth, num_expanded_nodes, max_search_depth = self.solve_puzzle_ast_alternative()
        elif method == "gbfs":
            path_to_goal, depth, num_expanded_nodes, max_search_depth = self.solve_puzzle_gbfs()
        else:
            print("Unknown solution method")

        running_time = time.time() - start_time

        memory_usage =psutil.Process().memory_info().rss/float(1000000)

        if print_results:
            print("")
            print("Search details:")
            #print "Calculated solution string:'{}'".format(solution_string))
            print("Cost of path:", len(solution_string))
            print("Total number of expanded nodes", num_expanded_nodes)
            print("Search depth:", len(solution_string))
            print("Max search depth:", max_search_depth)
            print("Running time of search:", running_time, "seconds")
            print("Max_RAM_usage (in millions):", memory_usage)
            #print "Expanded solution string:", convert_solution_string(solution_string)
            print("")
            print("Control of solution:")
            self.update_puzzle(solution_string)
            print("Puzzle after applying solution string:\n",self)

        return path_to_goal, depth, num_expanded_nodes, max_search_depth, running_time, memory_usage

