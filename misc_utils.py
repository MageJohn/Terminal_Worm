'''
Various miscellaneous functions.
They are:
  - calc_speed
  - timer
  - dialogue
  - help
'''
# Standard library modules
import time
import curses
import random

# Custom modules
import flow_control
from constants import INITSPEED, CONTROL_KEYS
from constants import UP, DOWN, LEFT, RIGHT


def calc_speed(length):
    return int(INITSPEED - (length / 5 + length) / 10 % 120)


def timer():
    start_time = time.time()
    yield 0
    while True:
        time_elapsed = time.time() - start_time
        start_time = time.time()
        yield time_elapsed * 1000


def dialogue(window, text, answer_map=None, border=0):
    '''
Shows a dialogue box to the user, and then returns True or False
The answer map is a dictionary,
where the keys are the menu options for the user,
and the values are what is returned when a given option is chosen.
The keys should be one letter strings,
but the values can be whatever you can put in a dictionary.

For example, in the default mapping ({'y':True, 'n':False}),
if the user presses 'y' True is returned

None is a wild-card. If None is used as a key,
then any keypress not already bound will return the value.

The text passed should be a list or tuple, where text[0] is the title
of the dialogue box, and text[1] is the body text.
You should inform the user what options he has, as this module won't.

    '''

    if answer_map is None:
        answer_map = {'y': True, 'n': False}

    body_text = text[1].split('\n')

    #--------------------
    # Now for initial variable setup

    win_height, win_width = window.getmaxyx()
    win_start_y, win_start_x = window.getbegyx()

    width = int((win_width * 70) / 100)  # 70% of the window
    height = len(body_text) + 2  # 1 line of padding around the text.

    start_y = int(((win_height - height) / 2) + win_start_y)
    start_x = int(((win_width  - width)  / 2) + win_start_x)

    #-----------------
    # That done, now we do the setup the dialogue box.

    dialogue = curses.newwin(height, width, start_y, start_x)
    dialogue.border('|', '|', '-', '-', '+', '+', '+', '+')
    # I have a custom function that does this for me, but I want this function
    # to be particularly self-sufficient.

    dialogue_title = text[0].center(width - 2, '-')
    dialogue.addstr(0, 0, ''.join(['+', dialogue_title, '+']),
        curses.A_REVERSE | curses.A_BOLD)

    for i, s in enumerate(body_text, 1):
        dialogue.addstr(i, 1, s.center(width - 2))

    dialogue.refresh()

    #---------------------------
    # Display of the dialog box dealt with, time for the input.
    safe_map = answer_map.copy()

    for key in answer_map.keys():
        # The ord_keys variable, defined below, will choke on a value of None,
        # so we're making a copy of the map without None.
        if key is None:
            del(safe_map[None])
    ord_keys = [ord(key) for key in safe_map.keys()]
    window.nodelay(0)
    c = -1
    while c not in ord_keys:
        # chr(c) will throw up an exception if the number isn't valid,
        # so were checking c against a list of the keys in ord() form
        c = dialogue.getch()
        if None in answer_map.keys() and c not in ord_keys:
            answer_map[chr(c)] = answer_map[None]
            ord_keys.append(c)
    window.nodelay(1)

    #------------------------
    # Cleanup and return

    del dialogue
    window.touchwin()
    window.refresh()
    return answer_map[chr(c)]


def help(window):
    command_help = """
Commands

      %s           
Use %s + %s  or the
      %s           
arrow keys for movement

'p': Pause

'q': Quit

'?': This help text

--Press space--
                """ % (CONTROL_KEYS[UP], CONTROL_KEYS[LEFT],
                       CONTROL_KEYS[RIGHT], CONTROL_KEYS[DOWN])

    gameplay_help_1 = """
Gameplay

Run around and eat the apples.
As you eat, you'll grow longer,
but be careful! Running into yourself,
or going backwards means Game Over.

The higher your score, the faster
you'll go.

Every now and again though.
you'll get a bonus...

--Press space--
    """

    bug_help = """
Bugs

Bugs are a delicious treat,
for which you'll get extra points!
If you see one, try and get to it
as quickly as possible.
There's a counter, and if it
reaches 0, the bug runs away.
But if you do catch it, then
the rest of the timer
will be added to your score!

That's it. I hope you have fun!

--Press space--
"""

    dialogue(window, ['Help', command_help], {' ': None})
    dialogue(window, ['Help', gameplay_help_1], {' ': None})
    dialogue(window, ['Help', bug_help], {' ': None})
    flow_control.countdown(window)


def get_random_pos(win, exclude_list=(None,)):
    '''
Returns a random position in win, that is not in exclude_list
    '''
    while True:
        random_pos = [random.randrange(1, win.getmaxyx()[0] - 1),
                    random.randrange(1, win.getmaxyx()[1] - 1)]
        if random_pos in exclude_list:
            continue
        else:
            break
    return random_pos
