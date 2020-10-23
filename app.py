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

app = Flask(__name__)

def sample_puzzle():
    puzzle = Puzzle(3,3)
    collection = ["rrddlur", "ddruurdd","rdluddrr"]
    puzzle.update_puzzle(random_choice(collection))
    return puzzle

@app.route("/", methods=['GET', 'POST'])
def index():
    # Render new sample puzlle 
    puzzle = sample_puzzle()
    is_solved = puzzle.is_solved()
    return render_template(
        "index.html",
        human_puzzle=puzzle._grid,
        ai_puzzle=puzzle._grid,
        ai_puzzle_is_solved = is_solved,
        human_puzzle_is_solved = is_solved,
        ai_cost = 0,
        human_cost = 0) 
 
@app.route('/solve', methods=['GET','POST'])
def solve():  
    if request.method == "POST":
        # Solve puzzle
        ai_puzzle = request.form['ai_puzzle']
        ai_puzzle = Puzzle(3,3, string_to_grid(''.join(c for c in ai_puzzle if c not in '[]')))

        human_puzzle = request.form['human_puzzle']
        human_puzzle = Puzzle(3,3, string_to_grid(''.join(c for c in human_puzzle if c not in '[]')))
        human_cost = request.form['human_cost']

        solution_string, cost, num_expanded_nodes, max_search_depth, running_time, max_ram_usage \
                = ai_puzzle.solve_puzzle("bfs")
        
        ai_puzzle.update_puzzle(solution_string)

        return render_template("index.html", 
                                human_puzzle=human_puzzle._grid, 
                                ai_puzzle=ai_puzzle._grid,
                                human_puzzle_is_solved = human_puzzle.is_solved(),
                                ai_puzzle_is_solved = ai_puzzle.is_solved(),
                                ai_cost = len(solution_string),
                                human_cost = human_cost,
                                solution_string=solution_string,
                                num_expanded_nodes=num_expanded_nodes,
                                max_search_depth = max_search_depth,
                                max_ram_usage= max_ram_usage) 
    else:
        # Render new sample puzlle 
        puzzle = sample_puzzle()
        is_solved = puzzle.is_solved()
        return render_template(
            "index.html", 
            human_puzzle=puzzle._grid,
            ai_puzzle=puzzle._grid,
            ai_puzzle_is_solved = is_solved,
            human_puzzle_is_solved = is_solved,
            ai_cost = 0,
            human_cost = 0) 
 
           
@app.route('/move', methods=['GET','POST'])
def move():
    if request.method == "POST":
        direction = request.form['direction']
        agent = request.form['agent']
        ai_puzzle = request.form['ai_puzzle']
        ai_puzzle = Puzzle(3,3, string_to_grid(''.join(c for c in ai_puzzle if c not in '[]')))
        ai_cost = request.form['ai_cost']
        human_puzzle = request.form['human_puzzle']
        human_puzzle = Puzzle(3,3, string_to_grid(''.join(c for c in human_puzzle if c not in '[]')))
        human_cost = int(request.form['human_cost']) + 1
        if agent == "human":
            try:         
                human_puzzle.update_puzzle(direction)
            except:
                # move off grid
                pass
        if agent == "ai":
            try:         
                ai_puzzle.update_puzzle(direction)
            except:
                # move off grid
                pass   
        
        return render_template(
            "index.html", 
            human_puzzle=human_puzzle._grid, 
            ai_puzzle=ai_puzzle._grid,
            human_puzzle_is_solved = human_puzzle.is_solved(),
            ai_puzzle_is_solved = ai_puzzle.is_solved(),
            ai_cost = ai_cost,
            human_cost = human_cost)
    else:
        # Render new sample puzlle 
        puzzle = sample_puzzle()
        is_solved = puzzle.is_solved()
        return render_template(
            "index.html", 
            human_puzzle=puzzle._grid,
            ai_puzzle=puzzle._grid,
            ai_puzzle_is_solved = is_solved,
            human_puzzle_is_solved = is_solved,
            ai_cost = 0,
            human_cost = 0)

if __name__ == "__main__":
    app.run(debug=True)