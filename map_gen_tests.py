"""
Tests functions is map_gen.py
"""

from random import randint
from random import choice
import map_gen

def empty_adjacent_tests():
    """ Tests the empty_adjacent function."""
    loc = (randint(1, 9), randint(1, 9))
    scenes = {}
    scenes[loc] = "This is a scene."
    print "Location is {}.".format(loc)
    adj_loc = map_gen.empty_adjacent(loc, scenes)
    print "Empty adjacent location is {}.".format(adj_loc)
