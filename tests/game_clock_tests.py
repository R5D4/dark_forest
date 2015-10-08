"""
Tests for game_clock module.
"""

from nose.tools import *
import game_clock


def init_test():
    clock = game_clock.GameClock()
    ok_(clock.time == 17)


def advance_time_test():
    clock = game_clock.GameClock()
    clock.time = 0 # reset time to something easier to work with
    clock.advance_time('travel')
    ok_(clock.time == 1)
    clock.time = 0 
    clock.advance_time('wait')
    ok_(clock.time == 1)
    clock.time = 0 
    clock.advance_time('rest')
    ok_(clock.time == 3)
    clock.time = 0 
    clock.advance_time('prayer')
    ok_(clock.time == 1)
