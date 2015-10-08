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
TIME_PERIOD = [ 'midnight', # 0
                'night2', 'night2', 'night2', 'night2', 'night2', # 1-5
                'sunrise', # 6
                'dawn', # 7
                'morning', 'morning', 'morning', 'morning', # 8-11
                'noon', # 12
                'afternoon', 'afternoon', 'afternoon', 'afternoon', 
                'afternoon', 'afternoon', # 13-18
                'dusk', # 19
                'sundown', #20
                'night1', 'night1', 'night1' # 21-23
                ]

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

    def time_period(self):
        """ Return time period keyword."""
        return TIME_PERIOD[self.time]
