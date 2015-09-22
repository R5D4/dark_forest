"""
Procedurally generates map scenes.
"""

from map_ import Scene
import random

EXITS = ['n', 'ne', 'e', 'se', 's', 'sw', 'w', 'nw']
CANOPY = ['oak', 'hickory', 'pine']
UNDERSTORY = ['dogwood', 'cedar', 'holly', 'young chestnut']
SHRUBS = ['blackberry', 'honeysuckle', 'poison ivy']
FLOOR = ['leafy', 'dirt', 'rocky']

def new_scene():
    new_scene = Scene(None)
    new_scene.exits = {}
    new_scene.flags = {}
    new_scene.features = {}
    return new_scene

def make_entrance():
    """
    Generate an entrance scene.
    """
    pass

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
