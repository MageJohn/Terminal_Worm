'''
The game classes
They are:
  - the snake class
  - the apple class
'''

import constants
import misc_utils


class Snake:
    '''
This is the class for the snake
It's methods are:
  - new_snake_struct (called by __init__)
  - move
  - extend
  - update
  - collide_detect
    '''

    def __init__(self, head_pos, length):
        self.length = length
        self.new_snake_struct(head_pos, length)

    def new_snake_struct(self, head_pos, length):
        '''
Sets self.pos_list to a new snake data structure
Used by __init__
        '''
        self.pos_list = [[head_pos[0], (head_pos[1] - (i + 1))]
                          for i in range(length - 1)]
        self.pos_list.insert(0, head_pos)

    def move(self, d):
        '''
Move the snake (does not update the screen)
The algorithm used is:

Move head in direction d

The position of the old head becomes a body part

Delete the old tail
        '''
        self.old_pos = self.pos_list[:]
        # The update method of the snake needs a record of the last snake.

        head_adjust = constants.ADJUSTMAP[d]

        new_head = [pos + adjust
                    for pos, adjust in zip(self.pos_list[0], head_adjust)]

        if not constants.WALL_KILL:
            if new_head[0] == constants.WINHEIGHT - 1:
                new_head[0] = 1

            elif new_head[0] == 0:
                new_head[0] = constants.WINHEIGHT - 2

            elif new_head[1] == constants.WINWIDTH - 1:
                new_head[1] = 1

            elif new_head[1] == 0:
                new_head[1] = constants.WINWIDTH - 2

        self.pos_list.insert(0, new_head)
        del self.pos_list[-1]

    def extend(self):
        '''
Add a new snake element to the tail

Algorithm used is:

if the last part is above the second-last, the new part goes above the last

if the last part is below the second-last, the new part goes below the last

Etc.
        '''

        ultimate = self.pos_list[-1]
        penultimate = self.pos_list[-2]

        if ultimate[0] < penultimate[0]:
            # The last section is above the second last
            new_part = [ultimate[0] - 1, ultimate[1]]
        elif ultimate[0] > penultimate[0]:
            # The last section is below the second last
            new_part = [ultimate[0] + 1, ultimate[1]]
        elif ultimate[1] < penultimate[1]:
            # The last section is to the left of the second last
            new_part = [ultimate[0], ultimate[1] - 1]
        elif ultimate[1] > penultimate[1]:
            # The last section is to the right of the second last
            new_part = [ultimate[0], ultimate[1] + 1]

        self.pos_list.append(new_part)

        self.length += 1

    def update(self, window, full_write=False):
        '''
Write the snake to the screen
If full_write is True, it will write the full snake structure to the
screen. Otherwise it will write only the changes made by the move method.
        '''

        if not full_write:
            # We'll start by dealing with old tails.
            # If the snake has been extended,
            # then we leave the part on the screen, otherwise,
            # we overwite with a space

            if self.length == len(self.old_pos):
                y, x = self.old_pos[-1]
                # self.old_pos[-1] is the position of the tail
                # before the move method was called
                window.addstr(y, x, ' ')

            # Now we overwrite the old head with a body part (an 'o')
            y, x = self.old_pos[0]
            # self.old_pos[0] is the position of the
            # head before the move method was called

            window.addstr(y, x, constants.BODYCHR)

            # Lastly, we write the new head to the screen
            y, x = self.pos_list[0]
            # The position of the current head
            window.addstr(y, x, constants.HEADCHR)
        else:
            window.addstr(
                self.pos_list[0][0],
                self.pos_list[0][1],
                constants.HEADCHR)
            for i in self.pos_list[1:]:
                window.addstr(i[0], i[1], constants.BODYCHR)

    def collide_detect(self, window):
        '''
Returns True if the snake has collided with itself or a wall,
else returns False
        '''

        if self.pos_list[0] in self.pos_list[1:]:
            return True

        if constants.WALL_KILL:
            if (self.pos_list[0][0] == 0 or
                    self.pos_list[0][0] == constants.WINHEIGHT or
                    self.pos_list[0][1] == 0 or
                    self.pos_list[0][1] == constants.WINWIDTH):
                return True

        if window.inch(
                self.pos_list[0][0],
                self.pos_list[0][1]) == ord(constants.WALLCHR):
            return True

        return False


class Apple:
    '''This is the class for the apple.
    It's methods are:
      - update
      - new_pos (used by __init__)

A snake structure is needed, so that the new_pos function can check
for any overlap between the snake and the apple.
    '''
    def __init__(self, snake, window):
            pos_exclude_list = snake.pos_list
            self.pos = misc_utils.get_random_pos(window, pos_exclude_list)

    def update(self, window):
        '''
Writes the apple to the screen
        '''
        window.addstr(self.pos[0], self.pos[1], constants.APPLECHR)
