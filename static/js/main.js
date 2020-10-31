// Render puzzles 
render_puzzle(js_data["ai_puzzle"], agent = "ai")
render_puzzle(js_data["human_puzzle"], agent = "human")

// Set eventlisteners
set_global_eventlisteners(js_data);

// If solution to computer puzzle is not computed yet
if (!js_data["ai_solution_computed"]){  
    // Set relevant eventlisteners 
    set_eventlisteners_ai_not_solved(js_data)
 
    // Set the checked radio-button (defaults to A*-search)
    document.getElementById(js_data["search_type"]).checked = true;
}

// If solution to computer puzzle has been computed
else{
    // Set relevant eventlisteners 
    set_eventlisteners_ai_solved(js_data)

    // Show the used solution method in a nice way
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

    // If human interrupts the animated solution by asking for help or moving human puzzle
    // make sure the final solved state of the computer puzzle is shown 
    if (js_data["requested_action"] == "human_move" || js_data["requested_action"] == "help"){
        console.log(js_data["final_state"])
        render_puzzle(js_data["final_state"], "ai")
        document.getElementById("ai_status").innerHTML = "Solved!"
    }
}

// If human moves are made, scroll to this part of the DOM (relevant for small screens)
if( js_data["requested_action"] == "human_move"){
    window.location = "#human-board"
}

// If solution to computer puzzle has just been computed, show animation: 
if(js_data['requested_action'] == 'solve_ai_puzzle'){
    document.getElementById("ai_status").innerHTML = "Showing solution..."
    show_solution_step(0)
}