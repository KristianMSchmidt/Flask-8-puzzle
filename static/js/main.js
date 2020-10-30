// Render puzzles 
render_puzzle(js_data["ai_puzzle"], agent = "ai")
render_puzzle(js_data["human_puzzle"], agent = "human")

// Set eventlisteners
set_eventlisteners(js_data);

// Set the checked radio-button (defaults to A*-search)
document.getElementById(js_data["search_type"]).checked = true;

// If solution to computer puzzle is computed
if (js_data["ai_solution_computed"]){
    
    // Hide select-algorithm area and solve button
    document.getElementById("select-algorithm-area").style.display="none"
    document.getElementById("solve_btn").style.display = "none";

    // Show solution method in a nice way
    method_info = "Solution method: " 
    if(js_data["search_type"]=="ast_alt"){
        method_info += "A*"
    } else if(js_data["search_type"]=="gbfs"){
        method_info += "GBFS"
    } else if(js_data["search_type"]=="bfs"){
        method_info += "BFS"
    } else if(js_data["search_type"]=="dfs"){
        method_info += "DFS"
    }
    document.getElementById("solution-method").innerHTML = method_info
    document.getElementById("solution-method").innerHTML = method_info

    // If human interrupts the animated solution by asking for help or moving human puzzle
    // make sure the final solved state of the computer puzzle is shown 
    if (js_data["requested_action"] == "human_move" || js_data["requested_action"] == "help"){
        solved_puzzle = js_data['animated_solution'][js_data['ai_num_solution_steps'] - 1]
        render_puzzle(solved_puzzle, "ai")
        document.getElementById("ai_status").innerHTML = "Solved!"
    }
}
// If solution to computer puzzle is not computed yet
else{
    //hide solution details area
    document.getElementById("solution-details-area").style.display = "none";
    
    //hide reset button 
    document.getElementById("reset_btn").style.display = "none";
}

// Set value of human puzzle status output depinding on state
if(js_data["human_puzzle_is_solved"]){
    document.getElementById("human_puzzle_status").innerHTML = "Solved!";
} else{
    document.getElementById("human_puzzle_status").innerHTML = "Not solved yet";
}

// Hide help-box unless the last request was asking for help
if (js_data["requested_action"] != "help"){
    document.getElementById("help-container").style.display = "none"
}

if( js_data["requested_action"] == "human_move"){
    window.location = (""+window.location).replace(/#[A-Za-z0-9_]*$/,'')+"#human-board"
}

// If solution to computer puzzle has just been computed, show animation: 
if(js_data['requested_action'] == 'solve_ai_puzzle'){
    show_solution_step(0)
}