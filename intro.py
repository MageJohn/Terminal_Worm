import time

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

ANIM_ORDER = (('{}  ', '   '), (' {} ', '   '), ('  {}', '`-<'),
              (' {} ', '   '), ('{}  ', '`-<'), (' {} ', '   '),
              ('  {}', '   '), (' {} ', '`-<'))

ANIM_SPEED = 0.5  # In seconds


def splash(window):
    '''
Puts an animation in the middle of the passed window,
and waits for a keypress
    '''
    window.border(0)
    snake_lines = SNAKE_ANIM_START.split('\n')
    snake_num_lines = len(snake_lines)

    #                                       |    Minus the num lines the  |   Plus how far down in
    #                 Half the window       | splash takes up devided by 2| stdscr the window started
    start_y = int((window.getmaxyx()[0] / 2) - ((snake_num_lines + 4) / 2) + window.getbegyx()[0])
    # The above line helps to ensure that the art is centered.
    # The four added to snake_num_lines is to make space for the name
    # and an instruction on how to start the game
    #                                       |    Minus the num lines the  |   Plus how far down in
    #                 Half the window       | splash takes up devided by 2| stdscr the window started
    start_y = int((window.getmaxyx()[0] / 2) - ((snake_num_lines + 4) / 2) + window.getbegyx()[0])
    # The above line helps to ensure that the art is centered

    start_x = window.getbegyx()[1] + 1

    line_length = window.getmaxyx()[1] - 2

    for i, line in enumerate(snake_lines):
        window.addstr(int(start_y + i), start_x, line.center(line_length))

    window.addstr(int(start_y + snake_num_lines) + 2, 1, 'W O R M Y'.center(line_length))
    window.addstr(int(start_y + snake_num_lines + 4), 1, '(press any key to start)'.center(line_length))

    frame = 0

    # The two lines below are chock full of a magic numbers.
    # Here's a little explanation:
    #                          nlines ncols tail y       tail x
    tail_win   = window.subwin(2,     4,    start_y + 5, int(line_length / 2 - 8))
    tongue_win = window.subwin(2,     3,    start_y + 4, int(line_length / 2 + 9))
    # If you want to change the animation, these will have to changed
    # to numbers that fit the your moving parts.
    # The idea is that we create a subwindow over the areas where there are
    # moving parts, and then use that subwindow to display them.

    window.nodelay(1)

    while True:
        tail_win.addstr(0, 0, ANIM_ORDER[frame][0])
        tongue_win.addstr(0, 0, ANIM_ORDER[frame][1])
        tail_win.refresh()
        tongue_win.refresh()

        if frame == len(ANIM_ORDER) - 1:
            frame = 0
        else:
            frame += 1

        ch = window.getch()
        if ch > -1:
            del tongue_win
            del tail_win
            window.clear()
            return
        time.sleep(ANIM_SPEED)


def test(stdscr):
    '''This function will be run if we're __main__'''

    window = curses.newwin(24, 80, 0, 0)
    splash(window)

if __name__ == '__main__':
    import curses
    curses.wrapper(test)
