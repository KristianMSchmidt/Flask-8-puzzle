function set_eventlisteners(js_data){

    function submit(){
        js_data['animated_solution'] = [];
        document.getElementById("json_data").value = JSON.stringify(js_data);
        document.getElementById("form").submit();
    }

    function human_move(direction){
        js_data["direction"] = direction;
        js_data["requested_action"] = "human_move"
        submit()
    }

    //Disable default window scrolling on arrow-keys
    window.addEventListener("keydown", function(e) {
        // space and arrow keys
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

    document.getElementById("new_puzzle_btn").addEventListener('click', event => {
        js_data["requested_action"] = "new_puzzle";
        submit();
    })

    document.getElementById("solve_btn").addEventListener('click', event => {
            document.getElementById("ai_status").innerHTML = "Searching...";
            //search_type = document.querySelector('input[name="search_type"]:checked').value;
            //js_data["search_type"] = search_type;
            js_data["requested_action"] = "solve_ai_puzzle";
            submit();
        });

    document.getElementById("reset_btn").addEventListener('click', event => {
            js_data["requested_action"] = "reset_ai";
            submit();                
        })

    document.getElementById("help_btn").addEventListener('click', event => {
        js_data["requested_action"] = "help";
        submit();
    })

    search_types = ["ast_alt", "gbfs", "bfs", "dfs"]
    if (!js_data["ai_solution_computed"]){
        for (let i = 0; i < search_types.length; i++) {
            document.getElementById(search_types[i]).addEventListener('change', event => {
                js_data["search_type"] = search_types[i];
            })
            
        }        
    }
}