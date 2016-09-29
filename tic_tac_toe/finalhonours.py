import sys
import random
import signal
import copy
from back_prop import *

class TimedOutExc(Exception):
        pass

def handler(signum, frame):
    #print 'Signal handler called with signal', signum
    raise TimedOutExc()

class heuristic_agent:
	def __init__(self):
		pass

	def compute_list_utility(self,sent_list):
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

	def utility_check(self,board, rows=3, cols=3):
		utility = 0
		# 3 rows utility 
		for i in range(rows):
			var = self.compute_list_utility(board[i])
			if var == 100 or var == -100:
				return var
			else:
				utility += var
        
		# 3 cols utility
		for j in range(cols):
			column = []
			for i in range(rows):
				column.append(board[i][j])
			var = self.compute_list_utility(column)
			if var == 100 or var == -100:
				return var
			else:
				utility += var
        
		
		# 2 diagonals utility 
		diag1 = [board[0][0], board[1][1], board[2][2]]
		diag2 = [board[0][2], board[1][1], board[2][0]]
		for k in [diag1, diag2]:
			var = self.compute_list_utility(k)
			if var == 100 or var == -100:
				return var
			else:
				utility += var
        	
		return utility

	def move(self,temp_board,old_move,flag):
		actions = get_empty_cells(temp_board)
		output = -10000
		best_cell = (-1,-1)
		for i in actions:
			tempboardnew = copy.deepcopy(temp_board)
			tempboardnew[i[0]][i[1]] = flag
			number_tempboardnew = [[0,0,0],[0,0,0],[0,0,0]]	
			
			for u in range(3):
				for v in range(3):
					if tempboardnew[u][v] == flag:
						number_tempboardnew[u][v] = 1
					elif tempboardnew[u][v] == '-':
						True
					else:
						number_tempboardnew[u][v] = -1
			
			current_max = self.utility_check(number_tempboardnew)
			if current_max >= output:
				output = current_max
				best_cell = i

		return (best_cell[0],best_cell[1],output)
		


class Manual_player:
	def __init__(self):
		pass
	def move(self, temp_board, old_move, flag):
		print 'Enter your move: <format:row column> (you\'re playing with', flag + ")"	
		mvp = raw_input()
		mvp = mvp.split()
		return (int(mvp[0]), int(mvp[1]),0)

class Random_Player:
	def __init__(self):
		pass
	def move(self, temp_board, old_move, flag):
		cells = get_empty_cells(temp_board)
		chose = cells[random.randrange(len(cells))]
		return (chose[0],chose[1],0)

class Player1:

	def __init__(self,hiddennodes):
		self.myNN = NN(9,hiddennodes,1)
		self.n = 0.5
		self.m = 0.1

	def move(self,temp_board,old_move,flag):
		actions = get_empty_cells(temp_board)
		output = -10000
		best_cell = (-1,-1)
		for i in actions:
			tempboardnew = copy.deepcopy(temp_board)
			tempboardnew[i[0]][i[1]] = flag
			number_tempboardnew = [[0,0,0],[0,0,0],[0,0,0]]	
			
			for u in range(3):
				for v in range(3):
					if tempboardnew[u][v] == flag:
						number_tempboardnew[u][v] = 1
					elif tempboardnew[u][v] == '-':
						True
					else:
						number_tempboardnew[u][v] = -1

			current_max = self.myNN.runNN(number_tempboardnew)[0]
			if current_max >= output:
				output = current_max
				best_cell = i
		return (best_cell[0],best_cell[1],output)
	
	def backpropagation_learning(self,reward,Qout,game_board,flag,mesg,old_move):
		temp_req = copy.deepcopy(game_board)
		temp_req[old_move[0]][old_move[1]] = '-'
		required_board = [[0,0,0],[0,0,0],[0,0,0]]	
			
		for u in range(3):
			for v in range(3):
				if temp_req[u][v] == flag:
					required_board[u][v] = 1
				elif temp_req[u][v] == '-':
					True
				else:
					required_board[u][v] = -1

		if reward == -1 or reward == 1 or mesg == 'D':
			Qtarget = (1 - self.n)*Qout + self.n*(reward)
			self.myNN.runNN(required_board)
			self.myNN.backPropagate([Qtarget],self.n,self.m)
			return
		else:
			sec_actions = get_empty_cells(game_board)
			sec_output = -10000
			for i in sec_actions:
				sec_temp_board = copy.deepcopy(game_board)
				sec_temp_board[i[0]][i[1]] = flag
				number_tempboardnew = [[0,0,0],[0,0,0],[0,0,0]]	
			
				for u in range(3):
					for v in range(3):
						if sec_temp_board[u][v] == flag:
							number_tempboardnew[u][v] = 1
						elif sec_temp_board[u][v] == '-':
							True
						else:
							number_tempboardnew[u][v] = -1
				sec_current_max = self.myNN.runNN(number_tempboardnew)[0]

				if sec_current_max >= sec_output:
					sec_output = sec_current_max

			Qtarget = (1 - self.n)*Qout + self.n*(reward + self.m*sec_output)
			self.myNN.runNN(required_board)
			self.myNN.backPropagate([Qtarget],self.n,self.m)
			return	

	def testing(self,board) :
		cells = get_empty_cells(board)
		for i in cells:
			temp_board = copy.deepcopy(board)
			temp_board[i[0]][i[1]] = 1
			print i , "  -->  " , self.myNN.runNN(temp_board)	
		
		

class Player2:
	def __init__(self):
		self.myNN = NN(9,27,1)
		self.n = 0.5
		self.m = 0.1

	def move(self,temp_board,old_move,flag):
		actions = get_empty_cells(temp_board)
		output = -10000
		best_cell = (-1,-1)
		for i in actions:
			tempboardnew = copy.deepcopy(temp_board)
			tempboardnew[i[0]][i[1]] = flag
			number_tempboardnew = [[0,0,0],[0,0,0],[0,0,0]]	
			
			for u in range(3):
				for v in range(3):
					if tempboardnew[u][v] == flag:
						number_tempboardnew[u][v] = 1
					elif tempboardnew[u][v] == '-':
						True
					else:
						number_tempboardnew[u][v] = -1

			current_max = self.myNN.runNN(number_tempboardnew)[0]
			if current_max >= output:
				output = current_max
				best_cell = i
		return (best_cell[0],best_cell[1],output)
	
	def backpropagation_learning(self,reward,Qout,game_board,flag,mesg):
		if reward == -1 or reward == 1 or mesg == 'D':
			Qtarget = (1 - self.n)*Qout + self.n*(reward)
			self.myNN.backPropagate([Qtarget],self.n,self.m)
			return
		else:
			sec_actions = get_empty_cells(game_board)
			sec_output = -10000
			for i in sec_actions:
				sec_temp_board = copy.deepcopy(game_board)
				sec_temp_board[i[0]][i[1]] = flag
				number_tempboardnew = [[0,0,0],[0,0,0],[0,0,0]]	
			
				for u in range(3):
					for v in range(3):
						if sec_temp_board[u][v] == flag:
							number_tempboardnew[u][v] = 1
						elif sec_temp_board[u][v] == '-':
							True
						else:
							number_tempboardnew[u][v] = -1
				sec_current_max = self.myNN.runNN(number_tempboardnew)[0]

				if sec_current_max >= sec_output:
					sec_output = sec_current_max
			Qtarget = (1 - self.n)*Qout + self.n*(reward + self.m*sec_output)
			self.myNN.backPropagate([Qtarget],self.n,self.m)
			return		
		

class Player3:
	def __init__(self):
		self.myNN = NN(9,27,1)
		self.n = 0.5
		self.m = 0.1


	def move(self,temp_board,old_move,flag):
		actions = get_empty_cells(temp_board)
		output = -10000
		best_cell = (-1,-1)
		for i in actions:
			tempboardnew = copy.deepcopy(temp_board)
			tempboardnew[i[0]][i[1]] = flag
			number_tempboardnew = [[0,0,0],[0,0,0],[0,0,0]]	
			
			for u in range(3):
				for v in range(3):
					if tempboardnew[u][v] == flag:
						number_tempboardnew[u][v] = 1
					elif tempboardnew[u][v] == '-':
						True
					else:
						number_tempboardnew[u][v] = -1

			current_max = self.myNN.runNN(number_tempboardnew)[0]
			if current_max >= output:
				output = current_max
				best_cell = i
		return (best_cell[0],best_cell[1],output)

	def minimax(self,root_board,flag1,flag2,maxnode,depth,alpha,beta):
		state_val = terminal_utility(root_board,flag1,flag2,depth)
		if  state_val != 10000:
			return state_val
		else:
			children = get_empty_cells(root_board)
			for child in children:
				if maxnode:
					root_board[child[0]][child[1]] = flag1
				else:
					root_board[child[0]][child[1]] = flag2
				if maxnode:
					score = self.minimax(root_board,flag1,flag2,False,depth+1,alpha,beta)
					if (score > alpha):
	        	          		alpha = score
				else:
					score = self.minimax(root_board,flag1,flag2,True,depth+1,alpha,beta)
					if (score < beta):
	        	          		beta = score
				root_board[child[0]][child[1]] = 0 
			if maxnode:
				return alpha
			else:
				return beta
				
	
	def backpropagation_learning(self,reward,Qout,game_board,flag,mesg):
		if reward == -1 or reward == 1 or mesg == 'D':
			Qtarget = (1 - self.n)*Qout + self.n*(reward)
			self.myNN.backPropagate([Qtarget],self.n,self.m)
			return
		else:
			sec_actions = get_empty_cells(game_board)
			sec_output = -10000
			best_cell = (-1,-1)
			for i in sec_actions:
				sec_temp_board = copy.deepcopy(game_board)
				sec_temp_board[i[0]][i[1]] = flag
				number_tempboardnew = [[0,0,0],[0,0,0],[0,0,0]]	
			
				for u in range(3):
					for v in range(3):
						if sec_temp_board[u][v] == flag:
							number_tempboardnew[u][v] = 1
						elif sec_temp_board[u][v] == '-':
							True
						else:
							number_tempboardnew[u][v] = -1 
				####### MINIMAX ##############
				score = self.minimax(number_tempboardnew,1,-1,False,0,-1000,1000)
				if score >= sec_output:
					sec_output = score
					best_cell = i
			print sec_output
			print "minimax: " 
			print best_cell
			sec_temp_board = copy.deepcopy(game_board)
			sec_temp_board[best_cell[0]][best_cell[1]] = flag
			number_tempboardnew = [[0,0,0],[0,0,0],[0,0,0]]	
			for u in range(3):
				for v in range(3):
					if sec_temp_board[u][v] == flag:
						number_tempboardnew[u][v] = 1
					elif sec_temp_board[u][v] == '-':
						True
					else:
						number_tempboardnew[u][v] = -1 

			sec_output = self.myNN.runNN(number_tempboardnew)[0]
			Qtarget = (1 - self.n)*Qout + self.n*(reward + self.m*sec_output)
			self.myNN.backPropagate([Qtarget],self.n,self.m)
			return
					


def get_empty_cells(boardd, rows=3, cols=3):
	empty_cells = []
	for i in range(rows):
		for j in range(cols):
			if boardd[i][j] == '-' or boardd[i][j] == 0:
				empty_cells.append([i,j])
	return empty_cells


def get_init_board():
	board = []
	for i in range(3):
		row = ['-']*3
		board.append(row)
	
	return board

def print_lists(gb):
	print '=========== Game Board ==========='
	for i in range(3):
		for j in range(3):
			print gb[i][j],

		print
	print "=================================="


def verification_fails_board(board_game, temp_board_state):
	return board_game == temp_board_state	



def check_valid_move(game_board, current_move, old_move):

	# first we need to check whether current_move is tuple of not
	# old_move is guaranteed to be correct
	if type(current_move) is not tuple:
		return False
	
	if len(current_move) != 3:
		return False

	a = current_move[0]
	b = current_move[1]	

	if type(a) is not int or type(b) is not int:
		return False
	if a < 0 or a > 2 or b < 0 or b > 2:
		return False

	#Special case at start of game, any move is okay!
	if old_move[0] == -1 and old_move[1] == -1:
		return True
        
        # We get all the empty cells in allowed blocks. If they're all full, we get all the empty cells in the entire board.
        cells = get_empty_cells(game_board)

	#Checks if you made a valid move. 
        if [current_move[0],current_move[1]] in cells:
     	    return True
        else:
	    
    	    return False


def update_lists(game_board, move_ret, fl):
	#move_ret has the move to be made, so we modify the game_board, and then check if we need to modify block_stat
	game_board[move_ret[0]][move_ret[1]] = fl
	return


def terminal_utility(root_board,flag1,flag2,depth):
	for rows in range(3):
		if root_board[rows] == [flag1,flag1,flag1]:
			return 10 - depth
		elif root_board[rows] == [flag2,flag2,flag2]:
			return depth - 10
		else:
			True
	for cols in range(3):
		column = []
		for i in range(3):
			column.append(root_board[i][cols])
		if column == [flag1,flag1,flag1]:
			return 10 - depth
		elif column == [flag2,flag2,flag2]:
			return depth - 10
		else:
			True
	diag1 = [root_board[0][0], root_board[1][1], root_board[2][2]]
	diag2 = [root_board[0][2], root_board[1][1], root_board[2][0]]
	if diag1 == [flag1,flag1,flag1] or diag2 == [flag1,flag1,flag1]:
		return 10 - depth
	elif diag1 == [flag2,flag2,flag2] or diag2 == [flag2,flag2,flag2]:
		return depth - 10
	else:
		True
	if len(get_empty_cells(root_board)) == 0:
		return 0
	
	return 10000

def terminal_state_reached(game_board,flag):
	for rows in range(3):
		if game_board[rows] == [flag,flag,flag]:
			return True,'W'
	for cols in range(3):
		column = []
		for i in range(3):
			column.append(game_board[i][cols])
		if column == [flag,flag,flag]:
			return True,'W'
	
	diag1 = [game_board[0][0], game_board[1][1], game_board[2][2]]
	diag2 = [game_board[0][2], game_board[1][1], game_board[2][0]]
	if diag1 == [flag,flag,flag] or diag2 == [flag,flag,flag]:
			return True,'W'

	if len(get_empty_cells(game_board)) == 0:
		return True,'D'
	
	return False,'C'

def decide_winner_and_get_message(player,status, message):
	if player == 'P1' and status == 'L':
		return ('P2',message)
	elif player == 'P1' and status == 'W':
		return ('P1',message)
	elif player == 'P2' and status == 'L':
		return ('P1',message)
	elif player == 'P2' and status == 'W':
		return ('P2',message)
	else:
		return ('NO ONE','DRAW')
	return





def simulate(obj1,obj2,start_flag,option,testing_flag):
	# ------------- we should add loop here for number of games agents should play------------------------
	# Game board is a 3x3 list
	game_board = get_init_board()

	pl1 = obj1 
	pl2 = obj2

	### basically, player with flag 'x' will start the game
	pl1_fl = 'x'
	pl2_fl = 'o'

	old_move = (-1, -1,0) # For the first move
	ret_move_pl2 = (-1,-1,0)
	ret_move_pl1 = (-1,-1,0)

	WINNER = ''
	MESSAGE = ''

        #Make your move in 6 seconds!
	TIMEALLOWED = 600

	print_lists(game_board)

	while(1):

		# Player1 will move
		
		temp_board_state = copy.deepcopy(game_board)
	
		signal.signal(signal.SIGALRM, handler)
		signal.alarm(TIMEALLOWED)
		# Player1 to complete in TIMEALLOWED secs. 
		try:
			ret_move_pl1 = pl1.move(temp_board_state, old_move, pl1_fl)
			print ret_move_pl1
		except TimedOutExc as e:
			WINNER, MESSAGE = decide_winner_and_get_message('P1', 'L',   'TIMED OUT')
			break
		signal.alarm(0)
	
                #Checking if list hasn't been modified! Note: Do not make changes in the lists passed in move function!
		if not(verification_fails_board(game_board, temp_board_state)):
			#Player1 loses - he modified something
			WINNER, MESSAGE = decide_winner_and_get_message('P1', 'L',   'MODIFIED CONTENTS OF LISTS')
			break
		
		# Check if the move made is valid
		if not check_valid_move(game_board,ret_move_pl1, old_move):
			## player1 loses - he made the wrong move.
			WINNER, MESSAGE = decide_winner_and_get_message('P1', 'L',   'MADE AN INVALID MOVE')
			break


		print "Player 1 made the move:", ret_move_pl1, 'with', pl1_fl

                #So if the move is valid, we update the 'game_board' and 'block_stat' lists with move of pl1
                update_lists(game_board, ret_move_pl1, pl1_fl)
		

		# Checking if the last move resulted in a terminal state
		gamestatus, mesg =  terminal_state_reached(game_board,pl1_fl)
		reward = 0
		if gamestatus == True and mesg == 'W':
			reward = -1

		old_move = ret_move_pl1
		# for backpropagation of second player
		if(start_flag == 1 and option != '1' and testing_flag == 0):
			pl2.backpropagation_learning(reward,ret_move_pl2[2],game_board,pl2_fl,mesg,old_move)

		elif option == 1 and testing_flag == 0 :
			pl2.backpropagation_learning(reward,ret_move_pl2[2],game_board,pl2_fl,mesg,old_move)


		if gamestatus == True:
			print_lists(game_board)
			WINNER, MESSAGE = decide_winner_and_get_message('P1', mesg,  'COMPLETE')
			if start_flag == 0 and (mesg == 'W' or mesg == 'D'):
				print WINNER + " won!"
				print MESSAGE
				return 1
			else:
				print WINNER + " won!"
				print MESSAGE
				return 0	
			break

		
		#old_move = ret_move_pl1
		print_lists(game_board)

                # Now player2 plays

                temp_board_state = copy.deepcopy(game_board)


		signal.signal(signal.SIGALRM, handler)
		signal.alarm(TIMEALLOWED)
		try:
                	ret_move_pl2 = pl2.move(temp_board_state, old_move, pl2_fl)
			print ret_move_pl2
			print old_move

		except TimedOutExc as e:
			WINNER, MESSAGE = decide_winner_and_get_message('P2', 'L',   'TIMED OUT')
			break
		signal.alarm(0)

                if not (verification_fails_board(game_board, temp_board_state)):
			WINNER, MESSAGE = decide_winner_and_get_message('P2', 'L',   'MODIFIED CONTENTS OF LISTS')
			break
			
                if not check_valid_move(game_board,ret_move_pl2, old_move):
			WINNER, MESSAGE = decide_winner_and_get_message('P2', 'L',   'MADE AN INVALID MOVE')
			break


		print "Player 2 made the move:", ret_move_pl2, 'with', pl2_fl
                
                update_lists(game_board, ret_move_pl2, pl2_fl)

		gamestatus, mesg =  terminal_state_reached(game_board, pl2_fl)
		reward = 0
		if gamestatus == True and mesg == 'W':
			reward = 1

		old_move = ret_move_pl2
		# for backpropagation of first player
		if(start_flag == 0 and option != '1' and testing_flag == 0):
			pl1.backpropagation_learning(reward,ret_move_pl1[2],game_board,pl1_fl,mesg,old_move)

		elif option == 1 and testing_flag == 0 :
			pl1.backpropagation_learning(reward,ret_move_pl1[2],game_board,pl1_fl,mesg,old_move)

                if gamestatus == True:
			print_lists(game_board)
                        WINNER, MESSAGE = decide_winner_and_get_message('P2', mesg,  'COMPLETE' )
			if start_flag == 1 and (mesg == 'W' or mesg == 'D'):
				print WINNER + " won!"
				print MESSAGE
				return 1
			else:
				print WINNER + " won!"
				print MESSAGE
				return 0

                        break
		#old_move = ret_move_pl2
		print_lists(game_board)
	
	#print WINNER + " won!"
	#print MESSAGE


if __name__ == '__main__':
	## get game playing objects

	if len(sys.argv) != 2:
		print 'Usage: python finalhonours.py <option>'
		print '<option> can be 1 => self learning agent vs. self learning agent'
		print '                2 => Human vs. self learning agent'
		print '                3 => heuristic agent  vs. self learning agent'
		sys.exit(1)
 
	obj1 = ''
	obj2 = ''
	option = sys.argv[1]	
	hidden_nodes = 48
	if option == '1':
		obj1 = Player1(hidden_nodes)
		obj2 = Player2()

	elif option == '2':
		obj1 = Player1(hidden_nodes)
		obj2 = Manual_player()
	elif option == '3':
		obj1 = Player1(hidden_nodes)
		obj2 = heuristic_agent()

	elif option == '4':
		obj1 = Player3()
		obj2 = Manual_player()
	
	elif option == '5':
		obj1 = Player1(hidden_nodes)
		obj2 = Random_Player()
        
        # Deciding player1 / player2 after a coin toss
        # However, in the tournament, each player will get a chance to go 1st. 
	loop = 360000
	while loop >=0:
        	num = random.uniform(0,1)
		start_flag = 0
		print num
        	if num > 0.5:
			start_flag = 1
			simulate(obj2, obj1,start_flag,option,0)
		else:
			simulate(obj1, obj2,start_flag,option,0)
		loop = loop - 1
	
	#obj1.testing([[0,-1,0],[1,-1,0],[1,0,0]])
	
	games = 100
	count = 0
	while games >= 0:
		num = random.uniform(0,1)
		start_flag = 0
		#print num
        	if num > 0.5:
			start_flag = 1
			count = count + simulate(obj2, obj1,start_flag,option,1)
		else:
			count = count + simulate(obj1, obj2,start_flag,option,1)
		games = games - 1


	print str(hidden_nodes) + '-->' + str(count) 


