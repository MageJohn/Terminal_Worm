'''Terminal Worm: A remake of the classic Snake game
    Copyright (C) 2012, 2013  Yuri Pieters

    Terminal Worm is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    Terminal Worm is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.


Various miscellaneous functions.
They are:
  - get_char
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

def get_char(window):
    '''Gets a char out of the queue,
       and then empties it. This stops the
       queue getting filled with spam if you
       hold down a button.
    '''
    char = window.getch()
    rest = None
    while rest != -1:
        rest = window.getch()

    return char


def calc_speed(length):
    return (INITSPEED - length * 2) / 1000


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
