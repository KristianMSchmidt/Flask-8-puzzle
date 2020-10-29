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
from python.utils import string_to_grid, convert_solution_string
from python.puzzle_collection import puzzle_collection
app = Flask('__name__')

@app.route("/", methods=['GET', 'POST'])
def index():
    human_num_solution_steps = ""
    asked_for_help = False
    human_solution = ""
    solution_grids = []
    show_ai_solution = False
    send_new_puzzle = (request.method == 'GET' or (request.method == 'POST' and request.form['requested_action']=='new_puzzle'))
    if send_new_puzzle:
        # First visit or user has requsted a new puzzle 
        puzzle_number = random_choice(range(len(puzzle_collection)))
        ai_puzzle = Puzzle(3,3,puzzle_collection[puzzle_number]) 
        puzzle_number +=1
        ai_puzzle_is_solved = ai_puzzle.is_solved()
        ai_original_puzzle = ai_puzzle.clone()
        human_puzzle = ai_puzzle.clone()
        human_puzzle_is_solved = human_puzzle.is_solved
        human_cost = 0 
        num_expanded_nodes = ""
        max_search_depth = ""
        max_ram_usage = ""
        running_time = ""
        ai_solution_string = ""
        search_type = ""
        ai_num_solution_steps = 0
        human_steps_made = ""
    else: 
        # User has made some reqeust other than new puzzle
        ai_puzzle = Puzzle(3,3, string_to_grid(request.form['ai_puzzle']))
        human_puzzle = Puzzle(3,3, string_to_grid(request.form['human_puzzle']))
        ai_original_puzzle = Puzzle(3,3, string_to_grid(request.form['ai_original_puzzle']))
        human_cost = int(request.form['human_cost'])
        num_expanded_nodes = request.form['num_expanded_nodes']
        max_search_depth = request.form['max_search_depth']
        max_ram_usage = request.form['max_ram_usage']
        running_time = request.form['running_time']
        ai_solution_string = request.form['ai_solution_string']
        search_type = request.form['search_type']
        ai_num_solution_steps = request.form['ai_num_solution_steps']
        human_steps_made = request.form['human_steps_made']
        puzzle_number = request.form['puzzle_number']
        ai_puzzle_is_solved = ai_puzzle.is_solved()
        human_puzzle_is_solved = human_puzzle.is_solved()
        if request.form['requested_action'] == "human_move":
            direction = request.form['direction']
            try:         
                human_puzzle.update_puzzle(direction)
                human_cost = human_cost + 1
                human_puzzle_is_solved = human_puzzle.is_solved()
            except:
                # move off grid
                pass

        elif request.form['requested_action'] == "solve_puzzle":
            search_type = request.form['search_type']
            ai_solution_string, ai_num_solution_steps, num_expanded_nodes, max_search_depth, running_time, max_ram_usage \
                = ai_puzzle.solve_puzzle(search_type)
            running_time = round(running_time, 5)
            max_ram_usage = round(max_ram_usage, 2)  #number is in megabytes
            solution_grids = []
            ai_puzzle_is_solved = True
            for direction in ai_solution_string:
                ai_puzzle.update_puzzle(direction)
                solution_grids.append(ai_puzzle.clone().get_grid())    
       
        elif request.form['requested_action'] == "unsolve":
            ai_puzzle = ai_original_puzzle.clone()
            ai_puzzle_is_solved = False
        
        elif request.form['requested_action'] == "help":
            human_solution_str, human_num_solution_steps, _, _, _, _ = human_puzzle.solve_puzzle("ast_alt")
            human_solution_list = convert_solution_string(human_solution_str)
            if len(human_solution_list) > 0:
                human_solution = human_solution_list[0]
            if len(human_solution_list)> 1:
                human_solution = human_solution + ", " + human_solution_list[1]       
            if len(human_solution_list)> 2:
                human_solution = human_solution + ", " + human_solution_list[2] 
            human_solution += "..."    
            asked_for_help = True 

    return render_template( 
        "index.html",
        human_puzzle = human_puzzle.get_grid(),
        ai_puzzle = ai_puzzle.get_grid(),
        ai_puzzle_is_solved = ai_puzzle_is_solved,
        human_puzzle_is_solved = human_puzzle_is_solved,
        human_cost = human_cost,
        num_expanded_nodes = num_expanded_nodes,
        max_search_depth = max_search_depth,
        max_ram_usage = max_ram_usage,
        running_time = running_time,
        ai_solution_string = ai_solution_string,
        show_ai_solution = show_ai_solution,
        search_type = search_type,
        ai_num_solution_steps = ai_num_solution_steps,
        human_steps_made = human_steps_made,
        puzzle_number = puzzle_number,
        human_solution = human_solution,
        human_num_solution_steps = human_num_solution_steps,
        asked_for_help = asked_for_help,
        ai_original_puzzle = ai_original_puzzle.get_grid(),
        solution_grids = solution_grids,
        json_data = {"name":"John", "age":30, "list":[1,2,3], "city":"New York"}

        ) 

@app.route('/<ai_solution_string>')
def show_solution_string(ai_solution_string):
    return str(convert_solution_string(ai_solution_string))

if __name__ == "__main__":
    app.run(debug=True)