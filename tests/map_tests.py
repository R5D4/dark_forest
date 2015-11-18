""" Tests for the map_ module."""

from nose.tools import *
import map_
import map_gen
import char
import items


def take_test():
    # Test Scene.take

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

    ## Testing the take method
    # no item ID
    msg = sc.take("")
    ok_(msg == "Please indicate item ID.")
    # invalid item ID
    msg = sc.take('9')
    ok_(msg == "No such item.")
    # invalid item ID 
    msg = sc.take('nop')
    ok_(msg == "No such item.")
    # valid scenario
    msg = sc.take('0')
    ok_(msg == "Took Hunting Knife.")
    

def scene_search_test():
    # Test Scene.search (the search command)

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
    msg = sc.search()
    ok_("Hunting Knife" in msg)


def search_test():
    # Test ItemStash.search

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


def print_help_test():
    # Test the print_help method
    player = char.Player()
    scene = map_.Scene({'player': player})
    msg = scene.print_help()
    ok_("look: ['l', 'look']" in msg)


def examine_test():
    # Tests the Scene.examine method
    player = char.Player()
    scene = map_.Scene({'player': player})
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
    wpn = items.Weapon(wpn_desc)
    player.inventory = [wpn]
    args = '0'
    out = scene.examine(args)
    print out
    ok_('name: Testing Sword' in out)


def update_encounter_test():
    # Scene class.
    # Test if encounter chance is calculated as desired.

    a_map = map_.Map('story')
    sc = map_.Scene(None)
    sc.features.append(map_.Landmark('wallow', 'large')) # +10
    a_map.add_scene(sc)
    map_gen.add_descriptions(a_map)

    a_map.clock.time = 22 # night1 (+3)
    # Recall base encounter rate is 1
    # chance = 10 + 3 + 1 = 14
    ok_(sc.update_encounter() == 14)


def equip_test():
    # Test Scene.equip method
    player = char.Player()
    scene = map_.Scene({'player': player})
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
    wpn = items.Weapon(wpn_desc)
    player.inventory = [wpn]
    args = '0'
    out = scene.equip(args)
    print out
    ok_(out == 'Equipped Testing Sword.')
