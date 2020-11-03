// Render puzzles 
render_puzzle(js_data["ai_puzzle"], agent = "ai")
render_puzzle(js_data["human_puzzle"], agent = "human")

// Set eventlisteners
set_global_eventlisteners();

// If solution to computer puzzle is not computed yet
if (!js_data["ai_solution_computed"]){  

    // Set the checked radio-button (defaults to A*-search)
    document.getElementById(js_data["search_type"]).checked = true;

    // Set relevant eventlisteners 
    set_solve_btn_eventlistener()
    set_radio_button_eventlisteners()
}

// If solution to computer puzzle has been computed
else{
    // Set relevant eventlisteners 
    set_reset_btn_eventlisteners()

    // Show the used solution method 
    method_info = "Method: " + js_data["search_names"][js_data["search_type"]];
    document.getElementById("solution-method").innerHTML = method_info;

    // If human interrupts the animated solution by asking for help or moving human puzzle
    // make sure the final solved state of the computer puzzle is shown 
    if (js_data["requested_action"] == "human_move" || js_data["requested_action"] == "help"){
        render_puzzle(js_data["final_state"], "ai")
        document.getElementById("ai_status").innerHTML = "Solved!"
    }
}

if(js_data["puzzle_type"] == "sample"){
    set_help_btn_eventlistener()
}

// On small screens: If human moves are made, scroll to this part of the DOM
let width = (window.innerWidth > 0) ? window.innerWidth : screen.width;
if(width < 950){
    if(js_data["requested_action"] == "human_move"){
        window.location = "#human-board"
    }
    if(js_data["requested_action"] == "help"){
        window.location = "#help-area"
    }
}

// If solution to computer puzzle has just been computed, show animation: 
if(js_data['requested_action'] == 'solve_ai_puzzle'){
    document.getElementById("ai_status").innerHTML = "Showing solution..."
    show_solution_step(0)
}