// Render puzzle
render_puzzle(js_data["puzzle"])

// Disable solve btn if puzzle is solved
if(js_data["puzzle_is_solved"]){
    document.getElementById("solve_reset_btn").disabled = true;
}

// Set global eventlisteners
set_global_eventlisteners();

// Set the checked radio-button (defaults to A*-search)
document.getElementById(js_data["search_type"]).checked = true;

// Show solution method in a nice readable way
if(js_data["show_solution_details"]){
    method_info = js_data["search_names"][js_data["search_type"]];
    document.getElementById("solution-method").innerHTML = method_info;
}

// On small screens: If moves by arrow keys are made, scroll to this part of the DOM
let width = (window.innerWidth > 0) ? window.innerWidth : screen.width;
if(width < 950){
    if(js_data["requested_action"] == "human_move"){
        window.location = "#board"
    }
    if(js_data["requested_action"] == "help"){
        window.location = "#help-area"
    }
}

// If solution to computer puzzle has just been computed, show animation: 
if(js_data['requested_action'] == 'solve_puzzle'){
    document.getElementById("status").innerHTML = "Showing solution..."
    show_solution_step(move_num = 0, time_delay=200 )
    js_data["puzzle"]=js_data["original_puzzle"]
}