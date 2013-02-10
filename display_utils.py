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


def border(window, border_chr=0):
    window.border(*([border_chr] * 8))
