function render_puzzle(puzzle){
    let dim = js_data["puzzle_dim"]
    for (let i=0; i < dim; i++) {
        for (let j=0; j < dim; j++){
            id = "tile" + i.toString() + j.toString();
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
    
    var time_delay = 250;
    
    setTimeout(function() {   //  
        let puzzle = js_data['animated_solution'][move_num]
        render_puzzle(puzzle)
        move_num ++;                    
        document.getElementById("move_count").innerHTML = `#Moves: ${move_num}`;
        if (move_num < js_data['num_solution_steps']) {          
            show_solution_step(move_num);              
        } 
        else{
            document.getElementById("status").innerHTML = "Solved!"
        }                      
    }, time_delay);
}