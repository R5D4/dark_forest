""" 
Tests for combat module.
"""

from nose.tools import *
import combat

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
               'hit_success_msg': "The slash cuts through!",
               'hit_fail_msg': "The slash misses!",
               }
    ok_(attack.messages == messages)
