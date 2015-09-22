"""
Procedurally generates map scenes.
"""

import random
import map_

EXITS = ['n', 'ne', 'e', 'se', 's', 'sw', 'w', 'nw']
CANOPY = ['oak', 'hickory', 'pine']
UNDERSTORY = ['dogwood', 'cedar', 'holly', 'young chestnut']
SHRUBS = ['blackberry', 'honeysuckle', 'poison ivy']
FLOOR = ['leafy', 'dirt', 'rocky']

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
    scene.flags['encounter_chance'] = 0.5
    scene.features['canopy'] = random.choice(CANOPY)
    scene.features['understory'] = random.choice(UNDERSTORY)
    scene.features['shrubs'] = random.choice(SHRUBS)
    scene.features['floor'] = random.choice(FLOOR)
    scene.description = "The canopy is {}. The understory is {}, the shrubs\
 are {}. The floor is {}.".format(scene.features['canopy'],
                                  scene.features['understory'],
                                  scene.features['shrubs'],
                                  scene.features['floor'])
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
