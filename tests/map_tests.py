""" Tests for the map_ module."""

from nose.tools import *
import map_
import map_gen
import char
import items


def examine_test():
    # Tests the Scene.examine method
    # Test Scene.process_equip method
    player = char.Player()
    scene = map_.Scene({'player': player})
    wpn_desc = {
               'name': 'Testing Sword',
               'atk_type': 'slash',
               'attribute': 'str',
               'dmg_roll': '1d8',
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
    sc.features['wallow'] = 'large' # +10
    a_map.add_scene(sc)
    map_gen.add_description(a_map)

    a_map.clock.time = 22 # night1 (+3)
    # chance = 10 + 3 + 1 = 14
    ok_(sc.update_encounter() == 14)


def process_equip_test():
    # Test Scene.process_equip method
    player = char.Player()
    scene = map_.Scene({'player': player})
    wpn_desc = {
               'name': 'Testing Sword',
               'atk_type': 'slash',
               'attribute': 'str',
               'dmg_roll': '1d8',
               }
    wpn = items.Weapon(wpn_desc)
    player.inventory = [wpn]
    args = '0'
    out = scene.process_equip(args)
    print out
    ok_(out == 'Equipped Testing Sword.')
