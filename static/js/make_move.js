function get_zero_pos(puzzle){
    for (let i = 0; i < 3; i++){
        for (let j = 0; j < 3; j++){
            if(puzzle[i][j] == 0){
                return {"zero_row":i, "zero_col":j}
            }
        }
    }
}

function make_move(puzzle, direction, zero_col, zero_row){
    /*
    Update the puzzle by moving the zero tile in the given direction
    */
    if (direction == "l"){
        if(zero_col - 1 > 0){
        puzzle[zero_row][zero_col] = puzzle[zero_row][zero_col - 1];
        puzzle[zero_row][zero_col - 1] = 0;
        zero_col -= 1;
        }
    }
    else if(direction == "r"){
        if(zero_col + 1 < 2){
        puzzle[zero_row][zero_col] = puzzle[zero_row][zero_col + 1];
        puzzle[zero_row][zero_col + 1] = 0;
        zero_col += 1;
        }
    }
    else if(direction == "u"){
        if(zero_row - 1 > 0){
        puzzle[zero_row][zero_col] = puzzle[zero_row - 1][zero_col];
        puzzle[zero_row - 1][zero_col] = 0;
        zero_row -= 1;
        }
    }
    else if(direction == "d"){
        if(zero_row + 1 < 2){
        puzzle[zero_row][zero_col] = puzzle[zero_row + 1][zero_col];
        puzzle[zero_row + 1][zero_col] = 0;
        zero_row += 1;
        }
    }
}

puzzle=[[1,9,2],
        [3,4,5],
        [6,0,4]]

console.log(get_zero_pos(puzzle))