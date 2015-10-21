""" Tests for the char module."""

from nose.tools import *
import char
import items


def unequip_test():
    player = char.Player()
    desc = {'name': 'Testing Sword'}
    weapon = items.Weapon(desc)
    player.inventory = []
    player.pick_up(weapon)
    player.equip(weapon)
    ok_(player.unequip('R_hand') == "Unequipped Testing Sword.")
    ok_(player.unequip('R_hand') == "Nothing equipped.")


def get_inventory_test():
    # check if inventory is printed correctly
    player = char.Player()
    desc = {'name': 'Testing Sword'}
    weapon = items.Weapon(desc)
    player.inventory = []
    player.pick_up(weapon)

    # unequipped
    ok_(player.get_inventory() == "0: Testing Sword")

    # equipped
    player.equip(weapon)
    ok_(player.get_inventory() == "0: Testing Sword[E]")


def get_equipped_test():
    # Test if equipped items are output correctly
    player = char.Player()
    item = items.Item()
    player.equip(item)
    print player.get_equipped()
    ok_("R_hand: Unidentified item." in player.get_equipped())


