""" Tests for the char module."""

from nose.tools import *
import char
import items


def sleep_test():
    # Test if sleep recovers the appropriate amount of HP
    player = char.Player()
    player.effective_stats['max_HP'] = 100
    # rest should recover 8 HP
    player.health['HP'] = 0
    print player.sleep()
    ok_(player.health['HP'] == 8)
    # sleep should recover 1 HP (max_HP limit)
    player.health['HP'] = 99
    print player.sleep()
    ok_(player.health['HP'] == 100)


def rest_test():
    # Test if resting recovers the appropriate amount of HP
    player = char.Player()
    player.effective_stats['max_HP'] = 100
    # rest should recover 5 HP
    player.health['HP'] = 0
    print player.rest()
    ok_(player.health['HP'] == 5)
    # rest should recover 1 HP (max_HP limit)
    player.health['HP'] = 99
    print player.rest()
    ok_(player.health['HP'] == 100)


def take_damage_test():
    # Test if damage and healing is resolved correctly
    player = char.Player()
    # set HP
    player.effective_stats['max_HP'] = 100
    # test damage
    player.health['HP'] = 100
    player.update_hp(-100)
    ok_(player.health['HP'] == 0)
    player.update_hp(-100)
    ok_(player.health['HP'] == -100)
    # test healing
    player.health['HP'] = 50
    player.update_hp(50)
    ok_(player.health['HP'] == 100)
    player.update_hp(50)
    ok_(player.health['HP'] == 100)


def player_equip_test():
    # Test if equipment restrictions are honoured for the player
    player = char.Player()
    player.unequip('R_hand')
    player.inventory = []
    # Test stat requirements
    wpn_desc = {
               'name': 'Testing Sword',
               'class': '1h_sword',
               'atk_type': 'slash',
               'attribute': 'str',
               'require': {'str': 4, 'dex': 4},
               'bonus': {'str': 0, 'dex': 0},
               'dmg_roll': '1d8',
               'description': "For testing only!"
               }
    testing_sword = items.Weapon(wpn_desc)
    player.pick_up(testing_sword)
    # below requirements
    player.base_stats.update({'dex': 0, 'str': 0})
    player.update_stats()
    msg = player.equip(testing_sword)
    print msg
    ok_("Unable to equip Testing Sword" in msg)
    # meets requirements
    player.base_stats.update({'dex': 4, 'str': 4})
    player.update_stats()
    msg = player.equip(testing_sword)
    print msg
    ok_(msg == "Equipped Testing Sword.")
    # already equipped
    msg = player.equip(testing_sword)
    print msg
    ok_(msg == "The item is already equipped.")
    # equip 2h weapon
    wpn_desc = {
               'name': 'Testing Bow',
               'class': 'bow',
               'atk_type': 'pierce',
               'attribute': 'dex',
               'require': {'str': 0, 'dex': 5},
               'bonus': {'str': 0, 'dex': 2},
               'dmg_roll': '1d8',
               'description': "For testing only!"
               }
    testing_bow = items.Weapon(wpn_desc)
    player.base_stats['dex'] = 5
    player.update_stats()
    msg = player.equip(testing_bow)
    print msg
    ok_(msg == "Equipped Testing Bow.")


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
    player.inventory = []

    # empty inventory
    ok_(player.get_inventory() == "Inventory is empty.")

    # add a weapon to inventory
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


