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
            js_data["search_type"] = "ast";            
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
                if((js_data["puzzle_dim"] == 4) && (js_data["search_type"]=="ast")){
                        alert("Warning: Solving complicated 15-puzzles by A*-Search might take several minutes.\r\n\r\nHowever, if you have the patience, A*-search is guaranteed to find the shortest possible solution (fewest number of moves).\r\n\r\nA*-search uses the Manhattan-distance heuristics, but also considers path-length back in time.")
                }
                else {
                    if(js_data["search_type"]=="gbfs"){
                        alert("Greedy Best-First Search will simply try to solve the puzzle as quickly as possible, without considering the number of moves needed to reach the solved state of the puzzle. \r\n\r\Greedy Best-First Search is guided solely by the Manhattan-distance heuristic.")
                    }
                    if(js_data["search_type"]=="dfs"){
                        alert("Solving puzzles by Depth-First Search usually results in solutions with ridiculously many moves. \r\n\r\nIt is an 'un-intelligent' kinds of search, which blindly and stubbornly keeps searching in one direction, making the path longer and longer, untill it either reaches the goal or  a dead end.")
                    }
                    if(js_data["search_type"]=="bfs"){
                        alert("Breath-First search is guaranteed to solve the puzzle in the fewest possible number of moves. \r\n\r\nHowever, it is an 'un-intelligent' kind search, exploring all possible directions blindly, and hence takes a long time. A*-Search is better in all regards.")
                    }
                    if(js_data["search_type"]=="ast"){
                        alert("Like Breath-First search, A*-search is guaranteed to find the shortest possible solution (fewest moves). But it usually does this way faster than Breath-First search since the search is guided by the Manhattan-distance heuristics.")
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
