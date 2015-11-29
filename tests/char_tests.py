""" Tests for the char module."""

from nose.tools import *
import char
import items
from tests.test_data import *


def new_player_test():
    # Test new player objects are created properly
    player = char.Player()
    
    # check stats (including health and conditions)
    ok_(player.base_stats['str'] > 0)
    ok_(player.base_stats['dex'] > 0)
    ok_(player.base_stats['AC'] > 10)
    ok_(player.base_stats['max_HP'] > 100)
    ok_(player.health['HP'] == player.base_stats['max_HP'])
    ok_(not player.conditions['surprised']) # conditions all False
    ok_(not player.conditions['bloodied'])
    ok_(not player.conditions['poisoned'])

    # check description
    ok_('name' in player.desc)
    ok_('job' in player.desc)
    ok_('desc' in player.desc)

    # check inventory and equipment
    ok_(player.inventory[0].desc['name'] == 'Hunting Knife') # default weapon
    ok_(player.equipped[0].desc['name'] == 'Hunting Knife') # equipped
    ok_(not player.equipped_names['head'])
    ok_(not player.equipped_names['torso'])
    ok_(player.equipped_names['R_hand']) # not None
    ok_(not player.equipped_names['L_hand'])
    ok_(not player.equipped_names['legs'])
    ok_(not player.equipped_names['feet'])


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
    player.base_stats.update({'dex': 5, 'str': 5})
    msg = player.equip(testing_sword)
    print msg
    ok_(msg == "Equipped Testing Sword.")
    ok_(testing_sword.equipped)
    ok_(testing_sword in player.equipped)
    ok_(player.equipped_names['R_hand'] == "Testing Sword")
    # already equipped
    msg = player.equip(testing_sword)
    print msg
    ok_(msg == "The item is already equipped.")
    ok_(testing_sword.equipped)
    ok_(testing_sword in player.equipped)
    ok_(player.equipped_names['R_hand'] == "Testing Sword")

    ## Equip two weapons
    testing_shield = items.Armor(TESTING_SHIELD)
    player.base_stats['str'] = 10 
    player.pick_up(testing_shield)
    msg = player.equip(testing_shield)
    print msg
    ok_(msg == "Equipped Testing Shield.")
    ok_(testing_sword.equipped)
    ok_(testing_shield.equipped)
    ok_(testing_sword in player.equipped)
    ok_(testing_shield in player.equipped)
    ok_(player.equipped_names['R_hand'] == "Testing Sword")
    ok_(player.equipped_names['L_hand'] == "Testing Shield")

    ## Equip 2H weapon while both hands have weapons
    testing_bow = items.Weapon(TESTING_BOW)
    player.base_stats['dex'] = 10 
    msg = player.equip(testing_bow)
    print msg
    ok_(msg == "Equipped Testing Bow.")
    ok_(testing_bow.equipped)
    ok_(not testing_sword.equipped)
    ok_(not testing_shield.equipped)
    ok_(testing_bow in player.equipped)
    ok_(testing_sword not in player.equipped)
    ok_(testing_shield not in player.equipped)
    ok_(player.equipped_names['R_hand'] == "Testing Bow")
    ok_(player.equipped_names['L_hand'] == "Testing Bow")

    ## Equip 1H weapon while a 2H weapon is equipped
    msg = player.equip(testing_sword)
    print msg
    ok_(msg == "Equipped Testing Sword.")
    ok_(testing_sword.equipped)
    ok_(not testing_bow.equipped)
    ok_(testing_sword in player.equipped)
    ok_(testing_bow not in player.equipped)
    ok_(player.equipped_names['R_hand'] == "Testing Sword")
    ok_(player.equipped_names['L_hand'] == None)


def player_unequip_test():
    # Test unequipping items for the player

    # initialize player equipment and inventory
    player = char.Player()
    player.unequip('R_hand')
    player.inventory = []
    sword  = items.Weapon(TESTING_SWORD)
    shield  = items.Armor(TESTING_SHIELD)
    bow  = items.Weapon(TESTING_BOW)
    player.pick_up(sword)
    player.pick_up(shield)
    player.pick_up(bow)

    # set player base stats to be able to equip everything
    player.base_stats.update({'dex': 100, 'str': 100, 'AC': 100})

    # unequip empty slot
    ok_(player.unequip('R_hand') == "Nothing equipped.")

    # unequip only weapon
    player.equip(sword)
    ok_(player.unequip('R_hand') == "Unequipped Testing Sword.")
    ok_(sword not in player.equipped)
    ok_(not sword.equipped)
    ok_(player.equipped_names['R_hand'] is None)

    # unequip one of two weapons
    player.equip(sword)
    player.equip(shield)
    ok_(player.unequip('R_hand') == "Unequipped Testing Sword.")
    ok_(sword not in player.equipped)
    ok_(not sword.equipped)
    ok_(player.equipped_names['R_hand'] is None)
    ok_(shield in player.equipped)
    ok_(shield.equipped)
    ok_(player.equipped_names['L_hand'] == "Testing Shield")

    ## unequip a 2H weapon
    # unequip using R_hand
    player.equip(bow)
    ok_(player.unequip('R_hand') == "Unequipped Testing Bow.")
    ok_(bow not in player.equipped)
    ok_(not bow.equipped)
    ok_(player.equipped_names['R_hand'] is None)
    ok_(player.equipped_names['L_hand'] is None)
    # unequip using L_hand
    player.equip(bow)
    ok_(player.unequip('L_hand') == "Unequipped Testing Bow.")
    ok_(bow not in player.equipped)
    ok_(not bow.equipped)
    ok_(player.equipped_names['R_hand'] is None)
    ok_(player.equipped_names['L_hand'] is None)


def update_stats_test():
    # Test if bonus stat and effective stat are calculated properly

    # unequip all items and empty inventory
    player = char.Player()
    player.unequip('R_hand')
    player.inventory = []

    # set player base stats to be able to equip everything
    player.base_stats.update({'dex': 100, 'str': 100, 'AC': 100})

    # one weapon (1H)
    w1 = items.Weapon(TESTING_KNIFE)
    player.equip(w1)
    ok_(player.bonus_stats['dex'] == 10)
    ok_(player.effective_stats['dex'] == 110)

    # two weapons
    w2 = items.Weapon(TESTING_SWORD)
    w3 = items.Armor(TESTING_SHIELD)
    player.equip(w2)
    player.equip(w3)
    ok_(player.bonus_stats['str'] == 10)
    ok_(player.bonus_stats['AC'] == 20)
    ok_(player.bonus_stats['dex'] == -10)
    ok_(player.effective_stats['str'] == 110)
    ok_(player.effective_stats['AC'] == 120)
    ok_(player.effective_stats['dex'] == 90)

    # one weapon (2H)
    w4 = items.Weapon(TESTING_BOW)
    player.equip(w4)
    ok_(player.bonus_stats['dex'] == 10)
    ok_(player.effective_stats['dex'] == 110)


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


