import itertools
import random

import display_utils

SNAKE_ANIM_START = '''\
             .-.  
            /  aa 
            \ -,_)
       _..._| \   
{}   ." .__.' |   
 {} (        /`\  
 {}(`'------'  /  
 |\/;._______.'\  
 ; \           /  
  '-'-.......-'   \
'''

ANIM_ORDER = itertools.cycle(('{}  ', ' {} ', '  {}', ' {} '))

ANIM_SPEED = 400  # In milliseconds


def splash(window):
    '''
Puts an animation in the middle of the passed window,
and waits for a keypress
    '''
    display_utils.border(window)
    snake_lines = SNAKE_ANIM_START.split('\n')
    snake_num_lines = len(snake_lines)

    start_y = int((window.getmaxyx()[0] / 2) - ((snake_num_lines + 5) / 2))
    # The above line helps to ensure that the art is centered.
    # The five added to snake_num_lines is to make space for the name
    # and an instruction on how to start the game

    start_x = 1

    line_length = window.getmaxyx()[1] - 2

    # Now we write the start of the animation to the screen.
    for i, line in enumerate(snake_lines):
        window.addstr(int(start_y + i), start_x, line.center(line_length))

    window.addstr(int(start_y + snake_num_lines) + 2, 1,
        'T E R M I N A L'.center(line_length))

    window.addstr(int(start_y + snake_num_lines) + 3, 1,
        'W O R M'.center(line_length))

    window.addstr(int(start_y + snake_num_lines + 5), 1,
        '(press any key to start)'.center(line_length))

    # The two lines below are chock full of a magic numbers.
    # Here's a little explanation:
    #                     nlines ncols tail y               tail x
    tail_win = window.subwin(2,   4,   start_y + 5,   int(line_length / 2 - 8))
    tongue_win = window.subwin(2,   3,   start_y + 4, int(line_length / 2 + 9))
    # If you want to change the animation, these will have to changed
    # to numbers that fit the your moving parts.
    # The idea is that we create a subwindow over the areas where there are
    # moving parts, and then use that subwindow to display them.

    window.timeout(ANIM_SPEED)

    # The animation
    for frame in ANIM_ORDER:
        tail_win.addstr(0, 0, frame)

        if random.randrange(3) == 0:
            tongue_win.addstr(0, 0, '`-<')
        else:
            tongue_win.addstr(0, 0, '   ')

        tail_win.refresh()
        tongue_win.refresh()

        ch = window.getch()
        if ch != -1:
            del tongue_win
            del tail_win
            window.clear()
            return


def test(stdscr):
    '''This function will be run if we're __main__'''

    window = curses.newwin(24, 80, 0, 0)
    curses.curs_set(0)
    splash(window)

if __name__ == '__main__':
    import curses
    curses.wrapper(test)
