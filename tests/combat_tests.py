""" 
Tests for combat module.
"""

from nose.tools import *
import combat
import char
import map_
import map_gen
from tests.test_data import *


def run_away_test():
    # Test player running away!

    # create map and characters
    a_map = map_.Map('story')
    player = char.Player()
    boar = char.Boar()
    a_map.characters['player'] = player
    a_map.characters['boar'] = boar
    # add two adjacent scenes
    s1 = map_gen.new_scene(a_map, None, (5, 5))
    s1.name = 'scene1'
    a_map.add_scene(s1)
    s2 = map_gen.new_scene(a_map, None, (6, 5))
    s2.name = 'scene2'
    a_map.add_scene(s2)
    map_gen.create_link(s1, s2)
    # spawn the boss in one of the scenes
    map_gen.add_lair(a_map)
    map_gen.spawn_boss(a_map)
    # run away from one of the scenes
    name = combat.run_away(s1)
    ok_(name == s2.name)
    name = combat.run_away(s2)
    ok_(name == s1.name)


def attack_create_test():
    # Test creating Attack objects
    attack = combat.Attack(TESTING_SWORD)
    ok_(attack.wpn_name == 'Testing Sword')
    ok_(attack.attribute == 'str')
    ok_(attack.dmg_roll == '1d8')
    messages = {
               'prep_msg': "The %s slashes the %s with the %s!",
               'hit_crit_msg': "The slash opens up a gushing wound!",
               'hit_success_msg': "The slash cuts through the defences!",
               'hit_fail_msg': "The slash misses!",
               }
    print attack.messages
    print messages
    ok_(attack.messages == messages)
