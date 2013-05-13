# Standard library modules
import curses

# Custom modules
import flow_control
import display_utils
import misc_utils
import classes
import intro
from constants import WINHEIGHT, WINWIDTH, INITPOS, INITLENGTH, INITSPEED
from constants import RIGHT, LEFT, UP, DOWN, CONTROL_KEYS

# NB: In curses, positions are 'y,x', instead of 'x,y'


def main(stdscreen):
    window = curses.newwin(WINHEIGHT, WINWIDTH, 1, 0)

    curses.curs_set(0)  # Invisible cursor
    curses.use_default_colors()
    window.keypad(1)  # With this setting on, python will interpret special
                      # keys, such as arrow keys, or the numpad.

    intro.splash(window)
    while True:
        # The setup for a new game
        snake = classes.Snake(INITPOS, INITLENGTH)
        bug = None
        apple = classes.Apple(snake, bug, window)
        score = 0
        direction = RIGHT
        no_new_bug = False

        display_utils.set_up_scr(stdscreen, window)
        snake.update(window, True)
        apple.update(window)

        window.timeout(INITSPEED)

        stdscreen.refresh()
        window.refresh()

        while True:  # The game loop
            # Event handling
            ch = window.getch()
            if ch == curses.KEY_LEFT or ch == ord(CONTROL_KEYS[LEFT]):
                direction = LEFT
            elif ch == curses.KEY_RIGHT or ch == ord(CONTROL_KEYS[RIGHT]):
                direction = RIGHT
            elif ch == curses.KEY_UP or ch == ord(CONTROL_KEYS[UP]):
                direction = UP
            elif ch == curses.KEY_DOWN or ch == ord(CONTROL_KEYS[DOWN]):
                direction = DOWN
            elif ch == ord('q'):
                if flow_control.confirm_quit(window):
                    break
            elif ch == ord('p'):
                flow_control.pause(window)
            elif ch == ord('?'):
                misc_utils.help(window)

            snake.move(direction)

            if snake.collide_detect(window):
                break

            snake.update(window)

            if snake.pos_list[0] == apple.pos:
                snake.extend()
                apple = classes.Apple(snake, bug, window)
                apple.update(window)
                score += 1
                no_new_bug = False
                display_utils.display_score(score, stdscreen)

            # Start bug code :-)
            # ====================

            if bug is not None:
                bug.timeout -= 1
                if bug.timeout < 0:
                    bug.remove(window, stdscreen)
                    bug = None
                    no_new_bug = True
                else:
                    bug.display_timer(stdscreen)

            if bug is not None:
                # We check two separate times if bug is not None,
                # because the first time has the possibility of
                # changing bugs value.
                if snake.pos_list[0] == bug.pos:
                    snake.extend()
                    score += bug.timeout
                    no_new_bug = False
                    display_utils.display_score(score, stdscreen)
                    bug.remove(window, stdscreen, True)
                    bug = None

            if (not no_new_bug and
                    snake.length > INITLENGTH + 1 and
                    snake.length % 5 == 0 and bug is None):
                bug = classes.Bug(window, stdscreen, snake, apple)
                bug.write(window)
                bug.display_timer(stdscreen)

            # ====================
            # End bug code

            # There's a bug that means a section of the border can be
            # overwritten. This is a quick fix:
            display_utils.border(window)
            # TODO: See if there might be a more efficient method,
            #       hopefully prevent the overwrite from happening at all.

            window.refresh()
            stdscreen.refresh()

            window.timeout(misc_utils.calc_speed(snake.length))

        if ch == ord('q') or not flow_control.play_again(score, window):
            break

curses.wrapper(main)

# curses.wrapper cleans up for us, so all that's left to do is:
print('See you soon!')
