""" Tests for the map_ module."""

from nose.tools import *
import map_
import map_gen
import char
import items
from tests.test_data import *

########## Map Class Tests ##########


def boss_at_lair_test():
    # Test if we can correctly determine if the boss is in the lair scene
    # create map
    a_map = map_.Map('story')
    # add a scene
    s1 = map_gen.new_scene(a_map, None, (5, 5))
    s1.name = 'scene1'
    a_map.add_scene(s1)
    s1.features = [] # no features
    # add a lair in s1
    map_gen.add_lair(a_map)
    # add another scene
    s2 = map_gen.new_scene(a_map, None, (6, 5))
    s2.name = 'scene2'
    a_map.add_scene(s2)
    s2.features = [] # no features

    # Test 1: boss at lair
    a_map.boss_scene_name = s1.name
    ok_(a_map.boss_at_lair())
    # Test 2: boss not at lair
    a_map.boss_scene_name = s2.name
    ok_(not a_map.boss_at_lair())


def construct_path_test():
    # Test path construction

    # map 1: 1-2-3-4
    a_map = map_.Map('story')
    s1 = map_gen.new_scene(a_map, None, (5, 5))
    s1.name = 'scene1'
    a_map.add_scene(s1)
    s2 = map_gen.new_scene(a_map, None, (6, 5))
    s2.name = 'scene2'
    a_map.add_scene(s2)
    s3 = map_gen.new_scene(a_map, None, (7, 5))
    s3.name = 'scene3'
    a_map.add_scene(s3)
    s4 = map_gen.new_scene(a_map, None, (8, 5))
    s4.name = 'scene4'
    a_map.add_scene(s4)
    # create links
    map_gen.create_link(s1, s2)
    map_gen.create_link(s2, s3)
    map_gen.create_link(s3, s4)
    # test 1: 1 to 4
    path = a_map.construct_path(s1.name, s4.name)
    print path
    ok_(path == ['scene4', 'scene3', 'scene2'])
    # test 2: 2 to 4
    path = a_map.construct_path(s2.name, s4.name)
    print path
    ok_(path == ['scene4', 'scene3'])
    # test 3: 3 to 4
    path = a_map.construct_path(s3.name, s4.name)
    print path
    ok_(path == ['scene4'])

    # map 2: 
    #   1
    #   |\
    #   2 3
    #   | |
    #   5-4
    a_map = map_.Map('story')
    s1 = map_gen.new_scene(a_map, None, (5, 5))
    s1.name = 'scene1'
    a_map.add_scene(s1)
    s2 = map_gen.new_scene(a_map, None, (5, 6))
    s2.name = 'scene2'
    a_map.add_scene(s2)
    s3 = map_gen.new_scene(a_map, None, (6, 6))
    s3.name = 'scene3'
    a_map.add_scene(s3)
    s4 = map_gen.new_scene(a_map, None, (6, 7))
    s4.name = 'scene4'
    a_map.add_scene(s4)
    s5 = map_gen.new_scene(a_map, None, (5, 7))
    s5.name = 'scene5'
    a_map.add_scene(s5)
    # create links
    map_gen.create_link(s1, s2)
    map_gen.create_link(s1, s3)
    map_gen.create_link(s2, s5)
    map_gen.create_link(s3, s4)
    map_gen.create_link(s4, s5)
    # test 1: 1 to 5
    path = a_map.construct_path(s1.name, s5.name)
    print path
    ok_(path == ['scene5', 'scene2'])
    # test 2: 3 to 2
    path = a_map.construct_path(s3.name, s2.name)
    print path
    ok_(path == ['scene2', 'scene1'])


def move_boss_test():
    # Tests boss' movement on the map

    # create map: 1-2-3 
    a_map = map_.Map('story')
    s1 = map_gen.new_scene(a_map, None, (5, 5))
    s1.name = 'scene1'
    a_map.add_scene(s1)
    s2 = map_gen.new_scene(a_map, None, (6, 5))
    s2.name = 'scene2'
    a_map.add_scene(s2)
    s3 = map_gen.new_scene(a_map, None, (7, 5))
    s3.name = 'scene3'
    a_map.add_scene(s3)
    map_gen.create_link(s1, s2)
    map_gen.create_link(s2, s3)
    # set lair and spawn boss
    a_map.boss_scene_name = s1.name
    a_map.lair_scene_name = s1.name
    s1.flags['encounter'] = True

    # test 1: daytime, in lair scene
    for t in range(7, 20): # 0700 to 1900
        a_map.clock.time = t
        new_scene, direction = a_map.move_boss()
        ok_(not a_map.path) # no path chosen
        ok_(new_scene == s1.name and not direction) # should stay in same scene

    # test 2: daytime, not in lair scene
    for t in range(7, 20): # 0700 to 1900
        a_map.clock.time = t
        a_map.path = [] # reset path
        a_map.boss_scene_name = s3.name # spawn boss away from lair
        new_scene, direction = a_map.move_boss()
        ok_(a_map.path) # path to lair constructed

    # test 3: nighttime
    moved = False
    a_map.clock.time = 20
    for t in range(10): # 2000 to 0600
        a_map.clock.tick()
        a_map.boss_scene_name = s3.name # spawn boss away from lair
        new_scene, direction = a_map.move_boss()
        if direction: # not None
            moved = True
        ok_(not a_map.path) # no path chosen
    ok_(moved) # should have moved at least once (randomly)


# NOTE: disabled for updates
#def map_update_clues_test():
#    # Test Map.update_clues method
#
#    # create map and characters
#    a_map = map_.Map('story')
#    player = char.Player()
#    boar = char.Boar()
#    a_map.characters['player'] = player
#    a_map.characters['boar'] = boar
#    # add two adjacent scenes
#    s1 = map_gen.new_scene(a_map, None, (5, 5))
#    s1.name = 'scene1'
#    a_map.add_scene(s1)
#    # scene2 is east of scene1
#    s2 = map_gen.new_scene(a_map, None, (6, 5))
#    s2.name = 'scene2'
#    a_map.add_scene(s2)
#    map_gen.create_link(s1, s2)
#    # put some clues in the scenes
#    s1.clues.append(map_.FootprintClue('e')) # ttl = 12
#    s2.clues.append(map_.DroppingsClue()) # ttl = 8
#    # update clues one clock tick
#    a_map.update_clues()
#    ok_(s1.clues) # both clues should still exist
#    ok_(s2.clues)
#    # update clues 7 more times
#    for i in range(7):
#        a_map.update_clues()
#    ok_(not s2.clues) # droppings should disappear
#    ok_(s1.clues) # footprint should still be there
#    # update clues 4 more times
#    for i in range(4):
#        a_map.update_clues()
#    ok_(not s1.clues) # footprints should disappear

########## Scene Class Tests ##########


def cmd_unequip_test():
    # Test 'unequip' command
    # NOTE: implement this
    pass


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


def print_encounter_msg_test():
    # Test if encounter messages are printed correctly

    # create map and characters
    a_map = map_.Map('story')
    player = char.Player()
    boar = char.Boar()
    a_map.characters['player'] = player
    a_map.characters['boar'] = boar
    # add a scene
    s1 = map_gen.new_scene(a_map, None, (5, 5))
    s1.name = 'scene1'
    a_map.add_scene(s1)
    # spawn the boss in s1 and put it in the lair
    a_map.boss_scene_name = s1.name
    s1.features = [] # no features
    map_gen.add_lair(a_map)
    lair = s1.features[0]

    # boss in lair, lair unrevealed
    lair.revealed = False
    lair.has_boss = True
    s1.flags['encounter'] = False
    ok_(s1.print_encounter_msg() is None)
    # boss in lair, lair revealed
    lair.revealed = True
    lair.has_boss= True
    s1.flags['encounter'] = True
    ok_(s1.print_encounter_msg() == "You can see movement inside the beast's \
lair!")
    # boss not in scene, lair unrevealed
    lair.revealed = False
    lair.has_boss = False
    s1.flags['encounter'] = False
    ok_(s1.print_encounter_msg() is None)
    # boss not in scene, lair revealed
    lair.revealed = True
    lair.has_boss = False
    s1.flags['encounter'] = False
    ok_(s1.print_encounter_msg() is None)
    # boss in scene (not in lair), lair unrevealed
    lair.revealed = False
    lair.has_boss= False
    s1.flags['encounter'] = True
    ok_(s1.print_encounter_msg() == "You see the boar! You don't think it \
notices you.")
    # boss in scene (not in lair), lair revealed
    lair.revealed = True
    lair.has_boss= False
    s1.flags['encounter'] = True
    ok_(s1.print_encounter_msg() == "You see the boar! You don't think it \
notices you.")


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
    a_map.clock.time = 22
    s1.flags['encounter'] = False
    ok_(not s1.get_boss_attack())
    # Should not attack (HP too low)
    a_map.clock.time = 22
    s1.flags['encounter'] = True
    boar.health['HP'] = 29
    ok_(not s1.get_boss_attack())
    # Should not attack (daytime)
    a_map.clock.time = 10
    s1.flags['encounter'] = True
    boar.health['HP'] = 30
    ok_(not s1.get_boss_attack())
    # Should attack with non-zero chance
    a_map.clock.time = 22
    s1.flags['encounter'] = True
    boar.health['HP'] = 30
    attacked = False
    for i in xrange(50): # 99.999...% chance that this result is correct
        attacked = s1.get_boss_attack()
        if attacked:
            break
    ok_(attacked)


def get_lair_test():
    # Test retrieving the Lair object from a scene

    # create map
    a_map = map_.Map('story')
    # add a scene
    s1 = map_gen.new_scene(a_map, None, (5, 5))
    s1.name = 'scene1'
    a_map.add_scene(s1)
    s1.features = [] # no features
    # add a lair as the only feature
    map_gen.add_lair(a_map)

    # Get the Lair object
    lair = s1.get_lair()
    ok_(isinstance(lair, map_.Lair))

########## Clue Class/Subclasses Tests ##########


def add_clue_test():
    # Test the Clue.add_clue method

    # FootprintClue
    clue = map_.FootprintClue('n')
    ok_(clue.count == 1)
    clue.add_clue('w')
    clue.direction == 'w'
    ok_(clue.count == 2)
    clue.add_clue('s')
    clue.direction == 's'
    ok_(clue.count == 3)


def clue_update_test():
    # Test update method of Clue subclasses

    # FootprintClue
    clue = map_.FootprintClue('n')
    ok_(clue.fresh == 2)
    clue.update()
    ok_(clue.fresh == 1)
    clue.fresh = 0
    clue.update()
    ok_(clue.fresh == 0)
    
    # BrokenTreeClue
    clue = map_.BrokenTreeClue()
    ok_(clue.fresh == 2)
    clue.update()
    ok_(clue.fresh == 1)
    clue.fresh = 0
    clue.update()
    ok_(clue.fresh == 0)

    # SlainAnimalClue
    clue = map_.SlainAnimalClue()
    ok_(clue.fresh == 2)
    clue.update()
    ok_(clue.fresh == 1)
    clue.fresh = 0
    clue.update()
    ok_(clue.fresh == 0)


def footprint_init_test():
    # Test creating FootprintClue objects
    clue = map_.FootprintClue('n')
    ok_(clue.direction == 'n')

########## ItemStash Class Tests ##########


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

########## Lair Class Tests ##########


def lair_init_test():
    # Test creating a Lair object
    lair = map_.Lair()
    ok_(not lair.revealed)


def lair_get_desc_test():
    # Test returning the description
    lair = map_.Lair()
    # not revealed
    msg = lair.get_desc()
    ok_(not msg)
    # revealed
    lair.revealed = True
    msg = lair.get_desc()
    ok_(msg == "There's a cave entrance behind the thick brush, it's the \
lair of the forest guardian!")


def lair_search_test():
    # Test searching for the lair
    lair = map_.Lair()
    msg = ""
    # test that the search method eventually uncovers the lair
    for i in xrange(50): # 99.5% accurate test
        msg = lair.search()
        if msg: # if not empty string, meaning search as successful
            break
    ok_(msg == "You've uncovered a secret lair!")
    ok_(lair.revealed)

########## Utility Functions Tests ##########


def update_desc_test():
    # Test update description function

    # create map and characters
    a_map = map_.Map('story')
    player = char.Player()
    boar = char.Boar()
    a_map.characters['player'] = player
    a_map.characters['boar'] = boar
    # add a scene
    s1 = map_gen.new_scene(a_map, None, (5, 5))
    s1.name = 'scene1'
    a_map.add_scene(s1)
    s1.features = [] # no features
    # add a lair as the only feature
    map_gen.add_lair(a_map)
    lair = s1.features[0]

    # unrevealed lair
    ok_(s1.description == "No description available.")
    # revealed lair
    lair.revealed = True
    map_.update_desc(s1)
    print s1.description
    ok_("There's a cave entrance behind the thick brush, it's the lair of the \
forest guardian!" in s1.description)

    
