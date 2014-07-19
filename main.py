#!/usr/bin/python3.4

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
'''
# Standard library modules
from __future__ import print_function
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
    '''The main function. This is where things happen!'''
    window = curses.newwin(WINHEIGHT, WINWIDTH, 1, 0)

    curses.curs_set(0)  # Invisible cursor
    curses.use_default_colors()

    # With this setting on, python will interpret special
    # keys, such as arrow keys, or the numpad.
    window.keypad(1)

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
            char = window.getch()
            if char == curses.KEY_LEFT or char == ord(CONTROL_KEYS[LEFT]):
                direction = LEFT
            elif char == curses.KEY_RIGHT or char == ord(CONTROL_KEYS[RIGHT]):
                direction = RIGHT
            elif char == curses.KEY_UP or char == ord(CONTROL_KEYS[UP]):
                direction = UP
            elif char == curses.KEY_DOWN or char == ord(CONTROL_KEYS[DOWN]):
                direction = DOWN
            elif char == ord('q'):
                if flow_control.confirm_quit(window):
                    break
            elif char == ord('p'):
                flow_control.pause(window)
            elif char == ord('?'):
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

            window.refresh()
            stdscreen.refresh()

            window.timeout(misc_utils.calc_speed(snake.length))

        if char == ord('q') or not flow_control.play_again(score, window):
            break

curses.wrapper(main)

# curses.wrapper cleans up for us, so all that's left to do is:
print('See you soon!')
