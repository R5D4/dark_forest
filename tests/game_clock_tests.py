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

def time_period_test():
    clock = game_clock.GameClock()
    # 0:00
    clock.time = 0
    ok_(clock.time_period() == 'midnight')
    # 1:00 - 5:00
    for clock.time in range(1, 6):
        ok_(clock.time_period() == 'night2')
    # 6:00
    clock.time = 6
    ok_(clock.time_period() == 'sunrise')
    # 7:00
    clock.time = 7
    ok_(clock.time_period() == 'dawn')
    # 8:00 - 11:00
    for clock.time in range(8, 12):
        ok_(clock.time_period() == 'morning')
    # 12:00
    clock.time = 12
    ok_(clock.time_period() == 'noon')
    # 13:00 - 18:00
    for clock.time in range(13, 19):
        ok_(clock.time_period() == 'afternoon')
    # 19:00
    clock.time = 19
    ok_(clock.time_period() == 'dusk')
    # 20:00
    clock.time = 20
    ok_(clock.time_period() == 'sundown')
    # 21:00 - 23:00
    for clock.time in range(21, 24):
        ok_(clock.time_period() == 'night1')

