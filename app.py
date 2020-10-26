# Setup instuctions for Flask in Visual Studio Code
# 1) Make folder/directory for flask project
# 2) Go to this folder and open terminal 
# 3) Write command "python -m venv env" (this makes the virtual environment)
# 4) Ctrl + Shift + P --> Python select intrepreter --> select the one with "env"   
# 5) In therminal: "pip install flask"
# 6) In terminal: "python app.py"

from flask import Flask, render_template, request
import timeit
from random import choice as random_choice
from python.Puzzle import Puzzle
from python.utils import string_to_grid, convert_solution_string

app = Flask('__name__')

collection = ["rdrdllurrullddrurdululddruuldduuddrr", "ddrruulddruulldrdurdllurdr", "rdrdluurdlurdlrldrulldruldruuldrldruuddruulddlurdruldluurrdlurdldr", "rdrulddlrurdluurdlurddlurdllurrdluuldrdrulurddllurdr", "drdrulurdlldrurduulddluurrdldluurrddlluurrddlluurrddlluurrdd","rrddllurrd","ddrruullddrruulldrldrr"]

@app.route("/", methods=['GET', 'POST'])
def index():
    human_num_solution_steps = ""
    asked_for_help = False
    human_solution = ""
    show_ai_solution_step = False
    full_ai_solution = ""
    send_new_puzzle = (request.method == 'GET' or (request.method == 'POST' and request.form['requested_action']=='new_puzzle'))
    if send_new_puzzle: 
        puzzle = Puzzle(3,3)
        puzzle_number = random_choice(range(len(collection)))
        puzzle.update_puzzle(collection[puzzle_number])
        puzzle_number +=1
        puzzle_is_solved = puzzle.is_solved()
        ai_puzzle = puzzle
        ai_original_puzzle = puzzle
        human_puzzle = puzzle
        ai_puzzle_is_solved = puzzle_is_solved
        human_puzzle_is_solved = puzzle_is_solved
        ai_cost = 0
        human_cost = 0 
        num_expanded_nodes = ""
        max_search_depth = ""
        max_ram_usage = ""
        running_time = ""
        ai_solution = ""
        search_type = ""
        ai_num_solution_steps = ""
        human_steps_made = ""
    else: 
        ai_puzzle = Puzzle(3,3, string_to_grid(''.join(c for c in  request.form['ai_puzzle'] if c not in '[]')))
        human_puzzle = Puzzle(3,3, string_to_grid(''.join(c for c in request.form['human_puzzle'] if c not in '[]')))
        ai_original_puzzle = Puzzle(3,3, string_to_grid(''.join(c for c in request.form['ai_original_puzzle'] if c not in '[]')))
        ai_cost = int(request.form['ai_cost'])
        human_cost = int(request.form['human_cost'])
        num_expanded_nodes = request.form['num_expanded_nodes']
        max_search_depth = request.form['max_search_depth']
        max_ram_usage = request.form['max_ram_usage']
        running_time = request.form['running_time']
        ai_solution = request.form['ai_solution']
        search_type = request.form['search_type']
        ai_num_solution_steps = request.form['ai_num_solution_steps']
        human_steps_made = request.form['human_steps_made']
        puzzle_number = request.form['puzzle_number']
        full_ai_solution = request.form['full_ai_solution']
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
            ai_solution, ai_num_solution_steps, num_expanded_nodes, max_search_depth, running_time, max_ram_usage \
                = ai_puzzle.solve_puzzle(search_type)
            running_time = round(running_time, 6)
            max_ram_usage = round(max_ram_usage, 4)  #number is in megabytes
            ai_puzzle_is_solved = True
            full_ai_solution = ai_solution
            if ai_num_solution_steps > 100:
                show_ai_solution_step = False
                ai_puzzle.update_puzzle(ai_solution)
                ai_puzzle_is_solved = True
                ai_cost = ai_num_solution_steps
            else:
                show_ai_solution_step = True
        
        elif request.form['requested_action'] == "show_ai_solution_step":
            if len(ai_solution) > 0:
                direction = ai_solution[0]
                ai_puzzle.update_puzzle(direction)
                ai_cost = ai_cost + 1
            if len(ai_solution) > 1:
                show_ai_solution_step = True
            else: 
                show_ai_solution_step = False
            ai_solution = ai_solution[1:]
            ai_puzzle_is_solved = True
        
        elif request.form['requested_action'] == "unsolve":
            ai_puzzle = ai_original_puzzle
            ai_puzzle_is_solved = False
            ai_cost = 0
        
        elif request.form['requested_action'] == "help":
            human_solution_str, human_num_solution_steps, _, _, _, _ = human_puzzle.solve_puzzle("ast")
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
        human_puzzle = human_puzzle._grid,
        ai_puzzle = ai_puzzle._grid,
        ai_puzzle_is_solved = ai_puzzle_is_solved,
        human_puzzle_is_solved = human_puzzle_is_solved,
        ai_cost = ai_cost,
        human_cost = human_cost,
        num_expanded_nodes = num_expanded_nodes,
        max_search_depth = max_search_depth,
        max_ram_usage = max_ram_usage,
        running_time = running_time,
        ai_solution = ai_solution,
        show_ai_solution_step = show_ai_solution_step,
        search_type = search_type,
        ai_num_solution_steps = ai_num_solution_steps,
        human_steps_made = human_steps_made,
        puzzle_number = puzzle_number,
        human_solution = human_solution,
        human_num_solution_steps = human_num_solution_steps,
        asked_for_help = asked_for_help,
        ai_original_puzzle = ai_original_puzzle._grid,
        full_ai_solution = full_ai_solution
        ) 

@app.route('/<full_ai_solution>')
def show_solution_string(full_ai_solution):
    return str(convert_solution_string(full_ai_solution))

if __name__ == "__main__":
    app.run(debug=True)