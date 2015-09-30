"""
Procedurally generate map scenes.
"""

from random import randint
from random import choice
import random
import map_

########## GLOBAL THINGIES ##########

MIN_SCENES = 10
MAX_SCENES = 10
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


########## PUBLIC FUNCTION ##########

def new_map():
    """ Generates a new map with random scenes."""
    a_map = map_.Map('story') # first scene is 'story'
    global ID_SEQ 
    ID_SEQ = 1 # reset sequence number for new map

    generate_scenes(a_map)
    link_scenes(a_map)
    a_map.print_map()
    update_exits(a_map)

    # add special scenes
    a_map.add_scene('story', map_.Story(a_map.characters))
    a_map.add_scene('death', map_.Death(a_map.characters))
    a_map.add_scene('win', map_.Win(a_map.characters))
    a_map.add_scene('quit', map_.Quit(a_map.characters))
    return a_map


########## HELPER FUNCTIONS ##########

def generate_scenes(a_map):
    """ Creates a predefined number of scenes."""
    scenes = {} # list of created scenes with empty adjacent locations
    n = randint(MIN_SCENES, MAX_SCENES)

    # pick a starting location for entrance scene
    x = randint(1, GRID_SIZE)
    y = randint(1, GRID_SIZE)

    # add entrance scene to list of created scenes
    new_sc = new_scene(a_map, 'entrance', (x, y))
    scenes[(x, y)] = new_sc
    a_map.add_scene(new_sc.name, new_sc)

    # randomly calculate number of total scenes
    added = 1 # number of scenes added

    while added < n:
        # pick an existing scene as a reference location
        ref_loc, sc = choice(scenes.items())
        # pick an empty adjacent location for the new scene
        x, y = empty_adjacent(ref_loc, scenes)
        # create a new scene at the empty location found above
        if (x, y) != (0, 0):
            new_sc = new_scene(a_map, 'random', (x, y))
            scenes[(x, y)] = new_sc
            a_map.add_scene(new_sc.name, new_sc)
            added += 1
        else: # we cannot add any more adjacent scenes to the ref location
            scenes.pop(ref_loc)


def link_scenes(a_map):
    """ Randomly create exits between scenes."""
    # for each created scene, make 1-2 exits to other scenes if possible
    # create a dictionary of (x, y): Scene object items for easy search
    scene_dict = create_scene_dict(a_map)

    # for each scene s1 in a_map.scenes
    for s1 in a_map.scenes.values():
        # make a list S of all scenes in a_map.scenes adjacent to s1
        adjacent_scenes = adjacent_scenes(scene_dict, s1.location)
        # determine number of desired links to make from s1 (1 or 2)
        n = randint(1, 2)
        linked = 0
        # while we still need to make more links and there are adjacent scenes
        while linked < n and adjacent_scenes:
            # pick a scene s2 from S
            s2 = choice(adjacent_scenes)
            # check if there's already a link between s1 and s2
            if has_link(s1, s2):
                # if yes, remove s2 from S, continue
                adjacent_scenes.remove(s2)
            else:
                # else if no, make a link b/w s1 and s2 
                create_link(s1, s2)
                link += 1
    

def create_scene_dict(a_map):
    """ Create dict with key=location, value=scene object."""
    scene_dict = {}
    for sc in a_map.scenes.values():
        scene_dict[sc.location] = sc
    return scene_dict


def adjacent_scenes(scene_dict, location):
    """ Return a list S of Scene objects that are adjacent to location."""
    # loop through all 9 possible locations centered at the given location
    adjacent_scenes = []
    s1_x, s1_y = location
    for new_x in range(s1_x - 1, s1_x + 2):
        for new_y in range(s1_y - 1, s1_y + 2):
            new_loc = (new_x, new_y)
            if new_loc != location and valid_location(new_loc):
                # if there is a scene from scene_dict in that location
                if new_loc in scene_dict:
                    # add the scene to S
                    adjacent_scenes.append(scene_dict[new_loc])
                else: # if there's no scene in that location
                    pass
    return adjacent_scenes


def link_direction(loc1, loc2):
    """ Return the direction of the exit from loc1 to loc2."""
    x1, y1 = loc1
    x2, y2 = loc2
    # not adjacent
    if not is_adjacent(loc1, loc2):
        return None

    direction = ''
    if x2 < x1:
        if y2 < y1:
            direction = 'sw'
        elif y2 == y1:
            direction = 'w'
        elif y2 > y1:
            direction = 'nw'
    elif x2 == x1:
        if y2 < y1:
            direction = 's'
        elif y2 == y1:
            # loc1 == loc2, shouldn't happen
            direction = None
        elif y2 > y1:
            direction = 'n'
    elif x2 > x1:
        if y2 < y1:
            direction = 'se'
        elif y2 == y1:
            direction = 'e'
        elif y2 > y1:
            direction = 'ne'
    return direction


def is_adjacent(loc1, loc2):
    """ Determine if loc1 and loc2 are adjacent."""
    x1, y1 = loc1
    x2, y2 = loc2
    return abs(x1 - x2) <= 1 and abs(y1 - y2) <= 1


def has_link(s1, s2):
    """ Return True if proper link b/w s1 and s2. Else false."""
    # determine link directions
    dir1 = link_direction(s1.location, s2.location)
    dir2 = link_direction(s2.location, s1.location)
    # check if links exist
    if dir1 in s1.exits and dir2 in s2.exits:
        # check if link in proper direction
        if s1.exits[dir1] == s2.name and s2.exits[dir2] == s1.name:
            return True
    return False


def create_link(s1, s2):
    """ Create a exit link between s1 and s2 based on relative position."""
    # determine direction of s1's exit to s2
    dir1 = link_direction(s1.location, s2.location)
    # add s2 as the destination of s1's exit
    s1.exits[dir1] = s2.name
    # determine direction of s2's exit to s1
    dir2 = OPPOSITE_EXITS[dir1]
    # add s1 as the destination of s2's exit
    s2.exits[dir2] = s1.name


def empty_adjacent(ref_loc, scenes):
    """ 
    Return an empty adjacent location to the reference location.

    ref_loc: reference location on the grid
    scenes: list of existing scenes
    """
    # generate list of all possible adjacent locations
    locations = [] # array of (x, y) tuples
    ref_x, ref_y = ref_loc
    #print "ref_loc = {}".format(ref_loc)
    for new_x in range(ref_x - 1, ref_x + 2):
        for new_y in range(ref_y - 1, ref_y + 2):
            new_loc = (new_x, new_y)
            #print "new_loc = {}".format(new_loc)
            if (new_x, new_y) != ref_loc and valid_location(new_loc):
                locations.append(new_loc)
    # while there are still locations with possible free adjacent locations
    #print "locations = {}".format(locations)
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


def new_scene(a_map, scene_type, location):
    """ Create a new scene and fill it with details."""
    scene = map_.Scene(a_map.characters)

    scene.name = make_name(scene_type)
    scene.location = location
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
        name = None
    return name
        

def update_exits(a_map):
    """ Update description of exits in all scenes in the map."""
    for scene in a_map.scenes.values():
        scene.description += "The path leads towards {}".format(
                                                            scene.exits.keys())

