'''Terminal Worm: A remake of the classic Snake game
    Copyright (C) 2012, 2013  Yuri Pieters

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.


Functions that help with flow control.
Included in this module are:
  - pause
  - confirm_quit
  - play_again
  - countdown
'''

import curses
import time
from dialogue import dialogue


def pause(window):
    '''
Pauses execution of the game.
Gives the user a message, waits for input, then counts down from 3
window should be a curses window object.
    '''
    dialogue(window, ['P A U S E D', 'press any key'], [{}, ['Start', None]])
    countdown(window)


def confirm_quit(window):
    '''
Asks the user to confirm whether they want to quit.
Returns True if they do, otherwise returns False.
window should be a curses window object.
    '''
    return dialogue(window, ['', 'Really quit?'])


def play_again(score, window):
    '''
Asks the user if they want to play again.
Returns True if they do, else returns False
score is the score of the game, to be displayed to the user,
window should be a curses window object.
    '''
    if score == 1:  # Make sure it's '1 point' and not '1 points'
        s = ''
    else:
        s = 's'

    dialogue_text = '''\
You got %s point%s!
    ''' % (int(score), s)

    while True:
        answer = dialogue(window, ['G A M E  O V E R', dialogue_text],
            [{}, ['Play again', 'playagain'], ['Exit', 'quit']])

        if answer == 'quit':
            if confirm_quit(window):
                return False
        else:
            return True


def countdown(window, start=3):
    '''
Counts down from start. (default 3)
It displays the countdown in the center of the passed curses window.
Pauses execution.
    '''
    countdown_win = curses.newwin(
        1, 2, int(window.getmaxyx()[0] / 2),
        int(window.getmaxyx()[1] / 2))
    for i in range(start, 0, -1):
        countdown_win.addstr(0, 0, str(i), curses.A_BOLD)
        countdown_win.refresh()
        time.sleep(0.5)
    del countdown_win
    window.touchwin()
    window.refresh()
