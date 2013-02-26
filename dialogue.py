import curses


class Menu:
    """This is a class for making a simple list menu.
It tracks what is currently selected, and provides
methods for changing the the current item, returning the current item,
and returning a list of all items.

Items are _MenuItem instances.

"""
    def __init__(self):
        self._menu_items = []
        self._current_item = 0
        self.has_changed = True

    def add_item(self, text, value):
        """Adds a new _MenuItem instance to the menu."""
        self._menu_items.append((text, value))

    def go_next(self):
        """Move down in the item list."""
        if not self._current_item == len(self._menu_items) - 1:
            self._current_item += 1
            self.has_changed = True

    def go_prev(self):
        """Move up in the item list."""
        if not self._current_item == 0:
            self._current_item -= 1
            self.has_changed = True

    def get_current(self):
        """Returns a tuple of the current menu item
and of it's position in the list.

"""
        return self._menu_items[self._current_item]

    def get_all(self):
        """Returns a list of all the items in the menu"""
        return self._menu_items[:]

    def write(self, window, y_pos, line_length):
        if self.has_changed:
            for i, item in enumerate(self._menu_items):
                if i == self._current_item:
                    window.addstr(
                        y_pos + i,
                        int(
                            (len(item[0].center(line_length)) -
                             len(item[0])) / 2),
                        item[0], curses.A_REVERSE)
                else:
                    window.addstr(
                        y_pos + i,
                        int(
                            (len(item[0].center(line_length)) -
                             len(item[0])) / 2),
                        item[0])


def dialogue(window, text, answer_map=None):
    '''
Shows a dialogue box to the user.
The answer map is a list, with the first item a dictionary.
This dictionary should have the keys as the hotkeys,
(it can take ascii values, or curses provided key constants) and the values
should be what you expect to be returned.

The rest of the list should be sub-lists, where item [0] is the text to be
displayed, and item [1] is what you expect to be returnedd

The default mapping is this:
[{}, ['Yes', True], ['No', False]]
It has no hotkeys, and two options

The use of None as a wildcard isn't supported anymore.

The text argument should be a list or tuple, where text[0] is the title
of the dialogue box, and text[1] is the body text.

Currently having only hotkeys, and no menu items, isn't supported.

    '''

    if answer_map is None:
        answer_map = [{}, ['Yes', True], ['No', False]]

    body_text = text[1].split('\n')

    #--------------------
    # Now for initial variable setup

    win_height, win_width = window.getmaxyx()
    win_start_y, win_start_x = window.getbegyx()

    width = int((win_width * 70) / 100)  # 70% of the window
    height = len(body_text) + len(answer_map) + 5  # 1 line of padding
                                                   # around the text.

    start_y = int(((win_height - height) / 2) + win_start_y)
    start_x = int(((win_width - width) / 2) + win_start_x)

    #--------------------
    # Now we set up the menu object

    menu = Menu()
    for item in answer_map[1:]:
        menu.add_item(item[0], item[1])

    #-----------------
    # That done, now we do the setup the dialogue box.

    dialogue = curses.newwin(height, width, start_y, start_x)
    dialogue.border('|', '|', '-', '-', '+', '+', '+', '+')
    # I have a custom function that does this for me, but I want this function
    # to be particularly self-sufficient.

    dialogue_title = text[0].center(width - 2, '-')
    dialogue.addstr(0, 0, ''.join(['+', dialogue_title, '+']),
        curses.A_REVERSE | curses.A_BOLD)

    for i, s in enumerate(body_text, 2):
        dialogue.addstr(i, 1, s.center(width - 2))

    menu_y = len(body_text) + 3
    menu.write(dialogue, menu_y, width - 2)

    dialogue.refresh()

    #---------------------------
    # Display of the dialog box dealt with, time for the input.

    window.nodelay(0)
    dialogue.keypad(1)
    end = False
    while True:
        c = dialogue.getch()
        if c == curses.KEY_UP:
            menu.go_prev()
        if c == curses.KEY_DOWN:
            menu.go_next()
        if c == ord(' ') or c == curses.KEY_ENTER or c == curses.KEY_SELECT:
            selection = menu.get_current()
            break
        else:
            menu.has_changed == False

        for key in answer_map[0].keys():
            if c == key or c == ord(key):
                selection = (key, answer_map[0][key])
                end = True
        if end:
            break

        menu.write(dialogue, menu_y, width - 2)
        dialogue.refresh()
    window.nodelay(1)

    #------------------------
    # Cleanup and return

    del dialogue
    window.touchwin()
    window.refresh()
    return selection[1]


def test(stdscr):
    win = curses.newwin(24, 80, 0, 0)
    return dialogue(win, ['Test', 'This is a test\nSelect Yes or No.'],
                    [{'q': None}, ['Yes', True], ['No', False]])

if __name__ == '__main__':
    answer = curses.wrapper(test)
    if answer == True:
        print('You replied Yes')
    elif answer == False:
        print('You replied No')
    elif answer == None:
        print('You exited')
