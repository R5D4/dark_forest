"""
Tests for the items module.
"""

from nose.tools import *
import items


def get_weapon_test():
    # Tests if weapon can be created by indicating weapon name
    weapon = items.get_weapon('Hunting Knife')
    ok_(weapon.desc['name'] == 'Hunting Knife')

    
def boss_weapon_test():
    # Tests if new weapons are created properly.
    weapon = items.boss_weapon()
    ok_(weapon is not None)


def new_weapon_test():
    # Tests if new weapons are created properly.
    weapon = items.new_weapon()
    ok_(weapon is not None)
    

def weapon_test():
    # Tests the creation of a Weapon object
    wpn_desc = {
               'name': 'Testing Sword',
               'atk_type': 'slash',
               'attribute': 'str',
               'dmg_roll': '1d8',
               'description': "Sword for testing only."
               }
    weapon = items.Weapon(wpn_desc)
    ok_(weapon.desc == wpn_desc)
