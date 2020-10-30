function render_puzzle(puzzle, agent){
    for (let i=0; i < 3; i++) {
        for (let j=0; j<3; j++){
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
    // shows this animated computer solution    
    
    const time_delay = 150;

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