import curses


def dialog(window, text, answer_map=None, border=0):
    '''
Show's a dialog box to the user, and then returns True or False
The answer map is a dictionary,
where the keys are the menu options for the user.

and the values are what is returned when a given option is chosen.
The keys should be one letter strings,
but the values can be whatever you can put in a dictionary.

For example, in the default mapping ({'y':True, 'n':False}),
if the user presses 'y' True is returned

None is a wildcard. If None is used as a key,
then any free key will return the value.

The text passed should inform the user what options he has,
and it can be a multiline string.
If it is, then each line will be centered
    '''

    if answer_map is None:
        answer_map = {'y': True, 'n': False}
    text = text.split('\n')

    win_height, win_width = window.getmaxyx()
    win_start_y, win_start_x = window.getbegyx()

    width = int((win_width * 70) / 100)  # 70% of the window
    height = len(text) + 2  # 1 line of padding around the text.
    start_y = int(((win_height - height) / 2) + win_start_y)
    start_x = int(((win_width - width) / 2) + win_start_x)

    dialog = curses.newwin(height, width, start_y, start_x)
    dialog.border(*([border] * 8))

    for i, s in enumerate(text, 1):
        dialog.addstr(i, 1, s.center(width - 2))
    dialog.refresh()

    safe_map = answer_map.copy()
    for key in answer_map.keys():
        if key is None:
            del(safe_map[None])
    ord_keys = [ord(key) for key in safe_map.keys()]
    window.nodelay(0)
    c = -1
    while c not in ord_keys:
        # chr(c) will throw up an exception if the number isn't valid,
        # so were checking c against a list of the keys in ord() form
        c = dialog.getch()
        if None in answer_map.keys() and c not in ord_keys:
            answer_map[chr(c)] = answer_map[None]
            ord_keys.append(c)
    window.nodelay(1)

    del dialog
    window.touchwin()
    window.refresh()
    return answer_map[chr(c)]
