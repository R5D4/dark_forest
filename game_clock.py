""" 
This module provides time functions.
"""

TICK = 1 # one tick = 1 hour
START_TIME = 17 # Default start time (5pm)


class GameClock(object):
    """
    A clock to keep track of time in the game.

    Has methods to advance time and defines time periods.
    """

    def __init__(self):
        self.time = START_TIME # 24-hr clock (values: 0-23)
        self.lifetime = 0 # total number of elapsed clock ticks

    def tick(self):
        """ Advance time by one clock tick."""
        self.lifetime += 1
        self.time = (self.time + TICK) % 24

    def is_day(self):
        """ Return True if it's daytime, else False."""
        if self.time >= 7 and self.time <= 19: # 0700 to 1900 inclusive
            return True
        else:
            return False

