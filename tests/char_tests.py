""" Tests for the char module."""

from nose.tools import *
import char
import items
from tests.test_data import *


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
    # Test equipping items on the player

    # unequip all items and empty inventory
    player = char.Player()
    player.unequip('R_hand')
    player.inventory = []

    ## Equip one weapon
    testing_sword = items.Weapon(TESTING_SWORD)
    player.pick_up(testing_sword)
    # below requirements
    player.base_stats.update({'dex': 0, 'str': 0})
    msg = player.equip(testing_sword)
    print msg
    ok_("Unable to equip Testing Sword" in msg)
    ok_(testing_sword not in player.equipped)
    ok_(player.equipped_names['R_hand'] is None)
    # meets requirements
    player.base_stats.update({'dex': 4, 'str': 4})
    msg = player.equip(testing_sword)
    print msg
    ok_(msg == "Equipped Testing Sword.")
    ok_(testing_sword in player.equipped)
    ok_(player.equipped_names['R_hand'] == "Testing Sword")
    # already equipped
    msg = player.equip(testing_sword)
    print msg
    ok_(msg == "The item is already equipped.")
    ok_(testing_sword in player.equipped)
    ok_(player.equipped_names['R_hand'] == "Testing Sword")

    ## Equip a weapon in the empty hand
    testing_shield = items.Weapon(TESTING_SHIELD)
    player.pick_up(testing_shield)
    msg = player.equip(testing_shield)
    print msg
    ok_(msg == "Equipped Testing Shield.")
    ok_(testing_shield in player.equipped)
    ok_(player.equipped_names['L_hand'] == "Testing Shield")

    ## Equip 2H weapon while equipping one weapon in each hand
    testing_bow = items.Weapon(TESTING_BOW)
    player.base_stats['dex'] = 5
    msg = player.equip(testing_bow)
    print msg
    ok_(msg == "Equipped Testing Bow.")
    ok_(testing_bow in player.equipped)
    ok_(testing_sword not in player.equipped)
    ok_(testing_shield not in player.equipped)
    ok_(player.equipped_names['R_hand'] == "Testing Bow")
    ok_(player.equipped_names['L_hand'] == "Testing Bow")

    ## Equip 1H weapon while a 2H weapon is equipped
    msg = player.equip(testing_sword)
    print msg
    ok_(msg == "Equipped Testing Sword.")
    ok_(testing_sword in player.equipped)
    ok_(testing_bow not in player.equipped)
    ok_(player.equipped_names['R_hand'] == "Testing Sword")
    ok_(player.equipped_names['L_hand'] == None)


def update_stats_test():
    # Test application of bonus stats and attacks on equipment change
    # NOTE: implement this
    player = char.Player()
    pass


def player_unequip_test():
    # Test unequipping items for the player
    # NOTE: need more test cases
    player = char.Player()
    weapon = items.Weapon(TESTING_KNIFE)
    player.inventory = []
    player.pick_up(weapon)
    player.equip(weapon)
    ok_(player.unequip('R_hand') == "Unequipped Testing Knife.")
    ok_(player.unequip('R_hand') == "Nothing equipped.")


def get_inventory_test():
    # check if inventory is printed correctly
    player = char.Player()
    player.inventory = []

    # empty inventory
    ok_(player.get_inventory() == "Inventory is empty.")

    # add a weapon to inventory
    weapon = items.Weapon(TESTING_KNIFE)
    player.pick_up(weapon)

    # unequipped
    ok_(player.get_inventory() == "0: Testing Knife")

    # equipped
    player.equip(weapon)
    ok_(player.get_inventory() == "0: Testing Knife[E]")


def get_equipped_test():
    # Test if equipped items are output correctly
    player = char.Player()
    weapon = items.Weapon(TESTING_KNIFE)
    player.equip(weapon)
    print player.get_equipped()
    ok_("R_hand: Testing Knife" in player.get_equipped())


