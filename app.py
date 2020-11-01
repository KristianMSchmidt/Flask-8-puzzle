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
from python.Puzzle import Puzzle
from python.utils import convert_solution_string
from python.puzzle_collection import puzzle_collection

app = Flask('__name__')

@app.route("/", methods=['GET', 'POST'])
def index():
    
    if request.method == 'GET':
        action = "new_puzzle"
        search_type = "ast_alt"
    else: 
        data = json.loads(request.form["json_data"])   #return(json.dumps(data))
        action = data["requested_action"]
        search_type = data["search_type"]

    if action == 'new_puzzle':
        puzzle_number = random_choice(range(len(puzzle_collection)))
        puzzle = Puzzle(3,3,puzzle_collection[puzzle_number])._grid 
        data = {
            "puzzle_number":puzzle_number + 1,
            "ai_puzzle": puzzle,
            "human_puzzle": puzzle,
            "human_move_count": 0,
            "human_puzzle_is_solved": False,
            "search_type" : search_type,
            "requested_action" : "new_puzzle",
            "ai_solution_computed": False,
            "15_puzzle": [[1, 2, 6, 3],
                          [4, 5, 0, 7],
                          [8, 9, 10, 11],
                          [12, 13, 14, 15]],
            "search_names": {
                "ast_alt": "A*-search",
                "dfs": "Depth-first Search",
                "bfs": "Breath-first Search",
                "gbfs": "Gready best-First Search "
            }
        }

    elif action == 'human_move':
        human_puzzle = Puzzle(3,3, data["human_puzzle"])
        try:
            human_puzzle.update_puzzle(data["direction"])
            data["human_puzzle"] = human_puzzle._grid
            data["human_move_count"] += 1
            data["human_puzzle_is_solved"] = human_puzzle.is_solved()
        except:
            pass

    elif action == 'solve_ai_puzzle':
        ai_puzzle = Puzzle(3,3, data["ai_puzzle"])
        ai_solution_string, ai_num_solution_steps, num_expanded_nodes, max_search_depth, running_time, max_ram_usage \
                = ai_puzzle.solve_puzzle(data['search_type'])
        data['running_time'] = round(running_time, 5)
        data['max_ram_usage'] = round(max_ram_usage, 2)  #number is in megabytes
        data['ai_num_solution_steps'] = len(ai_solution_string)
        data['num_expanded_nodes'] = num_expanded_nodes
        data['max_search_depth'] = max_search_depth
        data['ai_solution_string'] = ai_solution_string
        data["ai_solution_computed"] = True
        
        # Compute all board positions on the road to solution:
        ai_puzzle_clone = ai_puzzle.clone()
        animated_solution = []
        for direction in ai_solution_string:
            ai_puzzle_clone.update_puzzle(direction)
            animated_solution.append(ai_puzzle_clone.clone()._grid)    
        data['animated_solution'] = animated_solution 
        data["final_state"] = animated_solution[-1]

        
    elif action == 'reset_ai': 
        data["ai_solution_computed"] = False
    
    elif action == "help":
        human_puzzle = Puzzle(3,3, data["human_puzzle"])
        human_solution, human_num_solution_steps, _, _, _, _ = human_puzzle.solve_puzzle(data["search_type"])
        human_solution = convert_solution_string(human_solution)
        human_num_solution_steps = len(human_solution)
        if human_num_solution_steps > 0:
            hint = human_solution[0]
            if human_num_solution_steps > 1:
                hint += ", " + human_solution[1]       
                if human_num_solution_steps > 2:
                    hint += ", " + human_solution[2] 
            hint += "..."    
        else:
            hint = ""
        data["human_hint"] = hint
        data['human_num_solution_steps'] = human_num_solution_steps

    elif action == "solve_ai_15_puzzle":
        ai_puzzle = Puzzle(4,4, data["15_puzzle"])
        ai_solution_string, ai_num_solution_steps, num_expanded_nodes, max_search_depth, running_time, max_ram_usage \
                = ai_puzzle.solve_puzzle(data['search_type'])
        data['running_time_15'] = round(running_time, 5)
        data['max_ram_usage_15'] = round(max_ram_usage, 2)  #number is in megabytes
        data['ai_num_solution_steps_15'] = len(ai_solution_string)
        data['num_expanded_nodes_15'] = num_expanded_nodes
        data['max_search_depth_15'] = max_search_depth
        data['ai_15_solution_string'] = ai_solution_string
        data["ai_15_solution_computed"] = True
        
        # Compute all board positions on the road to solution:
        ai_puzzle_clone = ai_puzzle.clone()
        animated_solution = []
        for direction in ai_solution_string:
            ai_puzzle_clone.update_puzzle(direction)
            animated_solution.append(ai_puzzle_clone.clone()._grid)    
        data['animated_solution_15'] = animated_solution 
        data["final_state_15"] = animated_solution[-1]

    return render_template("index.html", data = data)

@app.route('/<ai_solution_string>')
def show_solution_string(ai_solution_string):
    return str(convert_solution_string(ai_solution_string))

if __name__ == "__main__":
    app.run(debug=True)