function submit(){
    js_data['animated_solution'] = []; // clear variable
    document.getElementById("json_data").value = JSON.stringify(js_data);
    document.getElementById("form").submit();
}

function set_global_eventlisteners(js_data){
    // Event handlers that should be defined in all game states

    document.getElementById("make_custom_btn").addEventListener('click', event => {
        js_data['requested_action'] = "show_solved_puzzle";
        submit();
    })
    
    document.getElementById("send_to_ai_btn").addEventListener('click', event => {
        js_data['ai_puzzle'] = js_data['human_puzzle'];
        js_data['puzzle_title'] = "Custom Puzzle";
        document.getElementById("ai_title").innerHTML = "Custom Puzzle";
        render_puzzle(js_data["ai_puzzle"], agent = "ai")

    })

    document.getElementById("change_puzzle_dim_link").addEventListener('click', event => {
        // User wants to change size of puzzle
        if(js_data["puzzle_dim"] == 3){
            js_data["puzzle_dim"] = 4;
        } else{
            js_data["puzzle_dim"] = 3;
        }
        js_data['requested_action'] = "new_sample"
        submit();
    })

    function human_move(direction){
        js_data["direction"] = direction;
        js_data["requested_action"] = "human_move"
        submit()
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

    document.getElementById("new_sample_btn").addEventListener('click', event => {
        js_data["requested_action"] = "new_sample";
        submit();
    })

    document.getElementById("help_btn").addEventListener('click', event => {
        if(document.getElementById("help-area")){
            document.getElementById("help-area").innerHTML = "<h4>Here's a hint</h4><p>Generating help...</p>";
        } else{
            document.getElementById("human_status").innerHTML = "Generating help..."
        }

        js_data["requested_action"] = "help";
        submit();
        })
}

function set_eventlisteners_ai_not_solved(){
    // These eventlisteners should only be set when ai puzzle is not yet solved

    document.getElementById("solve_btn").addEventListener('click', event => {
            document.getElementById("ai_status").innerHTML = "Searching...";
            js_data["requested_action"] = "solve_ai_puzzle";
            submit();
    });   
    search_types = ["ast_alt", "gbfs", "bfs", "dfs"]
    if (!js_data["ai_solution_computed"]){
        for (let i = 0; i < search_types.length; i++) {
            document.getElementById(search_types[i]).addEventListener('change', event => {
                js_data["search_type"] = search_types[i];
            })
            
        }        
    }
}

function set_eventlisteners_ai_solved(){
    // These eventlisteners should only be set when ai puzzle is solved
    document.getElementById("reset_btn").addEventListener('click', event => {
        js_data["requested_action"] = "reset_ai";
        submit();                
    })
}
