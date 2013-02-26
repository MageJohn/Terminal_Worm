'''
Various miscellaneous functions.
They are:
  - calc_speed
  - timer
  - help
'''
# Standard library modules
import random

# Custom modules
import flow_control
from constants import INITSPEED, CONTROL_KEYS
from constants import UP, DOWN, LEFT, RIGHT
from dialogue import dialogue


def calc_speed(length):
    return int(INITSPEED - (length / 5 + length) / 10 % 120)


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

                """ % (CONTROL_KEYS[UP], CONTROL_KEYS[LEFT],
                       CONTROL_KEYS[RIGHT], CONTROL_KEYS[DOWN])

    gameplay_help = """
Gameplay

Run around and eat the apples.
As you eat, you'll grow longer,
but be careful! Running into yourself,
or going backwards means Game Over.

The higher your score, the faster
you'll go.

Every now and again though.
you'll get a bonus...

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

"""

    dialogue(window, ['Help', command_help], [{}, ['--Press Space--', None]])
    dialogue(window, ['Help', gameplay_help], [{}, ['--Press Space--', None]])
    dialogue(window, ['Help', bug_help], [{}, ['--Press Space--', None]])
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
