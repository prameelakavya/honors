from back_prop import *
import copy

# assumed board is a list of lists, where inner list values are of cols and outer one's are of rows
# assumed white to be player1 and black to be player2 and training the NN for white

def get_empty_cells(boardd, rows=3, cols=3):
	empty_cells = []
	for i in range(rows):
		for j in range(cols):
			if boardd[i][j] == 0:
				empty_cells.append([i,j])
	return empty_cells

def compute_list_utility(sent_list):
	utility = 0
	if sent_list == [1,1,1]:
		#utility = 100
		return 100
	elif sent_list == [-1,-1,-1]:
		#utility = -100
		return -100
	elif sent_list == [1,1,0] or sent_list == [1,0,1] or sent_list == [0,1,1]:
		utility += 10
	elif sent_list == [-1,-1,0] or sent_list == [-1,0,-1] or sent_list == [0,-1,-1]:
		utility += -10
	elif sent_list == [1,0,0] or sent_list == [0,1,0] or sent_list == [0,0,1]:
		utility += 1
	elif sent_list == [-1,0,0] or sent_list == [0,-1,0] or sent_list == [0,0,-1]:
		utility += -1
	return utility

def utility_check(board, rows=3, cols=3):
	utility = 0
	# 3 rows utility 
	for i in range(rows):
		if compute_list_utility(board[i]) == 100 or compute_list_utility(board[i]) == -100:
			return compute_list_utility(board[i])
		else:
			utility += compute_list_utility(board[i])
        print utility
	# 3 cols utility
	for j in range(cols):
		column = []
		for i in range(rows):
			column.append(board[i][j])
		if compute_list_utility(column) == 100 or compute_list_utility(column) == -100:
			return compute_list_utility(column)
		else:
			utility += compute_list_utility(column)
        print utility
		
	# 2 diagonals utility 
	diag1 = [board[0][0], board[1][1], board[2][2]]
	diag2 = [board[0][2], board[1][1], board[2][0]]
	for k in [diag1, diag2]:
		if compute_list_utility(k) == 100 or compute_list_utility(k) == -100:
			return compute_list_utility(k)
		else:
			utility += compute_list_utility(k)
        print utility
	return utility
			
def black_move(board):
	reward = 1000
	cells = get_empty_cells(board)
	for i in cells :
		temp_board = copy.deepcopy(board)
		temp_board[i[0]][i[1]] = -1 # assuming black is player2 as so replacing with 2
                print temp_board
		current_max = min(reward, utility_check(temp_board))
		if reward >= current_max:
			reward = current_max
			best_cell = i
	return [reward, best_cell]
			 
			
def testing(board, myNN):
	cells = get_empty_cells(board)
	for i in cells:
		temp_board = copy.deepcopy(board)
		temp_board[i[0]][i[1]] = 1
		print i , "  -->  " , myNN.runNN(temp_board)
					

def main():
	myNN = NN ( 9, 25, 1)
	n = 0.5
	m = 0.1
	for games in range(1000):
		board = [[0,0,0],[0,0,0],[0,0,0]]
		#print board
		while 1:
			actions = get_empty_cells(board)
			if len(actions) == 0:
				break
			reward = -1000
			for i in actions:
				temp_board = copy.deepcopy(board)
				temp_board[i[0]][i[1]] = 1
				current_max = max(reward, myNN.runNN(temp_board)[0])
				if reward <= current_max:
					reward = current_max
					best_cell = i
			#print board
			print best_cell
			board[best_cell[0]][best_cell[1]] = 1
			print board
			Qout = reward
			reward = utility_check(board)
                        #print reward
			reward = float(reward)/100.0
                        print reward
			if reward == 1:
				Qtarget = (1 - n)*Qout + n
				myNN.runNN(board)
				myNN.backPropagate([Qtarget], n, m)
				break
			else:
				black = black_move(copy.deepcopy(board))
                                print "black:" , black
                                print black[0]/100.0
				if black[0]/100.0 == -1:
                                        print "000"
					myNN.runNN(board)
					board[black[1][0]][black[1][1]]	= -1
					Qtarget = (1 - n)*Qout - n
					myNN.backPropagate([Qtarget], n, m)
					break
				else:
					temp_board = copy.deepcopy(board)
					temp_board[black[1][0]][black[1][1]] = -1 # black did a move
					secondary_actions = get_empty_cells(copy.deepcopy(temp_board))
                                        print secondary_actions
					if len(secondary_actions) == 0:
                                                print 777
						Qtarget = (1 - n)*Qout
						myNN.runNN(board)
						board[black[1][0]][black[1][1]]	= -1
						myNN.backPropagate([Qtarget], n, m)
						break
					reward = -1000
					for i in secondary_actions:
                                                print 888
						temp_board_new = copy.deepcopy(temp_board)
						temp_board_new[i[0]][i[1]] = 1
						current_max = max(reward, myNN.runNN(temp_board)[0])
						if reward != current_max:
							reward = current_max
							#best_cell = i
					Qtarget = (1 - n)*Qout + n*(m*reward)
					myNN.runNN(board)
					board[black[1][0]][black[1][1]]	= -1
                                        print "bothmoves:",board
					myNN.backPropagate([Qtarget], n, m)
	
	
	
	testing([[0,-1,0],[1,-1,0],[1,0,0]], myNN)


					
if __name__ == "__main__":
    main()					
					
					
					
					
							
			
			
			
			
			
			
			
			
			
			
