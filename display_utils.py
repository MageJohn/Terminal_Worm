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
'''

import constants


def set_up_scr(stdscreen, window):
    '''
Puts a border around window.
Puts a titlebar in stdscreen
    '''

    # Firstly we clear stdscreen and window
    window.clear()
    stdscreen.clear()

    # Secondly we put a border around window
    border(window)

    # Lastly, we add the 'titlebar'
    titlebar = 'Terminal Worm (\'?\' for help)%sScore = 0  '
    titlebar_len = len(titlebar % (''))
    stdscreen.addstr(0, 0,
        titlebar % (' ' * (constants.WINWIDTH - titlebar_len - 1)))


def display_score(score, stdscreen):
    stdscreen.addstr(constants.SCOREPOS[0],
                     constants.SCOREPOS[1],
                     str(int(score)))


def border(window):
    window.border('|', '|', '-', '-', '+', '+', '+', '+')
