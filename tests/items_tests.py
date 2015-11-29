"""
Tests for the items module.
"""

from nose.tools import *
import items
from tests.test_data import *


def armor_test():
    # Tests the creation of an Armor object
    armor = items.Armor(TESTING_SHIELD)
    ok_(armor.desc == TESTING_SHIELD)


def get_armor_test():
    # Tests if armor can be created by indicating armor name
    armor = items.get_armor('Knight Shield')
    ok_(armor.desc['name'] == 'Knight Shield')


def new_armor_test():
    # Tests if new armors are created properly.
    armor = items.new_armor()
    ok_(armor is not None)


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
    weapon = items.Weapon(TESTING_SWORD)
    ok_(weapon.desc == TESTING_SWORD)
