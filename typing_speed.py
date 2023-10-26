import curses
from curses import wrapper
import time
import random

# function to display the welcome screen
def start_screen(stdscr):
	stdscr.clear()
	stdscr.addstr("Welcome to the Speed Typing Test!")
	stdscr.addstr("\nPress any key to begin!")
	stdscr.refresh()
	stdscr.getkey()

# display target text and current input of user function
def display_text(stdscr, target, current, wpm=0):
	stdscr.addstr(target)                         # display the target text
	stdscr.addstr(1, 0, f"WPM: {wpm}")            # display WPM

	for i, char in enumerate(current):
		correct_char = target[i]
		color = curses.color_pair(1)             # initialize with green color (correct input)
		if char != correct_char:
			color = curses.color_pair(2)           # red color means incorrect input

		stdscr.addstr(0, i, char, color)            # display curent input of user

# function to take a random line from a text file
def load_text():
	with open("text.txt", "r") as f:
		lines = f.readlines()
		return random.choice(lines).strip()

# function to measure the spped typing test
def wpm_test(stdscr):
	target_text = load_text()               # get random line of text
	current_text = []                       # current input of user
	wpm = 0
	start_time = time.time()                # record the start time
	stdscr.nodelay(True)                    # enable non blocking input

	while True:
		time_elapsed = max(time.time() - start_time, 1)
		wpm = round((len(current_text) / (time_elapsed / 60)) / 5)            # cal. WPM

		stdscr.clear()
		display_text(stdscr, target_text, current_text, wpm)                  # display the text and current input
		stdscr.refresh()

		if "".join(current_text) == target_text:                              # check if the input mathches the target
			stdscr.nodelay(False)
			break

		try:
			key = stdscr.getkey()
		except:
			continue

		if ord(key) == 27:                                                    # acci no of ESC key to exit the code
			break

		if key in ("KEY_BACKSPACE", '\b', "\x7f"):                             # check for backspace key
			if len(current_text) > 0:
				current_text.pop()
		elif len(current_text) < len(target_text):
			current_text.append(key)                                           # append the input to the current text

# main function

def main(stdscr):
	curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
	curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
	curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_BLACK)

	start_screen(stdscr)
	while True:
		wpm_test(stdscr)     # start the typing test
		stdscr.addstr(2, 0, "You completed the text! Press any key to continue...")
		key = stdscr.getkey()
		
		if ord(key) == 27:
			break

wrapper(main)