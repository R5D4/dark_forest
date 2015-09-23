"""
Procedurally generates map scenes.
"""

from random import randint
from random import choice
import random
import map_

ID_SEQ = 1
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
    link_scene(a_map, random_scene)
    a_map.add_scene(random_scene.name, random_scene)

    # add exit scenes

    update_exits(a_map)

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
    return scene


def link_scene(a_map, scene):
    """ Creates links (exits) between the new scene and existing scenes."""
    if a_map.scenes: # at least one existing scene
        # construct list of existing scenes to be potentially linked
        scene_list = a_map.scenes.values()
        # at the beginning, we can use any exit of the new scene
        scene_unused_exits = list(EXITS) # make a copy

        # link new scene with 1-3 different scenes
        n = randint(2, 4)
        #for i in range(1, n):
        # only link with 1 other scene - for testing
        for i in range(1, 2):
            # pick a scene from the scene list we made earlier
            s1 = choice(scene_list)
            # make a list of unused exits in the scene
            s1_unused_exits = list(set(EXITS).difference(s1.exits.keys()))

            # while there are still unused exits 
            while s1_unused_exits:
                # pick an unused exit in the scene
                s1_exit = choice(s1_unused_exits)
                # look up opposite exit
                scene_exit = OPPOSITE_EXITS[s1_exit]
                # if the opposite exit is unused in the new scene
                if scene_exit in scene_unused_exits:
                    # link the two scenes using their respective exits
                    s1.exits[s1_exit] = scene.name
                    scene.exits[scene_exit] = s1.name
                    break
                else: # the opposite exit isn't available in the new scene
                    # remove the original exit from potential exits
                    s1.unused_exits.remove(s1_exit)
    else:
        pass


def update_exits(a_map):
    """ Update description of exits in all scenes in the map."""
    for scene in a_map.scenes.values():
        scene.description += "The path leads towards {}".format(
                                                            scene.exits.keys())


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
