function submit(){
    js_data['animated_solution'] = []; // clear variable
    document.getElementById("json_data").value = JSON.stringify(js_data);
    document.getElementById("form").submit();
}

function set_global_eventlisteners(){
    // Event handlers that should be defined in in all states

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
        if(js_data["solve_or_reset_btn_value"] == "Solve"){
           
            if (js_data["puzzle_dim"] == 4 && js_data["search_type"]=="ast_alt"){
                alert("It might take several minutes to solve complicated 15-puzzles by A*-search.\r\n\r\nHowever, if you have patience, you might find a solution with fewer moves than the one found with Gready best-first search")
            }      
            document.getElementById("status").innerHTML = "Searching...";
            document.getElementById("solve_reset_btn").disabled = true;
            js_data["requested_action"] = "solve_puzzle";
        } else{
            js_data["requested_action"] = "reset";
        }
        submit();                
        
    })

    for (let i = 0; i < js_data["all_search_types"].length; i++) {
        document.getElementById(js_data["all_search_types"][i]).addEventListener('change', event => {
            js_data["search_type"] = js_data["all_search_types"][i];
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
