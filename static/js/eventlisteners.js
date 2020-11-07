function submit(){
    js_data['animated_solution'] = []; // clear variable
    document.getElementById("json_data").value = JSON.stringify(js_data);
    document.getElementById("form").submit();
}

function set_eventlisteners(){
    // Event handlers 

    document.getElementById("new_sample_btn").addEventListener('click', event => {
        js_data["requested_action"] = "new_sample";
        js_data["puzzle_type"] = "sample"
        submit();
    })

    document.getElementById("make_custom_btn").addEventListener('click', event => {
        js_data['requested_action'] = "show_solved_puzzle";
        js_data['puzzle_type'] = "custom";
        submit();
    })

    document.getElementById("change_puzzle_dim_link").addEventListener('click', event => {
        // User wants to change size of puzzle
        if(js_data["puzzle_dim"] == 3){
            js_data["puzzle_dim"] = 4;
            js_data["search_type"] = "gbfs";            
        } else{
            js_data["puzzle_dim"] = 3;
            js_data["search_type"] = "ast_alt";            
        }
        js_data['puzzle_type'] = "sample"
        js_data['requested_action'] = "new_sample"
        submit();
    })

    function human_move(direction){
        js_data["direction"] = direction;
        js_data["requested_action"] = "human_move"
        submit()
    }

    document.getElementById("solve_reset_btn").addEventListener('click', event => {
        let button_value = document.getElementById("solve_reset_btn").value 
        if(button_value == "Solve"){
            if(js_data["puzzle_is_solved"]){
                document.getElementById("status").innerHTML = "Puzzle already solved"
                return
            }         
            document.getElementById("status").innerHTML = "Searching...";
            js_data["requested_action"] = "solve_puzzle";
            document.getElementById("solve_reset_btn").value="Stop"
        } else{
            // Button value is "Stop" or "Reset"
            js_data["requested_action"] = "reset";
        }
        submit();                
        
    })

    for (let i = 0; i < js_data["all_search_types"].length; i++) {
        document.getElementById(js_data["all_search_types"][i]).addEventListener('change', event => {
            js_data["search_type"] = js_data["all_search_types"][i];
            if(js_data["puzzle_dim"] == 4){
                if(js_data["search_type"]=="ast_alt"){
                    alert("Warning: Solving complicated 15-puzzles by A*-search might take several minutes.\r\n\r\nHowever, if you have the patience, you might find an elegant solution with fewer moves a the solution found by greedy best-first search.")
                }
            }
            if(js_data["puzzle_dim"] == 3){
                if(js_data["search_type"]=="gbfs"){
                    alert("Greedy best-first search is a fast and reliable, but the solutions found by this algorithm typically involve more moves than a solution found with A*-search or best-first search.")
                }
                if(js_data["search_type"]=="dfs"){
                    alert("Solving puzzles by depth-first usually results in solutions with ridiculously many moves.")
                }
            }

        })
    }
            
    //Disable default window scrolling on arrow-keys
    window.addEventListener("keydown", function(e) {
        if([37, 38, 39, 40].indexOf(e.keyCode) > -1) {
            e.preventDefault();
        }
    }, false);

    document.addEventListener('keydown', event => {
        switch (event.keyCode){
            case 37: human_move("l");
            break;

            case 39: human_move("r");
            break;

            case 38: human_move("u"); 
            break;

            case 40: human_move("d");
            break;
        }
    }); 
}
