'''
All the constants for the game.
They are:
  - LEFT
  - RIGHT
  - UP
  - DOWN
  - ADJUSTMAP
  - APPLECHR
  - WINWIDTH
  - WINHEIGHT
  - WALLCHR
  - SCOREPOS
  - HEADCHR
  - BODYCHR
  - INITPOS
  - INITLENGTH
  - INITSPEED
'''

# Direction constants
LEFT = 'left'
RIGHT = 'right'
UP = 'up'
DOWN = 'down'

ADJUSTMAP = {
    LEFT:  [ 0, -1],
    RIGHT: [ 0,  1],
    UP:    [-1,  0],
    DOWN:  [ 1,  0]
}

APPLECHR = 'O'

# Game window constants
WINHEIGHT = 20
WINWIDTH = 60

assert WINHEIGHT % 2 == 0 and WINWIDTH % 2 == 0, (
       'Window height and window width need to be even numbers')
# This makes life easier, because then we can do things
# like halve the window size and still end up with whole numbers

WALLCHR = '*'
SCOREPOS = [0, WINWIDTH - 4]

# Snake constants
HEADCHR = '@'
BODYCHR = 'o'
INITPOS = [int(WINHEIGHT / 2), int(WINWIDTH / 2)]
INITLENGTH = 4
assert (INITPOS[1] - INITLENGTH > 0 and
        INITPOS[1] < WINWIDTH and
        INITPOS[0] > 0 and
        INITPOS[0] < WINHEIGHT), ('The snake needs to start in the window! '
        'Remember, the snake is not in the window if '
        'INITPOS - INITLENGTH goes outside the window')

# Intial speed, in seconds
INITSPEED = 0.15

WALL_KILL = False  # Set to True if you want running into walls to mean
                   # Game Over.
