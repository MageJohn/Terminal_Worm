'''
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
    return dialogue(window, ['', 'Really quit?\n(y/n)'])


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
Press 'q' to quit, or 'p'
to play again''' % (int(score), s)

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
