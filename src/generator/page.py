import os
import sys
import numpy as np

# Project imports
sys.path.append(os.getcwd())
from src.generator.tictactoe import init_board, get_state_tree

cache_tree_path = "cache-tree.npy"

page_start = """<!DOCTYPE html>
<html>

<head>
	<title>Tic Tac Toe</title>
	<link rel="stylesheet" type="text/css" href="./../style.css">
	<script src="https://cdn.tailwindcss.com"></script>
</head>

<body>
	<div class="flex absolute top-4 left-4 gap-4">
		<a href="./../index.html" class="flex text-white bg-black rounded-lg p-2 button gap-2 justify-center items-center">
			<svg class="w-6 h-6 text-white" xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24"
				fill="none" stroke="currentColor" stroke-width="2" strokeLinecap="round" strokeLinejoin="round">
				<path d="m3 9 9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z" />
				<polyline points="9 22 9 12 15 12 15 22" />
			</svg>
		</a>
		<a href="https://github.com/RobertBarachini" target=" _blank"
			class="flex text-white bg-black rounded-lg p-2 button gap-2 justify-center items-center">
			<svg class="w-6 h-6 text-white" xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24"
				fill="none" stroke="currentColor" stroke-width="2" strokeLinecap="round" strokeLinejoin="round">
				<path
					d="M15 22v-4a4.8 4.8 0 0 0-1-3.5c3 0 6-2 6-5.5.08-1.25-.27-2.48-1-3.5.28-1.15.28-2.35 0-3.5 0 0-1 0-3 1.5-2.64-.5-5.36-.5-8 0C6 2 5 2 5 2c-.3 1.15-.3 2.35 0 3.5A5.403 5.403 0 0 0 4 9c0 3.5 3 5.5 6 5.5-.39.49-.68 1.05-.85 1.65-.17.6-.22 1.23-.15 1.85v4" />
				<path d="M9 18c-4.51 2-5-2-7-2" />
				<div className="text-white">Robert Barachini</div>
		</a>
	</div>
	<div class="flex items-center justify-center h-screen w-screen">
		<section class="flex flex-col items-center justify-center py-12">
			<h2 class="text-2xl md:text-3xl lg:text-4xl font-bold mb-8">Tic Tac Toe</h2>
			<div class="grid grid-cols-3 gap-4">"""

page_end = """</section>
	</div>
</body>

</html>"""

square = """<div class="flex items-center justify-center border bg-white h-20 w-20 text-white">
					<p class="text-2xl">"""

button = """<a href="000000000-1.html"><div
				class="button inline-flex items-center justify-center font-medium ring-offset-background transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50 hover:bg-primary/90 h-10 mt-8 px-6 py-2 text-xl rounded-lg bg-black text-white">"""


def get_state_difference_index(state1: str, state2: str) -> int:
	'''
	Returns the index of the first difference between the two states.
	'''
	for i, c in enumerate(state1):
		if c != state2[i]:
			return i
	return -1


def generate_page_tree(board_state: str, future_states: list = []):
	'''
	Generates the page for the given state.
	'''
	filepath = os.path.join(*["src", "site", "generated", f"{board_state}.html"])
	if os.path.exists(filepath):
		return
	future_state_indices = {}
	for future_state in future_states:
		future_state_indices[get_state_difference_index(
		    board_state, future_state)] = future_state
	page = page_start
	board, state = board_state.split("-")
	for i, c in enumerate(board):
		square_str = ""
		if c == "1":
			square_str = "X"
		elif c == "2":
			square_str = "O"
		if i in future_state_indices:
			new_state = future_state_indices[i]
			href = f"{new_state}.html"
			page += f"<a class=\"rounded-lg\" href=\"{href}\">"
		square_colored = square
		if c == "1":
			square_colored = square.replace("text-white", "text-red")
		elif c == "2":
			square_colored = square.replace("text-white", "text-blue")
		page += square_colored + square_str + "</p></div>"
		if i in future_state_indices:
			page += "</a>"
	page += "</div>"
	state_string = ""
	if state == "1":
		state_string = "X to play"
	elif state == "2":
		state_string = "O to play"
	elif state == "3":
		state_string = "X wins!"
	elif state == "4":
		state_string = "O wins!"
	elif state == "5":
		state_string = "Tie!"
	page += f"<div class=\"text-2xl mt-4\">{state_string}</div>"
	if state not in ["1", "2"]:
		page += button + "Play again</div></a>"
	page += page_end
	with open(filepath, "w") as f:
		f.write(page)


def traverse_tree(tree: dict):
	'''
	Traverses the tree and generates the pages.
	'''
	for state_key, value in tree.items():
		if not isinstance(value, dict):
			generate_page_tree(state_key)
		else:
			generate_page_tree(state_key, list(value.keys()))
			traverse_tree(value)


def generate_pages_tree():
	'''
	Generates all the pages from a tree.
	'''
	if not os.path.exists(os.path.join(*["src", "site", "generated"])):
		os.mkdir(os.path.join(*["src", "site", "generated"]))
	tree = {}
	if not os.path.exists(cache_tree_path):
		tree = get_state_tree(init_board(), 1)
		tree = {"000000000-1": tree}
		with open(cache_tree_path, "wb") as f:
			np.save(f, tree, allow_pickle=True)  # type: ignore
	else:
		tree = np.load(cache_tree_path, allow_pickle=True).item()
	print("Generating pages from the tree structure...")
	traverse_tree(tree)


if __name__ == "__main__":
	generate_pages_tree()
	print("ALL DONE!")
