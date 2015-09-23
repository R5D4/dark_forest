"""
Procedurally generates map scenes.
"""

from random import randint
from random import choice
import random
import map_

ID_SEQ = 0
EXITS = ['n', 'ne', 'e', 'se', 's', 'sw', 'w', 'nw']
OPPOSITE_EXITS = {
                 'n': 's',
                 'ne': 'sw',
                 'e': 'w', 
                 'se': 'nw', 
                 's': 'n', 
                 'sw': 'ne', 
                 'w': 'e', 
                 'nw': 'se'
                 }
CANOPY = ['none', 'oak', 'hickory', 'pine']
UNDERSTORY = ['none', 'dogwood', 'cedar', 'holly', 'young chestnut']
SHRUBS = ['none', 'blackberry', 'honeysuckle', 'poison ivy']
FLOOR = ['leafy', 'dirt', 'rocky']


def new_map():
    """ Generates a new map with random scenes."""
    a_map = map_.Map('story')

    # add entrance scene
    entrance_scene = make_entrance(a_map)
    a_map.add_scene('entrance', entrance_scene)

    # add middle scenes
    random_scene = make_random(a_map)
    #link_scene(a_map, random_scene)
    a_map.add_scene('random1', random_scene)

    # add exit scenes

    # add special scenes
    a_map.add_scene('story', map_.Story(a_map.characters))
    a_map.add_scene('death', map_.Death(a_map.characters))
    a_map.add_scene('win', map_.Win(a_map.characters))
    a_map.add_scene('quit', map_.Quit(a_map.characters))
    return a_map


def new_scene(a_map, name):
    """ Generate a new random scene."""
    scene = map_.Scene(a_map.characters)

    scene.name = name
    scene.flags['encounter_chance'] = 1

    scene.features['canopy'] = random.choice(CANOPY)
    scene.features['understory'] = random.choice(UNDERSTORY)
    scene.features['shrubs'] = random.choice(SHRUBS)
    scene.features['floor'] = random.choice(FLOOR)

    scene.description = ""
    for feature in scene.features.keys():
        scene.description += "The {} is {}. ".format(feature, 
                                                     scene.features[feature])

    scene.description += "Exits are to the "
    for e in scene.exits.keys():
        scene.description += "{}, ".format(e)
    return scene


def link_scene(a_map, scene):
    """ Generates exits in the scene given all other existing scenes."""
    if a_map.scenes: # only one scene, no need to add exits
        pass
    else:
        # create 2-4 exits
        for i in range(2,4):
            other_scene = choice(a_map.scenes.items())


def make_entrance(a_map):
    """
    Generate an entrance scene.
    """
    return new_scene(a_map, 'entrance')


def make_exit():
    """
    Generate an exit scene.
    """
    global ID_SEQ
    name = "scene{}".format(ID_SEQ)
    ID_SEQ += 1
    return new_scene(a_map, name)


def make_random(a_map):
    """
    Generate a scene.
    """
    global ID_SEQ
    name = "scene{}".format(ID_SEQ)
    ID_SEQ += 1
    return new_scene(a_map, name)
