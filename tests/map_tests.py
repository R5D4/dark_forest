""" Tests for the map_ module."""

from nose.tools import *
import map_
import map_gen
import char
import items
from tests.test_data import *


def random_clue_test():
    # Test generation of random Clue object
    for i in xrange(50):
        clue = map_.random_clue()
        ok_(clue) # not None
        ok_(clue.clue_type in ['footprint', 'droppings', 'rubbing'])


def cmd_unequip_test():
    # Test 'unequip' command
    # NOTE: implement this
    pass


def cmd_equip_test():
    # Test 'equip' command
    player = char.Player()
    scene = map_.Scene({'player': player})
    wpn = items.Weapon(TESTING_SWORD)
    player.inventory = [wpn]

    # no argument
    args = None
    msg = scene.cmd_equip(args)
    print msg
    ok_('R_hand' in msg)
    # argument is out of bound
    args = '10'
    msg = scene.cmd_equip(args)
    print msg
    ok_(msg == "No such item.")
    # argument isn't an integer
    args = 'hello'
    msg = scene.cmd_equip(args)
    print msg
    ok_(msg == "No such item.")


def cmd_drop_test():
    # Test 'drop' command

    ## Setup
    # create scene
    a_map = map_.Map('story')
    a_map.add_player()
    sc = map_gen.new_scene(a_map, 'random', (0,0))

    # initialize player equipment and inventory
    player = sc.characters['player']
    player.unequip('R_hand')
    player.inventory = []
    knife = items.Weapon(TESTING_KNIFE)
    bow = items.Weapon(TESTING_BOW)
    shield = items.Armor(TESTING_SHIELD)

    # set player base stats to be able to equip everything
    player.base_stats.update({'dex': 100, 'str': 100, 'AC': 100})

    ## Testing the 'drop' command
    # no item ID
    msg = sc.cmd_drop(None)
    ok_(msg == "Please indicate item ID.")
    # invalid item ID (out of range)
    msg = sc.cmd_drop('9')
    ok_(msg == "No such item.")
    # invalid item ID (not an integer)
    msg = sc.cmd_drop('nop')
    ok_(msg == "No such item.")
    # drop unequipped weapon
    player.pick_up(knife)
    msg = sc.cmd_drop('0')
    ok_(msg == "Dropped Testing Knife.")
    ok_(knife not in player.inventory)
    ok_(knife in sc.items)
    # drop equipped weapon (1H)
    sc.items = []
    player.pick_up(knife)
    player.equip(knife)
    msg = sc.cmd_drop('0')
    ok_(msg == "Dropped Testing Knife.")
    ok_(not knife.equipped)
    ok_(knife not in player.equipped)
    ok_(player.equipped_names['R_hand'] is None)
    ok_(knife not in player.inventory)
    ok_(knife in sc.items)
    # drop equipped weapon (2H)
    sc.items = []
    player.pick_up(bow)
    player.equip(bow)
    msg = sc.cmd_drop('0')
    ok_(msg == "Dropped Testing Bow.")
    ok_(not bow.equipped)
    ok_(bow not in player.equipped)
    ok_(player.equipped_names['R_hand'] is None)
    ok_(player.equipped_names['L_hand'] is None)
    ok_(bow not in player.inventory)
    ok_(bow in sc.items)

    ## drop one of two equipped weapons
    sc.items = []
    player.pick_up(shield)
    player.pick_up(knife)
    player.equip(shield)
    player.equip(knife)
    msg = sc.cmd_drop('0') # drop shield
    # check left hand is unequipped
    ok_(msg == "Dropped Testing Shield.")
    ok_(not shield.equipped)
    ok_(shield not in player.equipped)
    ok_(player.equipped_names['L_hand'] is None)
    ok_(shield not in player.inventory)
    ok_(shield in sc.items)
    # check right hand is still equipped
    ok_(knife.equipped)
    ok_(knife in player.equipped)
    ok_(player.equipped_names['R_hand'] == "Testing Knife")
    ok_(knife in player.inventory)
    ok_(knife not in sc.items)


def cmd_take_test():
    # Test 'take' command

    ## Setup
    # create scene
    a_map = map_.Map('story')
    a_map.add_player()
    sc = map_gen.new_scene(a_map, 'random', (0,0))
    # empty player inventory
    player = sc.characters['player']
    player.inventory = []
    # create item
    w = items.get_weapon("Hunting Knife")
    # add items to scene
    sc.items.append(w)

    ## Testing the 'take' command
    # no item ID
    msg = sc.cmd_take(None)
    ok_(msg == "Please indicate item ID.")
    # invalid item ID
    msg = sc.cmd_take('9')
    ok_(msg == "No such item.")
    # invalid item ID 
    msg = sc.cmd_take('nop')
    ok_(msg == "No such item.")
    # valid scenario
    msg = sc.cmd_take('0')
    ok_(msg == "Took Hunting Knife.")
    ok_(w not in sc.items)
    

def cmd_search_test():
    # Test 'search' command

    # create scene
    a_map = map_.Map('story')
    sc = map_gen.new_scene(a_map, 'random', (0,0))
    # create items
    wps = [items.get_weapon("Hunting Knife")]
    # add items to item stash
    stash = map_.ItemStash(wps)
    # add item stash to scene
    sc.features.append(stash)
    # search scene and check results
    msg = sc.cmd_search()
    ok_("Hunting Knife" in msg)


def itemstash_search_test():
    # Test ItemStash.search method

    hidden = []
    # generate weapon 1
    w1 = items.new_weapon()
    w1.desc['name'] = "Weapon 1"
    w1.desc['rarity'] = 0
    # generate weapon 2
    w2 = items.new_weapon()
    w2.desc['name'] = "Weapon 2"
    w2.desc['rarity'] = 0
    # generate weapon 3
    w3 = items.new_weapon()
    w3.desc['name'] = "Weapon 3"
    w3.desc['rarity'] = 100 # more than max find chance possible

    # test no items
    stash = map_.ItemStash([])
    ok_(stash.search() == [])
    ok_(stash.hidden_items == [])
    # test one item with lowest rarity
    hidden = [w1]
    stash = map_.ItemStash(hidden)
    discovered = stash.search()
    ok_(w1 in discovered)
    ok_(stash.hidden_items == [])
    # test two items with lowest rarity
    hidden = [w1, w2]
    stash = map_.ItemStash(hidden)
    discovered = stash.search()
    ok_(w1 in discovered and w2 in discovered)
    ok_(stash.hidden_items == [])
    # test two items, one is not discoverable
    hidden = [w1, w3]
    stash = map_.ItemStash(hidden)
    discovered = stash.search()
    ok_(w1 in discovered and w3 not in discovered)
    ok_(stash.hidden_items == [w3])


def cmd_help_test():
    # Test the print_help method
    player = char.Player()
    scene = map_.Scene({'player': player})
    msg = scene.cmd_help()
    for k in map_.ENV_ACTIONS.keys():
        ok_(k in msg)


def cmd_examine_test():
    # Tests the Scene.examine method
    player = char.Player()
    scene = map_.Scene({'player': player})
    wpn = items.Weapon(TESTING_SWORD)
    player.inventory = [wpn]
    args = '0'
    out = scene.cmd_examine(args)
    print out
    ok_('name: Testing Sword' in out)

