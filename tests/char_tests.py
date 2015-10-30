""" Tests for the char module."""

from nose.tools import *
import char
import items


def update_stats_test():
    player = char.Player()
    pass

def unequip_test():
    player = char.Player()
    wpn_desc = {
               'name': 'Testing Sword',
               'class': '1h_sword',
               'atk_type': 'slash',
               'attribute': 'str',
               'require': {'str': 0, 'dex': 0},
               'bonus': {'str': 0, 'dex': 0},
               'dmg_roll': '1d8',
               'description': "For testing only!"
               }
    weapon = items.Weapon(wpn_desc)
    player.inventory = []
    player.pick_up(weapon)
    player.equip(weapon)
    ok_(player.unequip('R_hand') == "Unequipped Testing Sword.")
    ok_(player.unequip('R_hand') == "Nothing equipped.")


def get_inventory_test():
    # check if inventory is printed correctly
    player = char.Player()
    wpn_desc = {
               'name': 'Testing Sword',
               'class': '1h_sword',
               'atk_type': 'slash',
               'attribute': 'str',
               'require': {'str': 0, 'dex': 0},
               'bonus': {'str': 0, 'dex': 0},
               'dmg_roll': '1d8',
               'description': "For testing only!"
               }
    weapon = items.Weapon(wpn_desc)
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
    wpn_desc = {
               'name': 'Testing Sword',
               'class': '1h_sword',
               'atk_type': 'slash',
               'attribute': 'str',
               'require': {'str': 0, 'dex': 0},
               'bonus': {'str': 0, 'dex': 0},
               'dmg_roll': '1d8',
               'description': "For testing only!"
               }
    weapon = items.Weapon(wpn_desc)
    player.equip(weapon)
    print player.get_equipped()
    ok_("R_hand: Testing Sword" in player.get_equipped())


