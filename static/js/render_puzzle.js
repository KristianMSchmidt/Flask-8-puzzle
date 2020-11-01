function render_puzzle(puzzle, agent){
    let num_rows = puzzle.length;
    let num_columns = puzzle[0].length; 
    for (let i=0; i < num_rows; i++) {
        for (let j=0; j < num_columns; j++){
            id = agent + i.toString() + j.toString();
            element = document.getElementById(id);
            if(puzzle[i][j] == 0){
                element.classList.add("zero-tile");
                element.innerHTML= "";
            }
            else{
                element.innerHTML=puzzle[i][j];
                element.classList.remove("zero-tile");
            }
        }
     }
}

function show_solution_step(move_num) {  
    /* shows this animated computer solution */   
    
    if(js_data['ai_num_solution_steps'] < 100){
        var time_delay = 250;
    } else{
        var time_delay = 2;
    }
    
    setTimeout(function() {   //  
        let puzzle = js_data['animated_solution'][move_num]
        render_puzzle(puzzle, "ai")
        move_num ++;                    
        document.getElementById("ai_move_count").innerHTML = `#Moves: ${move_num}`;
        if (move_num < js_data['ai_num_solution_steps']) {          
            show_solution_step(move_num);              
        } 
        else{
            document.getElementById("ai_status").innerHTML = "Solved!"
        }                      
    }, time_delay);
}