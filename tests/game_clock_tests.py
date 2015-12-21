"""
Tests for game_clock module.
"""

from nose.tools import *
import game_clock


def init_test():
    clock = game_clock.GameClock()
    ok_(clock.time == 17)


def tick_test():
    clock = game_clock.GameClock()
    clock.time = 0 # reset time to something easier to work with
    clock.tick()
    ok_(clock.time == 1)
    clock.tick()
    ok_(clock.time == 2)
    clock.time = 23
    clock.tick()
    ok_(clock.time == 0)

