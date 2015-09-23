"""
Procedurally generates map scenes.
"""

import random
import map_

EXITS = ['n', 'ne', 'e', 'se', 's', 'sw', 'w', 'nw']
CANOPY = ['none', 'oak', 'hickory', 'pine']
UNDERSTORY = ['none', 'dogwood', 'cedar', 'holly', 'young chestnut']
SHRUBS = ['none', 'blackberry', 'honeysuckle', 'poison ivy']
FLOOR = ['leafy', 'dirt', 'rocky']


def new_map():
    """ Generates a new map with random scenes."""
    a_map = map_.Map('story')
    entrance_scene = make_entrance(a_map.characters)
    a_map.add_scene('entrance', entrance_scene)
    return a_map

def new_scene(characters):
    scene = map_.Scene(characters)
    scene.exits = {}
    scene.flags = {}
    scene.features = {}
    return scene


def make_entrance(characters):
    """
    Generate an entrance scene.
    """
    scene = new_scene(characters)

    scene.flags['encounter_chance'] = 1

    scene.features['canopy'] = random.choice(CANOPY)
    scene.features['understory'] = random.choice(UNDERSTORY)
    scene.features['shrubs'] = random.choice(SHRUBS)
    scene.features['floor'] = random.choice(FLOOR)

    scene.description = ""
    for feature in scene.features.keys():
        scene.description += "The {} is {}. ".format(feature, 
                                                     scene.features[feature])
    return scene


def make_exit():
    """
    Generate an exit scene.
    """
    pass


def make_random():
    """
    Generate a scene that's not an entrance or exit.
    """
    scene = new_scene()
    scene.features['canopy'] = random.choice(CANOPY)
    scene.features['understory'] = random.choice(UNDERSTORY)
    scene.features['shrubs'] = random.choice(SHRUBS)
    scene.features['floor'] = random.choice(FLOOR)
    return scene
