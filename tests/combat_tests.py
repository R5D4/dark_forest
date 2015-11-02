""" 
Tests for combat module.
"""

from nose.tools import *
import combat
import map_
import map_gen


def run_away_test():
    # Test running away!

    # add two adjacent scenes
    a_map = map_.Map('story')
    s1 = map_gen.new_scene(a_map, None, (5, 5))
    s1.name = 'scene1'
    a_map.add_scene(s1)
    s2 = map_gen.new_scene(a_map, None, (6, 5))
    s2.name = 'scene2'
    a_map.add_scene(s2)
    map_gen.create_link(s1, s2)
    # run away from one of the scenes
    name = combat.run_away(s1)
    ok_(name == s2.name)
    name = combat.run_away(s2)
    ok_(name == s1.name)


def attack_create_test():
    # Test creating Attack objects
    wpn_desc = {
               'name': 'Testing Sword',
               'atk_type': 'slash',
               'attribute': 'str',
               'dmg_roll': '1d8',
               }
    attack = combat.Attack(wpn_desc)
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
