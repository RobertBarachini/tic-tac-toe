import numpy as np

# Globals
nodes_count = 0
visits = 0
states = {}
stats = {3: 0, 4: 0, 5: 0}
stats_unique = {3: 0, 4: 0, 5: 0}
stat_states = {3: [], 4: [], 5: []}


def print_board(board: np.ndarray) -> None:
	'''
	Prints a tic-tac-toe board.
	'''
	for i in range(3):
		for j in range(3):
			val = board[i][j]
			to_print = ' '
			if val == 1:
				to_print = 'X'
			elif val == 2:
				to_print = 'O'
			print(to_print, end='')
			if j < 2:
				print(' | ', end='')
		if i < 2:
			print('\n--+---+--', end='')
		print()


def get_board_string(board: np.ndarray) -> str:
	'''
	Returns a string representation of the board on one line.
	'''
	s = ''
	for i in range(3):
		s += f'{board[i][0]}{board[i][1]}{board[i][2]}'
	return s


def init_board() -> np.ndarray:
	'''
	Initializes a 3x3 tic-tac-toe board.
	'''
	return np.zeros((3, 3), dtype=int)


def get_winner(board: np.ndarray) -> int:
	'''
	Returns the winner of the game.
	'''
	# check rows
	for i in range(3):
		if board[i][0] == board[i][1] == board[i][2] != 0:
			return board[i][0]
	# check columns
	for i in range(3):
		if board[0][i] == board[1][i] == board[2][i] != 0:
			return board[0][i]
	# check diagonals
	if board[0][0] == board[1][1] == board[2][2] != 0:
		return board[0][0]
	if board[0][2] == board[1][1] == board[2][0] != 0:
		return board[0][2]
	# no winner
	return 0


def is_full(board: np.ndarray) -> bool:
	'''
	Returns true if the board is full.
	'''
	for i in range(3):
		for j in range(3):
			if board[i][j] == 0:
				return False
	return True


def print_tree(tree: dict[str, dict], depth: int = 0) -> None:
	'''
	Prints the tree.
	'''
	global nodes_count
	if depth == 0:
		nodes_count = 0
	for key, value in tree.items():
		if isinstance(value, dict):
			print('\t' * depth + key)
			print_tree(value, depth + 1)
		else:
			print('\t' * depth + key)
			nodes_count += 1
	if depth == 0:
		print(f"Nodes: {nodes_count}")


# TODO: this function could be optimized by merging the duplicate states (nodes)
#       and returning when we reach a state we have already explored, however
#       I could not be bothered to do this for a meme project
def get_state_tree(board: np.ndarray, player: int = 1) -> dict[str, dict]:
	'''
	Returns all possible boards after the player makes a move.
	'''
	global visits
	global states
	global stats
	global stats_unique
	global stat_states
	if get_board_string(board) == '000000000':
		visits = 0
		states = {}
		stats = {3: 0, 4: 0, 5: 0}
		stats_unique = {3: 0, 4: 0, 5: 0}
		stat_states = {3: [], 4: [], 5: []}
	visits += 1
	node = {}
	for i in range(3):
		for j in range(3):
			if board[i][j] == 0:
				new_board = board.copy()
				new_board[i][j] = player
				board_string = get_board_string(new_board)
				winner = get_winner(new_board)
				if winner != 0:  # we have a winner
					node[f"{board_string}-{winner+2}"] = board
					stats[winner + 2] += 1
					if f"{board_string}-{winner+2}" not in states:
						stats_unique[winner + 2] += 1
						stat_states[winner + 2].append(board_string)
					states[f"{board_string}-{winner+2}"] = board
				else:
					if is_full(new_board):  # we have a tie
						node[f"{board_string}-5"] = board
						stats[5] += 1
						if f"{board_string}-5" not in states:
							stats_unique[5] += 1
							stat_states[5].append(board_string)
						states[f"{board_string}-5"] = board
						return node
					new_node = get_state_tree(new_board, 1 if player == 2 else 2)
					if player == 1:
						node[f"{board_string}-2"] = new_node
						states[f"{board_string}-2"] = board
					else:
						node[f"{board_string}-1"] = new_node
						states[f"{board_string}-1"] = board
	return node


if __name__ == "__main__":
	# print_board(np.array([[1, 2, 1], [2, 1, 2], [1, 2, 1]]))
	tree = get_state_tree(init_board(), 1)
	tree = {"000000000-1": tree}  # add empty board
	# print_tree(tree)
	print(f"Tree function visits: {visits}")
	print(
	    f"Unique states/boards: {len(states)} ({len(states) + 1} with empty board)"
	)
	print("")
	print("Stats:")
	print("> X wins:", stats[3])
	print("> O wins:", stats[4])
	print("> Ties:", stats[5])
	print("> Unique X wins:", stats_unique[3])
	print("> Unique O wins:", stats_unique[4])
	print("> Unique Ties:", stats_unique[5])
	print("")
	print("Tied boards:")
	print("")
	for i, board in enumerate(stat_states[5]):
		print(f"Tie {i + 1}:")
		print_board(
		    np.array([[int(board[i + j])
		               for j in range(3)]
		              for i in range(0, len(board), 3)]))
		print("")
	print("ALL DONE!")
