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
from python.utils import string_to_grid

app = Flask('__name__')

@app.route("/", methods=['GET', 'POST'])

def index():
    send_new_puzzle = (request.method == 'GET' or (request.method == 'POST' and request.form['requested_action']=='new_puzzle'))
    if send_new_puzzle: 
        collection = ["rrddlur", "ddruurdd","rdluddrr"]
        puzzle = Puzzle(3,3)
        puzzle.update_puzzle(random_choice(collection))
        puzzle_is_solved = puzzle.is_solved()
        ai_puzzle = puzzle
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
        render_mgs = "generated new random puzzle"
        show_ai_solution_step = False

    else: 
        ai_puzzle = Puzzle(3,3, string_to_grid(''.join(c for c in  request.form['ai_puzzle'] if c not in '[]')))
        human_puzzle = Puzzle(3,3, string_to_grid(''.join(c for c in request.form['human_puzzle'] if c not in '[]')))
        ai_cost = request.form['ai_cost']
        human_cost = request.form['human_cost']
        num_expanded_nodes = request.form['num_expanded_nodes']
        max_search_depth = request.form['max_search_depth']
        max_ram_usage = request.form['max_ram_usage']
        running_time = request.form['running_time']
        ai_solution = request.form['ai_solution']
        ai_puzzle_is_solved = ai_puzzle.is_solved()
        human_puzzle_is_solved = human_puzzle.is_solved()
        show_ai_solution_step = False

        if request.form['requested_action'] == "human_move" and not human_puzzle_is_solved:
            direction = request.form['direction']
            render_mgs = "made human move"
            try:         
                human_puzzle.update_puzzle(direction)
                human_cost = int(human_cost) + 1
            except:
                # move off grid
                pass

        elif request.form['requested_action'] == "solve_puzzle":
            ai_solution, ai_cost, num_expanded_nodes, max_search_depth, running_time, max_ram_usage \
                = ai_puzzle.solve_puzzle("bfs")
            running_time =round(running_time, 5)
            ai_puzzle_is_solved = True
            render_mgs = "solved ai puzzle"
            show_ai_solution_step = True
        
        elif request.form['requested_action'] == "show_ai_solution_step":
            if len(ai_solution) > 0:
                direction = ai_solution[0]
                ai_puzzle.update_puzzle(direction)
            if len(ai_solution) > 1:
                render_mgs = "show more solution steps"
                show_ai_solution_step = True
            else: 
                render_mgs = "made the last solution step"
                show_ai_solution_step = False
            ai_solution = ai_solution[1:]
            ai_puzzle_is_solved = True





            
    return render_template(
        "index.html",
        render_mgs = render_mgs,
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
        show_ai_solution_step = show_ai_solution_step
        ) 

if __name__ == "__main__":
    app.run(debug=True)