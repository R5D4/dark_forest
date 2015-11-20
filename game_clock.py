""" 
This module provides time functions.
"""

TICK = 1 # one tick = 1 hour
START_TIME = 17 # Default start time (5pm)
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

    def tick(self):
        """ Advance time by one clock tick."""
        self.time = (self.time + TICK) % 24

    def time_period(self):
        """ Return time period keyword."""
        return TIME_PERIOD[self.time]
