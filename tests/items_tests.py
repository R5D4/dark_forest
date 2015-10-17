"""
Tests for the items module.
"""

from nose.tools import *
import items

def new_weapon_test():
    # Tests if new weapons are created properly.
    weapon = items.new_weapon()
    ok_(weapon is not None)
    

