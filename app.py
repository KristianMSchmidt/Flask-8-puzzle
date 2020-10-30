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
    else: 
        data = json.loads(request.form["json_data"])   #return(json.dumps(data))
        action = data["requested_action"]

    if action == 'new_puzzle':
        puzzle_number = random_choice(range(len(puzzle_collection)))
        puzzle = Puzzle(3,3,puzzle_collection[puzzle_number])._grid 
        puzzle_number += 1
        search_type = "ast_alt"
        data = {
            "puzzle_number":puzzle_number,
            "ai_puzzle": puzzle,
            "human_puzzle": puzzle,
            "human_move_count": 0,
            "human_puzzle_is_solved": False,
            "ai_status_mgs": "Not solved yet",
            "search_type" : search_type
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
        ai_puzzle_clone = ai_puzzle.clone()
        animated_solution = []
        for direction in data['ai_solution_string']:
            ai_puzzle_clone.update_puzzle(direction)
            animated_solution.append(ai_puzzle_clone.clone()._grid)    
        data['animated_solution'] = animated_solution 
        data['ai_status_mgs'] = "Showing solution..."

    elif action == 'reset_ai': 
        data['ai_status_mgs'] = "Not solved yet"
        data["ai_solution_computed"] = False
    
    elif action == "help":
        human_puzzle = Puzzle(3,3, data["human_puzzle"])
        human_solution, human_num_solution_steps, _, _, _, _ = human_puzzle.solve_puzzle("ast_alt")
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

    return render_template("index.html", data = data)

@app.route('/<ai_solution_string>')
def show_solution_string(ai_solution_string):
    return str(convert_solution_string(ai_solution_string))

if __name__ == "__main__":
    app.run(debug=True)