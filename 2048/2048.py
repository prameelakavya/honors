
#import poc_2048_gui
from random import randrange
from random import random

UP = 1
DOWN = 2
LEFT = 3
RIGHT = 4
OFFSETS = {UP: (1, 0), DOWN: (-1, 0), LEFT: (0, 1), RIGHT: (0, -1)} 


def merge(line):
    """
    Function that merges a single row or column in 2048
    """
    length = len(line)
    result = [0] * length
    last_index = 0
            
    for current_index in range(length):
        if line[current_index] != 0:
            result[last_index] = line[current_index]
            last_index += 1
    
    for key in range(length - 1):
        if result[key] is result[key + 1]:
            result[key] = result[key] * 2
            result.pop(key + 1)
            result.append(0)
    
    return result

def check_if_changed(merged_grid, cur_grid, direction):
	#print_game(merged_grid)
	#print_game(cur_grid)
	if direction == 1:
		for i in range(len(board)):
			for j in range(len(board[0])):
				if merged_grid[j][i] != cur_grid[i][j]:
					return True
	if direction == 2:
		for i in range(len(board)):
			for j in range(len(board[0])):
				if merged_grid[j][3-i] != cur_grid[i][j]:
					return True
	if direction == 3:
		for i in range(len(board)):
			for j in range(len(board[0])):
				if merged_grid[i][j] != cur_grid[i][j]:
					return True
	if direction == 4:
		for i in range(len(board)):
			for j in range(len(board[0])):
				if merged_grid[i][3-j] != cur_grid[i][j]:
					return True
	return False

class TwentyFortyEight:
    """
    Class to run the game
    """

    def __init__(self, grid_height, grid_width):
        self._grid_height = grid_height
        self._grid_width = grid_width
        self._is_occupied = False
        self._is_changed = True
        self.reset()   
    
    
    def reset(self):
        """
        Reset the game so the grid is empty
        """        
        self._grid = [[0 for this_col in range(self._grid_width)] for this_row in range(self._grid_height)]
        self.new_tile()
        self.new_tile()
            
    def __str__(self):
        """
        Return a string representation of the grid
        """        
        return (self._grid)
    
    def params(self):
    	return [self._is_occupied, self._is_changed]

    def get_grid_height(self):
        """
        Get the height of the board
        """
        return self._grid_height
    
    
    def get_grid_width(self):
        """
        Get the width of the board
        """                
        return self._grid_width
                            

    def move(self, direction):
        """
        Move all tiles in the given direction and add a new tile if any tiles moved
        """
        offset = OFFSETS[direction]
        temp_grid = []
            
        # Up
        if direction == 1:
            for row in range(self._grid_width):
                start = 0
                temp_list = []
                for this_col in range(self._grid_height):
                    temp_list.append(self._grid[start][row])
                    start += offset[0]
                temp_list = merge(temp_list)
                temp_grid.append(temp_list)
            self._is_changed = check_if_changed(temp_grid, self._grid, direction)
            if self._is_changed == True:
            	for row in range(self._grid_height):
            	    for col in range(self._grid_width):
            	        self._grid[row][col] = temp_grid[col][row]
        
        # Down
        elif direction == 2:
            for row in range(self._grid_width):
                start = self._grid_height -1
                temp_list = []
                for this_col in range(self._grid_height):
                    temp_list.append(self._grid[start][row])
                    start += offset[0]
                temp_list = merge(temp_list)
                temp_grid.append(temp_list)
            self._is_changed = check_if_changed(temp_grid, self._grid, direction)
            if self._is_changed == True:
            	for row in range(self._grid_height):
                	for col in range(self._grid_width):
                    		self._grid[row][col] = temp_grid[col][self._grid_height -1 -row]
        
        # Left
        elif direction == 3:
            for col in range(self._grid_height):
                start = 0
                temp_list = []
                for this_row in range(self._grid_width):
                    temp_list.append(self._grid[col][start])
                    start += offset[1]
                temp_list = merge(temp_list)
                temp_grid.append(temp_list)
            self._is_changed = check_if_changed(temp_grid, self._grid, direction)
            if self._is_changed == True:
            	for row in range(self._grid_height):
            	    for col in range(self._grid_width):
            	        self._grid[row][col] = temp_grid[row][col]
                    
        # Right                    
        elif direction == 4:
            for col in range(self._grid_height):
                start = self._grid_width -1
                temp_list = []
                for this_row in range(self._grid_width):
                    temp_list.append(self._grid[col][start])
                    start += offset[1]
                temp_list = merge(temp_list)
                temp_grid.append(temp_list)
            self._is_changed = check_if_changed(temp_grid, self._grid, direction)
            if self._is_changed == True:
            	for row in range(self._grid_height):
            	    for col in range(self._grid_width):
            	        self._grid[row][col] = temp_grid[row][self._grid_width -1 -col]
        
        total_num = 1
        for value in self._grid:
            for val_el in value:
                total_num *= val_el
                if total_num == 0:
                    self._is_occupied = False
                    break
                else:
                    self._is_occupied = True
                    
        if self._is_changed and not self._is_occupied:
            self.new_tile()
        
            
    def new_tile(self):
        """
        Create a new tile
        """              
        probabilities = []
        for this_i in range(100):
            if this_i < 90:
                probabilities.append(2)
            else:
                probabilities.append(4)                      
        while True :
            random_row = randrange(0, self._grid_height)
            random_col = randrange(0, self._grid_width)
            if self._grid[random_row][random_col] is 0 :
                self.set_tile(random_row, random_col, probabilities[int(random() * 100)])
                break
        

    def set_tile(self, row, col, value):
        """
        Set the tile at position [row][col] to the given value
        """
        self._grid[row][col] = value


    def get_tile(self, row, col):
        """
        Return the value of the tile at position [row][col]
        """          
        return self._grid[row][col]
        
    def set_grid(self, board):
    	for i in range(len(board)):
    		for j in range(len(board[0])):
    			self._grid[i][j] = board[i][j]

def print_game(board):
	for i in range(len(board)):
		print "-------------------------"
		for j in range(len(board[0])):
			print "|" + str(board[i][j]) + (4 - len(str(board[i][j]))) * " ",
		print "|"
	print "-------------------------"

def get_empty_cells(board):
	cells = []
	for i in range(len(board)):
		for j in range(len(board[0])):
			if board[i][j] == 0:
				cells.append([i,j])
	return cells

def heuristic(board):
	dummy_grid = TwentyFortyEight(4,4)
	ans = -1
	direction = -1
	#UP
	dummy_grid.set_grid(board)
	dummy_grid.move(1)
	if dummy_grid.params()[1] == True:
		prev_ans = ans
		ans = max(ans, len(get_empty_cells(dummy_grid.__str__())))
		if ans > prev_ans:
			direction = 1
	#DOWN
	dummy_grid.set_grid(board)
	dummy_grid.set_grid(board)
	dummy_grid.move(2)
	if dummy_grid.params()[1] == True:
		prev_ans = ans
		ans = max(ans, len(get_empty_cells(dummy_grid.__str__())))
		if ans > prev_ans:
			direction = 2
	#LEFT
	dummy_grid.set_grid(board)
	dummy_grid.move(3)
	if dummy_grid.params()[1] == True:
		prev_ans = ans
		ans = max(ans, len(get_empty_cells(dummy_grid.__str__())))
		if ans > prev_ans:
			direction = 3
	#RIGHT
	dummy_grid.set_grid(board)
	dummy_grid.move(4)
	if dummy_grid.params()[1] == True:
		prev_ans = ans
		ans = max(ans, len(get_empty_cells(dummy_grid.__str__())))
		if ans > prev_ans:
			direction = 4
	
	return direction		
			
if __name__ == "__main__":
	game_obj = TwentyFortyEight(4,4)
	while(1):
		board = game_obj.__str__()
		print_game(board)
		#print str(board) + "  " ,
		flag = 0
		for i in range(len(board)):
			for j in range(len(board[0])):
				if board[i][j] == 2048:
					print "YOU WON!!"
					flag = 1
					break
		if flag == 1:
			break
		direction = heuristic(board)
		print "direction:  " + str(direction) 
		#print str(direction)
		if direction == -1:
			print "Game ended!!"
			break
		game_obj.move(direction)
		
#poc_2048_gui.run_gui(TwentyFortyEight(4, 4))


