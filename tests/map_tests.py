""" Tests for the map_ module."""

from nose.tools import *
import map_
import map_gen
import char
import items
from tests.test_data import *


def move_boss2_test():
    # Test the new boss movement algorithm
    # NOTE: rename this after renaming the method
    pass


def move_boss_test():
    # Tests boss' movement on the map

    # create map and characters
    a_map = map_.Map('story')
    player = char.Player()
    boar = char.Boar()
    a_map.characters['player'] = player
    a_map.characters['boar'] = boar
    # add two adjacent scenes
    s1 = map_gen.new_scene(a_map, None, (5, 5))
    s1.name = 'scene1'
    a_map.add_scene(s1)
    s2 = map_gen.new_scene(a_map, None, (6, 5))
    s2.name = 'scene2'
    a_map.add_scene(s2)
    map_gen.create_link(s1, s2)
    # spawn the boss in s1
    a_map.boss_scene_name = s1.name
    s1.flags['encounter'] = True
    # move the boss
    direction = a_map.move_boss()
    print direction
    ok_(direction == (s1.name, None) or direction == (s1.name, 'e'))
    if direction == 'e':
        ok_(not s1.flags['encounter'])
        ok_(s2.flags['encounter'])
        a_map.boss_scene_name == s2.name


def get_boss_attack_test():
    # Test when the boss will attack
    # create map and characters
    a_map = map_.Map('story')
    boar = char.Boar()
    boar.effective_stats['max_HP'] = 100
    a_map.characters['boar'] = boar
    # add two adjacent scenes
    s1 = map_gen.new_scene(a_map, None, (5, 5))
    s1.name = 'scene1'
    a_map.add_scene(s1)
    # Should not attack (boss not in scene)
    s1.flags['encounter'] = False
    ok_(not s1.get_boss_attack())
    # Should not attack (HP too low)
    s1.flags['encounter'] = True
    boar.health['HP'] = 29
    ok_(not s1.get_boss_attack())
    # Should attack with non-zero chance
    s1.flags['encounter'] = True
    boar.health['HP'] = 30
    attacked = False
    for i in xrange(50): # 99.999...% chance that this result is correct
        attacked = s1.get_boss_attack()
        if attacked:
            break
    ok_(attacked)


def map_update_clues_test():
    # Test Map.update_clues method

    # create map and characters
    a_map = map_.Map('story')
    player = char.Player()
    boar = char.Boar()
    a_map.characters['player'] = player
    a_map.characters['boar'] = boar
    # add two adjacent scenes
    s1 = map_gen.new_scene(a_map, None, (5, 5))
    s1.name = 'scene1'
    a_map.add_scene(s1)
    # scene2 is east of scene1
    s2 = map_gen.new_scene(a_map, None, (6, 5))
    s2.name = 'scene2'
    a_map.add_scene(s2)
    map_gen.create_link(s1, s2)
    # put some clues in the scenes
    s1.clues.append(map_.FootprintClue('e')) # ttl = 12
    s2.clues.append(map_.DroppingsClue()) # ttl = 8
    # update clues one clock tick
    a_map.update_clues()
    ok_(s1.clues) # both clues should still exist
    ok_(s2.clues)
    # update clues 7 more times
    for i in range(7):
        a_map.update_clues()
    ok_(not s2.clues) # droppings should disappear
    ok_(s1.clues) # footprint should still be there
    # update clues 4 more times
    for i in range(4):
        a_map.update_clues()
    ok_(not s1.clues) # footprints should disappear


def clue_update_test():
    # Test update method of Clue subclasses
    clue = map_.FootprintClue('n')
    ok_(clue.ttl == 12)
    clue.update()
    ok_(clue.ttl == 11)
    clue.ttl = 0
    clue.update()
    ok_(clue.ttl == -1)


def footprint_init_test():
    # Test creating FootprintClue objects
    clue = map_.FootprintClue('n')
    ok_(clue.direction == 'n')


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

