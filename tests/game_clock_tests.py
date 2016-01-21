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

def is_day_test():
    # Test if day/night is determined correctly
    clock = game_clock.GameClock()
    # test cases
    clock.time = 6
    ok_(not clock.is_day())
    clock.time = 7
    ok_(clock.is_day())
    clock.time = 8
    ok_(clock.is_day())
    clock.time = 18
    ok_(clock.is_day())
    clock.time = 19
    ok_(clock.is_day())
    clock.time = 20
    ok_(not clock.is_day())


def lifetime_test():
    # Test if lifetime is incremented properly
    clock = game_clock.GameClock()
    ok_(clock.lifetime == 0)
    clock.tick()
    ok_(clock.lifetime == 1)
    clock.tick()
    ok_(clock.lifetime == 2)
