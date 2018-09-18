#!/usr/bin/python
import logging, utils, curses

class CursesHandler(logging.Handler):
    """
    Creates a curses object to interface with a terminal output.
    """

    def __init__(self, screen):
        """Constructor for the CursesHandler calssself.

        Keyword arguments:
        self --  The caller, the new CursesHandler
        screen -- presumably where the graphics will be displayed

        Side effects:
        - Sets instance variables
        - Sets the color for curses
        """
        logging.Handler.__init__(self)
        self.screen = screen

        curses.start_color()
        curses.use_default_colors()
        for i in range(0, curses.COLORS):
            curses.init_pair(i + 1, i, -1)

    def emit(self, record):
        """
        This method tries to esablish a connection with the screen and refresh

        Keyword arguments:
        self -- The caller
        record -- The location that handles the Error

        Side effects:
        -Creates a screen object and sets it up
        """
        try:
            screen = self.screen
            screen.addstr(u'\n%s' % self.format(record), self.get_color_pair(record.levelno))
            screen.refresh()
        except (KeyboardInterrupt, SystemExit):
            raise
        except:
            self.handleError(record)

    def get_color_pair(self, level):
        """
        Returns a color pair based on a level.

        Keyword arguments:
        self -- The caller
        level -- the index of the color in the array
        """
        index = str(level)
        return curses.color_pair({
            '10': 83,
            '20': 39,
            '30': 245,
            '40': 167,
            '50': 197
        }[index])
