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
    ok_(player.get_inventory() == "0: Testing Sword")


def get_equipped_test():
    # Test if equipped items are output correctly
    player = char.Player()
    item = items.Item()
    player.equipped = {'R_hand': item}
    ok_(player.get_equipped() == "R_hand: Unidentified item.")
