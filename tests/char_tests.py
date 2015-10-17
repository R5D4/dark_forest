""" Tests for the char module."""

from nose.tools import *
import char
import items


def get_inventory_test():
    # check if inventory is printed correctly
    player = char.Player()
    desc = {'name': 'Testing Sword'}
    weapon = items.Weapon(desc)
    player.inventory = [weapon]
    ok_(player.get_inventory() == "0: Testing Sword\n")
