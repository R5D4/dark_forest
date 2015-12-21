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
        self.time = START_TIME

    def tick(self):
        """ Advance time by one clock tick."""
        self.time = (self.time + TICK) % 24

