function set_event_listeners(){
    document.getElementById("new_puzzle_btn").addEventListener('click', event => {
        document.getElementById("requested_action").value = "new_puzzle";
        document.getElementById("form").submit();
    })

    document.getElementById("help_btn").addEventListener('click', event => {
        document.getElementById("requested_action").value = "help";
        document.getElementById("form").submit();
    })

    document.getElementById("solve_btn").addEventListener('click', event => {
        if (document.getElementById("solve_btn").value == "Solve"){
            console.log("Solve")
            search_type = document.querySelector('input[name="search_type"]:checked').value;
            document.getElementById("search_type").value = search_type;
            document.getElementById("ai_solve_status").innerHTML = "Calculating..."
            document.getElementById("requested_action").value = "solve_puzzle";
            document.getElementById("form").submit();
        }
        else{
            console.log("unsolve")
            document.getElementById("requested_action").value = "unsolve";
            document.getElementById("form").submit();
        }
    })

    function human_move(direction){
        document.getElementById("requested_action").value = "human_move";
        document.getElementById("human_steps_made").value= "{{human_steps_made}}" + direction;
        document.getElementById("direction").value=direction;
        document.getElementById("form").submit(); 
    }
    
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

