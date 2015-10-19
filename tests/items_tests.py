"""
Tests for the items module.
"""

from nose.tools import *
import items


def new_weapon_test():
    # Tests if new weapons are created properly.
    weapon = items.new_weapon()
    ok_(weapon is not None)
    

def weapon_test():
    # Tests the creation of a Weapon object
    desc = {
        'name': 'Test Sword',
        'class': '2h_sword',
        'attacks': ['slash'],
        'base': {
                'slash': {'dmg': 1, 'hit': 1}
                },
        'description': "Sword for testing only."
    }
    weapon = items.Weapon(desc)
    ok_(weapon.desc['name'] == 'Test Sword')
