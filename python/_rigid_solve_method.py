##################################################################
# Phase one methods
from Puzzle import Puzzle
def solve_puzzle_rigid():
    def lower_row_invariant(puzzle, target_row, target_col):
        """
        Check whether the puzzle satisfies the specified invariant
        at the given position in the bottom rows of the puzzle (target_row > 1)
        Returns a boolean
        """
        #Tile zero is positioned at (i,j).
        if puzzle._grid[target_row][target_col] != 0:
            return False

        #All tiles in rows i+1 or below are positioned at their solved location.
        for row in range(target_row + 1, puzzle._height):
            for col in range(puzzle._width):
                if puzzle.current_position(row, col) != (row, col):
                    return False

        #All tiles in row i to the right of position (i,j) are positioned at their solved location.
        for col in range(target_col + 1, puzzle._width):
            if puzzle.current_position(target_row, col) != (target_row, col):
                return False

        return True

    def position_tile(puzzle, target_row, target_col, vertical_displacement, horizontal_displacement):
        """
        Helper function. Moves zero vertically up to prior row position of target_tile and rearranges (while keeping
        invariants) such that target_tile ends up beging placed just above this new positionn of the zero.
        input         output                 input      output         input    output           input     output
        .........     ..x......             .x.....    ....0..
        ........x     ..0......             .......    ....x..        .......    .....x           ..x.....   .....0
        .........     .........     or      .......    .......   or   x.....0    .....0     or    .......0   .....x
        .........     .........             .......    .......
        ..0......     .........             .....0.    .......
        """
        move_string = ""

        if vertical_displacement >= 2 or (vertical_displacement == 1 and horizontal_displacement) > 0:
            #in this case there is free space below target tile
            ver_shift = "d"
            opposite_ver_shift = "u"
        else:
            #in this case there is free space above target tile
            ver_shift = "u"
            opposite_ver_shift = "d"

        for dummy in range(vertical_displacement):
            move_string += "u"

        ####Nu staar nullet vertikalt ud for target_tile

        if horizontal_displacement < 0:
            direction_to_target = "r"
            opposite_direction = "l"

        else:
            direction_to_target = "l"
            opposite_direction = "r"

        number_of_loops = abs(horizontal_displacement)

        while number_of_loops > 0:
            #Dette loops kunne godt optimeres. Ingen grund til at gaa helt tilbage hver gang.
            for dummy in range(number_of_loops):
                move_string += direction_to_target
            move_string += ver_shift
            for dummy in range(number_of_loops):
                move_string += opposite_direction
            move_string += opposite_ver_shift
            number_of_loops -= 1

        return move_string

    def solve_interior_tile(puzzle, target_row, target_col):
        """
        Place correct tile at target position
        Updates puzzle and returns a move string
        """
        assert lower_row_invariant(puzzle, target_row, target_col), "Lower row invariant not satisfied before solving"
        target_tile = puzzle.current_position(target_row, target_col)
        vertical_displacement = target_row - target_tile[0]
        horizontal_displacement = target_col - target_tile[1]

        ## CASE 1: Target tile is vertically above target position and target_col != 0
        move_string = ""

        if target_tile[1] == target_col and target_col != 0:

            #position zero just above target_tile.
            for dummy_number in range(vertical_displacement):
                move_string += "u"
                puzzle.update_puzzle("u")

            #move target_tile vertically down to desired position
            for dummy_number in range(vertical_displacement - 1):
                puzzle.update_puzzle("lddru")
                move_string += "lddru"

            # place zero at next target_postition
            puzzle.update_puzzle("ld")
            move_string += "ld"

        # CASE 2: Target tile is not vertically above target position and target_colon !=0
        elif target_col != 0:
            move_string = position_tile(puzzle, target_row, target_col, vertical_displacement, horizontal_displacement)

            ### THIS IS VERY INEFFICIENT as it will result in "ddduuu" sequences.
            ## Solution is to refactor some of above code
            for dummy in range(vertical_displacement):
                move_string += "d"

            puzzle.update_puzzle(move_string)
            move_string += solve_interior_tile(puzzle, target_row, target_col)

        error_message = "Lower row invariant not satisfied after solve interior tile at target position ({},{})".format(target_row, target_col)
        assert lower_row_invariant(puzzle, target_row, target_col-1), error_message
        return move_string

    def solve_col0_tile(puzzle, target_row):
        """
        Solve tile in column zero on specified row (> 1)
        Updates puzzle and returns a move string
        """
        assert lower_row_invariant(puzzle, target_row, 0), "Lower row invariant not satisfied before solving"
        target_col = 0
        target_tile = puzzle.current_position(target_row, target_col)
        vertical_displacement = target_row - target_tile[0]
        horizontal_displacement = target_col - target_tile[1]

        move_string = position_tile(puzzle, target_row, target_col, vertical_displacement, horizontal_displacement)

        ###Some speciale cases
        if vertical_displacement == 1:
            if target_tile[1] == 0:
                move_string += "r"
            else:
                move_string += "urdl"

        ## More general situation
        else:
            current_target_tile_row = target_tile[0] + 1
            number_of_loops = target_row - 1 - current_target_tile_row
            while number_of_loops > 0:
                move_string += "rddlu"
                number_of_loops -= 1
            move_string += "rdl"

        #add long string in all but the most special case
        if not (vertical_displacement == 1 and target_tile[1] == 0):
            move_string += "ruldrdlurdluurddlur"

        #move zero tile to next target position to solve
        for dummy in range(puzzle._width - 2):
            move_string += "r"

        #update puzzle, check invariant and return move string
        puzzle.update_puzzle(move_string)
        error_message = "Lower row invariant not satisfied after solving col0 at pos({},{})".format(target_row, 0)
        assert lower_row_invariant(puzzle, target_row-1, puzzle._width-1), error_message
        return move_string

    #############################################################
    # Phase two methods

    def row0_invariant(puzzle, target_col):
        """
        Check whether the puzzle satisfies the row zero invariant
        at the given column (col > 1)
        Returns a boolean
        """

        if puzzle._grid[0][target_col] != 0:
            return False

        if puzzle.current_position(1, target_col) != (1, target_col):
            return False

        for row in range(puzzle._height):
            for col in range(puzzle._width):
                if (row >= 2 or col > target_col) and puzzle.current_position(row, col) != (row, col):
                    return False
        return True

    def row1_invariant(puzzle, target_col):
        """
        Check whether the puzzle satisfies the row one invariant
        at the given column (col > 1)
        Returns a boolean
        """

        if puzzle._grid[1][target_col] != 0:
            return False

        for row in range(puzzle._height):
            for col in range(puzzle._width):
                if (row >= 2 or col > target_col) and puzzle.current_position(row, col) != (row, col):
                    return False
        return True

    def solve_row1_tile(puzzle, target_col):
        """
        Solve the tile in row one at the specified column
        Updates puzzle and returns a move string
        """
        error_message = "row1 invariant not satisfied prior to solving col{}".format(target_col)
        assert puzzle.row1_invariant(target_col), error_message

        target_row = 1
        target_tile = puzzle.current_position(target_row, target_col)
        vertical_displacement = target_row - target_tile[0]
        horizontal_displacement = target_col - target_tile[1]

        move_string = position_tile(puzzle, target_row, target_col, vertical_displacement, horizontal_displacement)

        if target_tile[0] == 1:
            move_string += "u"

        puzzle.update_puzzle(move_string)
        error_message = "row0 invariant not satisfied after to solving row 1 in col{}".format(target_col)
        assert row0_invariant(puzzle, target_col), error_message
        return move_string


    def solve_row0_tile(puzzle, target_col):
        """
        Solve the tile in row zero at the specified column
        Updates puzzle and returns a move string
        """
        error_message = "row0 invariant not satisfied prior to solving col{}".format(target_col)
        assert row0_invariant(puzzle, target_col), error_message

        move_string = "ld"
        puzzle.update_puzzle(move_string)

        #special case
        if puzzle.current_position(0,target_col) == (0, target_col):
            return move_string

        target_row = 0
        target_tile = puzzle.current_position(target_row, target_col)

        #Nota Bene: This is a bit different than usual
        current_zero_pos = (1, target_col - 1)
        vertical_displacement = current_zero_pos[0] - target_tile[0]
        horizontal_displacement = current_zero_pos[1] - target_tile[1]

        more_moves = position_tile(puzzle, target_row, target_col, vertical_displacement, horizontal_displacement)
        move_string += more_moves

        if target_tile[0] == 1:
            add_moves = "uld"
        else:
            add_moves = "ld"

        move_string += add_moves

        trick_move = "urdlurrdluldrruld"
        move_string += trick_move

        puzzle.update_puzzle(more_moves + add_moves + trick_move)
        error_message = "row1 invariant for col {} not satisfied after to solving row 0 in col{}".format(target_col-1, target_col)
        assert puzzle.row1_invariant(target_col-1), error_message
        return move_string

    ###########################################################
    # Phase 3 methods

    def solve_2x2(puzzle):
        """
        Solve the upper left 2x2 part of the puzzle
        Updates the puzzle and returns a move string
        The assumptions right now is, that zero is at position (1,1) and thas puzzle is solvable
        Future development: I ought to add an assertion that 2x2 puzzle is solvable!
        """
        assert puzzle.row1_invariant(1), "Phase 1 and 2 of solution proces not completed prior to solving 2x2 puzzle"
        one_tile_pos = puzzle.current_position(0,1)

        #To avoid errors if user mistakenly applies method to solved puzzle:
        if row0_invariant(puzzle, 0):
            return ""

        #Postiton of 1_tile determines the 3 solvable constallations, where 0_tile is at pos (1,1)
        if one_tile_pos == (0,0):
            move_string = "ul"
        elif one_tile_pos == (1,0):
            move_string = "uldrul"
        elif one_tile_pos == (0,1):
            move_string = "lu"

        puzzle.update_puzzle(move_string)
        assert row0_invariant(puzzle, 0), "Puzzle not solved correctly"
        return(move_string)


    def legal_directions(puzzle):
        """
        Returns list of legal directions
        """
        zero_row, zero_col = puzzle.current_position(0, 0)

        legal_moves = []
        if zero_row > 0:
            legal_moves.append("u")
        if zero_row < puzzle._height - 1:
            legal_moves.append("d")
        if zero_col > 0:
            legal_moves.append("l")
        if zero_col < puzzle._width - 1:
            legal_moves.append("r")
        return legal_moves


    def satisfies_some_invariant(puzzle):
        zero_row, zero_col = puzzle.current_position(0, 0)

        if zero_row == 0 and row0_invariant(puzzle, zero_col):
            return True
        if zero_row == 1 and puzzle.row1_invariant(zero_col):
            return True
        if zero_row > 1 and lower_row_invariant(puzzle, zero_row, zero_col):
            return True

    def score_invariant_position(puzzle):
        score_matrix = [[16, -1, 11, 9],
                        [-1, 12, 10, 8],
                        [7,  6,  5,  4],
                        [3,  2,  1, 0]]
        zero_row, zero_col = puzzle.current_position(0, 0)
        return score_matrix[zero_row][zero_col]

    def tree_search(puzzle, move_string, recursion_depth):
        """
        Performs tree search
        """

        if recursion_depth == 0:
            if satisfies_some_invariant(puzzle):
                return (score_invariant_position(puzzle), move_string)
            else:
                return (-1, "")

        legal_direcs = legal_directions(puzzle)
        subtrees = []
        best_score = -1
        best_move = ""

        if satisfies_some_invariant(puzzle):
            score = score_invariant_position(puzzle)
            if score == 16:
                return (16, move_string)
            elif score > best_score or (score == best_score and len(move_string)<len(best_move)):
                best_score = score
                best_move = move_string

        for direction in legal_direcs:
            subtree = puzzle.clone()
            subtree.update_puzzle(direction)
            subtrees.append(subtree)
            score, move = tree_search(puzzle, move_string + direction, recursion_depth - 1)
            if score > best_score or (score == best_score and len(move)<len(best_move)):
                best_score = score
                best_move = move

        return (best_score, best_move)

    def solve_puzzle(puzzle, answer_move):
        """
        Generate a solution string for a puzzle
        Updates the puzzle and returns a move string
        #Phase 3 in need of further testing. Think about unsolvable cases...
        Future development: I could rewrite the function so that it could
        return final move_string instead of just printing it. It would take someting like
        return "move_string so far"+solve_puzzle(reduced_puzzle)
        """
        #Set dpeth of recursion:
        recursion_depth = 15

        if answer_move == "":
            print("Solving original puzzle")
            print(puzzle)

        if row0_invariant(puzzle, 0):
            print( "\nPuzzle solved")
            print("\nLenght of final solution string: "+ str(len(answer_move)))
            print("Final solution string:", answer_move)
            quit()
            #return answer_move

        #Don't do tree search in this special case:
        if puzzle._grid[1][1] == 0 and puzzle.row1_invariant(1):
            print("\nAlmost done. Puzzle reduced to 2x2 case\n")
            best_score = -1
            best_move = None

        #Do tree search in this more general situation:
        else:
            best_score, best_move = tree_search(puzzle, "",recursion_depth)
            if best_move == "":
                move_message = "'empty string'"
            else:
                move_message = best_move
            print("Tree search applied to puzzle:\n", puzzle)
            print("Best move from tree search is {} with score {}\n".format(move_message, best_score))

        if best_score > -1 and best_move != "":
            puzzle.update_puzzle(best_move)
            print("Above tree search move applied with resulting puzzle:\n", puzzle)
            answer_move += best_move
            solve_puzzle(puzzle, answer_move)

        row, col = puzzle.current_position(0, 0)

        # Phase 0: If solve proces has not even begun, then move zero to buttom right
        if answer_move == "" and (row, col) != (puzzle._height - 1, puzzle._width - 1):
            print("Moving zero to buttom right corner")
            zero_move = ""
            for dummy in range(puzzle._height - row - 1):
                zero_move += "d"
            for dummy in range(puzzle._width - col - 1):
                zero_move += "r"
            puzzle.update_puzzle(zero_move)
            solve_puzzle(puzzle, zero_move)

        # Phase 1:
        elif row >1 :
            print("\nComputing phase 1 move to below puzzle...\n{}\n".format(puzzle))
            assert lower_row_invariant(puzzle, row, col), "lower row invariant not satisfied prior to solving"
            if col > 0:
                move = solve_interior_tile(puzzle, row, col)
                assert lower_row_invariant(puzzle,row, col-1)
            else:
                move = solve_col0_tile(puzzle, row)
                assert lower_row_invariant(puzzle, row-1, puzzle._width-1)

            print("Phase 1 move {} applied with resulting puzzle\n{}\n".format(move, puzzle))
            answer_move += move
            print("Lenght of solution string, so far:", len(answer_move))
            solve_puzzle(puzzle, answer_move)

        #Phase 2
        elif col > 1:
            print("\nComputing phase 2 move to below puzzle...\n{}\n".format(puzzle))
            if row == 1:
                move = solve_row1_tile(puzzle, col)
                assert row0_invariant(puzzle, col)
            if row == 0:
                move = puzzle.solve_row0_tile(col)
                assert puzzle.row1_invariant(col-1)
            answer_move += move
            print("Phase 2 move {} applied with resulting puzzle\n{}\n".format(move, puzzle))
            print("Lenght of solution string, so far:", len(answer_move))
            solve_puzzle(puzzle, answer_move)

        #Phase 3
        #The assumption here is that phase 1 and 2 are completed properly
        else:
            print("\nComputing phase 3 move to below puzzle...\n{}\n".format(puzzle))
            move = solve_2x2(puzzle)
            assert row0_invariant(puzzle, 0)
            answer_move += move
            print("Phase 3 move {} applied with resulting puzzle\n{}\n".format(move, puzzle))
            solve_puzzle(puzzle, answer_move)
    solve_puzzle(puzzle, "")

def small_tests():
    ##Joe Warrens challenge puzzle. 
    # My rigid tile by tile solution is about 236 moves. Optimal solution is about 80 moves.
    puzzle=Puzzle(4, 4, 
    [
        [15, 11, 8, 12], 
        [14, 10, 9, 13], 
        [2, 6, 1, 4], 
        [3, 7, 5, 0]
    ])
    solve_puzzle_rigid(puzzle, "")
small_tests()