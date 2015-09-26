"""
Procedurally generate map scenes.
"""

from random import randint
from random import choice
import random
import map_

MIN_SCENES = 10
MAX_SCENES = 15
GRID_SIZE = 9 # scenes created in virtual grid of size GRID_SIZE x GRID_SIZE
ID_SEQ = 1 # part of name for generated scenes
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
    a_map = map_.Map('story') # first scene is 'story'

    generate_scenes(a_map)
    a_map.print_map()

    # add special scenes
    a_map.add_scene('story', map_.Story(a_map.characters))
    a_map.add_scene('death', map_.Death(a_map.characters))
    a_map.add_scene('win', map_.Win(a_map.characters))
    a_map.add_scene('quit', map_.Quit(a_map.characters))
    return a_map


def generate_scenes(a_map):
    """ Creates a predefined number of scenes."""
    scenes = {} # list of created scenes with empty adjacent locations

    # pick a starting location for entrance scene
    x = randint(1, GRID_SIZE)
    y = randint(1, GRID_SIZE)

    # add entrance scene to list of created scenes
    scenes[(x, y)] = new_scene(a_map, 'entrance')

    # randomly calculate number of total scenes
    n = randint(MIN_SCENES, MAX_SCENES)
    added = 1 # number of scenes added

    while added < n:
        # pick an existing scene as a reference location
        print "scenes: {}.".format(scenes)
        ref_loc, sc = choice(scenes.items())
        # pick an empty adjacent location for the new scene
        x, y = empty_adjacent(ref_loc, scenes)
        # create a new scene at the empty location found above
        if (x, y) != (0, 0):
            new_sc = new_scene(a_map, 'random')
            scenes[(x, y)] = new_sc
            a_map.add_scene(new_sc.name, new_sc)
            added += 1
        else: # we cannot add any more adjacent scenes to the ref location
            scenes.pop(ref_loc)


def empty_adjacent(ref_loc, scenes):
    """ 
    Return an empty adjacent location to the reference location.

    ref_loc: reference location on the grid
    scenes: list of existing scenes
    """
    # generate list of all possible adjacent locations
    locations = [] # array of (x, y) tuples
    ref_x, ref_y = ref_loc
    for new_x in range(ref_x - 1, ref_x + 2):
        for new_y in range(ref_y - 1, ref_x + 2):
            new_loc = (new_x, new_y)
            if (new_x, new_y) != ref_loc and valid_location(new_loc):
                locations.append(new_loc)
    # while there are still locations with possible free adjacent locations
    while locations:
        # pick a location at random and check if it's already occupied
        loc = choice(locations)
        # if not occupied, return this location
        if loc not in scenes:
            return loc
        # if occupied, remove this location and pick another
        else:
            locations.remove(loc)
    # if all adjacent locations occupied, return (0, 0)
    return (0, 0)


def valid_location(location):
    """ Determine if a location is valid based on grid size."""
    x, y = location
    if x < 1 or x > GRID_SIZE or y < 1 or y > GRID_SIZE:
        return False
    else:
        return True


def new_scene(a_map, scene_type):
    """ Create a new scene and fill it with details."""
    scene = map_.Scene(a_map.characters)

    scene.name = make_name(scene_type)
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


def make_name(scene_type):
    """ Return an appropriate scene name."""
    global ID_SEQ
    if scene_type == 'entrance':
        name = 'entrance'
    elif scene_type == 'random':
        name = "random{}".format(ID_SEQ)
        ID_SEQ += 1
    elif scene_type == 'exit':
        name = "exit{}".format(ID_SEQ)
        ID_SEQ += 1
    else:
        pass
    return name
        

def update_exits(a_map):
    """ Update description of exits in all scenes in the map."""
    for scene in a_map.scenes.values():
        scene.description += "The path leads towards {}".format(
                                                            scene.exits.keys())


def link_scene(a_map, scene):
    """ Creates links (exits) between the new scene and existing scenes."""
    if a_map.scenes: # at least one existing scene
        # construct list of existing scenes to be potentially linked
        scene_list = a_map.scenes.values()
        # at the beginning, we can use any exit of the new scene
        scene_unused_exits = list(EXITS) # make a copy

        # link new scene with 1-3 different scenes
        n = randint(1, 3)
        linked = 0 # number of scenes successfully linked
        # while less than the desired links and there are more scenes to link
        while linked < n and scene_list:
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
                        linked += 1
                        scene_list.remove(s1)
                        break
                    else: # the opposite exit isn't available in the new scene
                        # remove the original exit from potential exits
                        s1.unused_exits.remove(s1_exit)
    else: # this is the first scene, no need to add exits
        pass
