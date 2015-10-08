""" 
This module provides time functions.
"""

START_TIME = 17 # Default start time (5pm)
ACTION_DURATION = {
                  'travel': 1,
                  'wait': 1,
                  'rest': 3,
                  'pray': 1
                  }


class GameClock(object):
    """
    A clock to keep track of time in the game.

    Has methods to advance time and defines time periods.
    """

    def __init__(self):
        self.time = START_TIME

    def advance_time(self, action):
        """ Advance time by the duration of the action."""
        self.time = (self.time + ACTION_DURATION[action]) % 24

        
