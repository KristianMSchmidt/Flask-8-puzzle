# Setup instuctions for Flask in Visual Studio Code
# 1) Make folder/directory for flask project
# 2) Go to this folder and open terminal 
# 3) Write command "python -m venv env" (this makes the virtual environment)
# 4) Ctrl + Shift + P --> Python select intrepreter --> select the one with "env"   
# 5) In therminal: "pip install flask"
# 6) In terminal: "python app.py"

from flask import Flask, render_template, request
import timeit, json
from random import choice as random_choice
from backend.Puzzle import Puzzle
from backend.utils import convert_solution_string
from backend.puzzle_collection import eight_puzzles, fifteen_puzzles

app = Flask('__name__')

@app.route("/", methods=['GET', 'POST'])
def index():

    if request.method == 'GET':
        action = "new_sample"
        puzzle_dim = 3  
        search_type = "gbfs"
        puzzle_type = "sample"
   
    else: 
        data = json.loads(request.form["json_data"])   #return(json.dumps(data))
        action = data["requested_action"]
        puzzle_dim = data["puzzle_dim"]
        search_type = data["search_type"]
        puzzle_type = data["puzzle_type"]

    if action == 'new_sample' or action == 'show_solved_puzzle': # new sample btn or change puzzle size
        if action == 'new_sample':
            if puzzle_dim == 3:
                puzzle_collection = eight_puzzles
            else:
                puzzle_collection = fifteen_puzzles 
            puzzle_number = random_choice(range(len(puzzle_collection)))
            puzzle = Puzzle(puzzle_dim, puzzle_dim, puzzle_collection[puzzle_number])._grid 
            puzzle_title = "Sample #" + str(puzzle_number+1)
            puzzle_is_solved = False
        else: 
            if puzzle_dim == 3:
                puzzle = [[0,1,2],[3,4,5],[6,7,8]]
            else:
                puzzle = [[0, 1, 2, 3], [4, 5, 6, 7], [8, 9, 10, 11], [12, 13, 14, 15]]
            puzzle_title = "Custom puzzle"
            puzzle_is_solved =  True
    
        if puzzle_dim == 3:
            all_search_types = ["ast", "gbfs", "bfs", "dfs"]
 
        elif puzzle_dim == 4:
            all_search_types = ["ast", "gbfs"]        

        data = {
            "puzzle_title": puzzle_title,
            "puzzle": puzzle,
            "original_puzzle": puzzle,
            "puzzle_dim": puzzle_dim,
            "search_type" : search_type,
            "puzzle_is_solved": puzzle_is_solved,
            "solution_computed": False,
            "requested_action": action,
            "puzzle_type": puzzle_type,
            "move_count": 0,
            "solve_or_reset_btn_value": "Solve",
            "show_solution_details": False,
            "all_search_types": all_search_types,
            "search_names":
                {"ast": "A*-Search",
                "gbfs": "Greedy Best-First Search ",
                "dfs": "Depth-First Search",
                "bfs": "Breadth-First Search"}
        }
        
    elif action == 'human_move':
        puzzle = Puzzle(puzzle_dim, puzzle_dim, data["puzzle"]);    
        try:
            puzzle.update_puzzle(data["direction"])
            data["puzzle"] = puzzle._grid
            data["move_count"] += 1
            data["puzzle_is_solved"] = puzzle.is_solved()
            if data["puzzle_type"] == "sample":
                data["solve_or_reset_btn_value"] = "Reset Sample"
            else:
                data["solve_or_reset_btn_value"] = "Solve"
            data["show_solution_details"] = False
            if data["puzzle_type"] == "custom":
                data["original_puzzle"] = data["puzzle"]
        except:
            pass   # Move is off grid

    elif action == 'solve_puzzle':
        puzzle = Puzzle(puzzle_dim, puzzle_dim, data["puzzle"]);    
        solution_string, num_expanded_nodes, max_search_depth, running_time, max_ram_usage \
                = puzzle.solve_puzzle(data['search_type'])
        data['running_time'] = round(running_time, 5)
        data['max_ram_usage'] = round(max_ram_usage, 2)  #number is in megabytes
        data['num_solution_steps'] = len(solution_string)
        data['num_expanded_nodes'] = num_expanded_nodes
        data['max_search_depth'] = max_search_depth
        data['solution_string'] = solution_string
        data["solution_computed"] = True
        data["show_solution_details"] =  True
        if data["puzzle_type"] == "sample":
            data["solve_or_reset_btn_value"] = "Reset Sample"
        else: 
            data["solve_or_reset_btn_value"] = "Reset Custom"

        
        # Compute all board positions on the road to solution:
        puzzle_clone = puzzle.clone()
        animated_solution = []
        for direction in solution_string:
            puzzle_clone.update_puzzle(direction)
            animated_solution.append(puzzle_clone.clone()._grid)    
        data['animated_solution'] = animated_solution 
        data["final_state"] = animated_solution[-1]

        
    elif action == 'reset': 
        data["solution_computed"] = False
        data["solve_or_reset_btn_value"] = "Solve"
        data["show_solution_details"] = False
        data["puzzle"] = data["original_puzzle"]
        if data["puzzle_type"] == "sample":
            data["move_count"] = 0         

    return render_template("index.html", data = data)

@app.route('/<solution_string>')
def show_solution_string(solution_string):
    return str(convert_solution_string(solution_string))

@app.route("/about")
def about():
    return render_template("about.html")
    
if __name__ == "__main__":
    app.run(debug=True)