// Render puzzle
render_puzzle(js_data["puzzle"])

// Set global eventlisteners
set_eventlisteners();

// Set the checked radio-button (defaults to A*-search)
document.getElementById(js_data["search_type"]).checked = true;

// Show solution method in a nice, readable way
if(js_data["show_solution_details"]){
    method_info = js_data["search_names"][js_data["search_type"]];
    document.getElementById("solution-method").innerHTML = method_info;
}

// On small screens: If moves by arrow keys are made, scroll to this part of the DOM
let width = (window.innerWidth > 0) ? window.innerWidth : screen.width;
if(width < 950){
    if(js_data["requested_action"] == "move"){
        window.location = "#title";
    }
}

// If solution to computer puzzle has just been computed, do the following: 
if(js_data['requested_action'] == 'solve_puzzle'){
    // Show animation on screen
    document.getElementById("status").innerHTML = "Showing solution..."
    show_solution_step(move_num = 0, time_delay=200 )
    // Set puzzle equal to original puzzle to make reset possible
    js_data["puzzle"]=js_data["original_puzzle"]
}