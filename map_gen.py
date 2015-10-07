"""
Procedurally generate map scenes.
"""

from random import randint
from random import choice
import random
import map_

########## GLOBAL THINGIES ##########

MIN_SCENES = 30
MAX_SCENES = 50
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
# location difference to link direction
DIFF_TO_DIR = {
              (-1, -1): 'nw',
              (-1, 0): 'w',
              (-1, 1): 'sw',
              (0, -1): 'n',
              (0, 0): None,
              (0, 1): 's',
              (1, -1): 'ne',
              (1, 0): 'e',
              (1, 1): 'se'
              }
# link direction to location difference
DIR_TO_DIFF = {
           'nw': (-1, -1),
           'w': (-1, 0),
           'sw': (-1, 1),
           'n': (0, -1),
           's': (0, 1),
           'ne': (1, -1),
           'e': (1, 0),
           'se': (1, 1)
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
    add_links(a_map)
    update_exits(a_map)

    # add special scenes
    a_map.add_special_scene('story', map_.Story(a_map.characters))
    a_map.add_special_scene('death', map_.Death(a_map.characters))
    a_map.add_special_scene('win', map_.Win(a_map.characters))
    a_map.add_special_scene('quit', map_.Quit(a_map.characters))
    return a_map


########## HELPER FUNCTIONS ##########

def generate_scenes(a_map):
    """ Generate scenes for the new map."""
    candidate_scenes = [] # list of scenes with empty adjacent locations
    occupied_locs = [] # list of occupied locations
    n = randint(MIN_SCENES, MAX_SCENES)

    # pick a starting location for entrance scene
    loc = (randint(1, GRID_SIZE), randint(1, GRID_SIZE))

    # create a new scene at the starting location
    new_sc = new_scene(a_map, 'entrance', loc)
    candidate_scenes.append(new_sc) 
    occupied_locs.append(loc)
    a_map.add_scene(new_sc)

    added = 1 # number of scenes added

    while added < n:
        # pick an existing scene as a reference location
        sc = choice(candidate_scenes)
        # pick an empty adjacent location for the new scene
        new_loc = empty_adjacent(sc.location, occupied_locs)
        # create a new scene at the empty location found above
        if new_loc: # not None
            new_sc = new_scene(a_map, 'random', new_loc)
            # add a link between the reference scene and the new scene
            # this ensures that the map is a connected graph
            create_link(new_sc, sc)
            candidate_scenes.append(new_sc)
            occupied_locs.append(new_loc)
            a_map.add_scene(new_sc)
            added += 1
        else: # we cannot add any more adjacent scenes to the ref location
            candidate_scenes.remove(sc)


def new_scene(a_map, scene_type, location):
    """ Create a new scene and fill it with details."""
    scene = map_.Scene(a_map.characters)

    scene.name = make_name(scene_type)
    scene.location = location
    scene.flags['encounter_chance'] = 0.5

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
        

def empty_adjacent(ref_loc, occupied_locs):
    """ 
    Return an empty adjacent location to the reference location.

    ref_loc: reference location on the grid
    occupied_locs: list of occupied locations
    """
    # generate list of all possible adjacent locations
    locations = all_adjacent(ref_loc)

    while locations:
        # pick a location at random and check if it's already occupied
        loc = choice(locations)
        # if not occupied, return this location
        if loc not in occupied_locs:
            return loc
        # if occupied, remove this location and pick another
        else:
            locations.remove(loc)
    # all adjacent locations occupied
    return None


def all_adjacent(ref_loc):
    """ Returns a list of all adjacent locations to ref_loc."""
    # generate list of all possible adjacent locations
    locations = [] # array of (x, y) tuples
    ref_x, ref_y = ref_loc
    for new_x in range(ref_x - 1, ref_x + 2):
        for new_y in range(ref_y - 1, ref_y + 2):
            new_loc = (new_x, new_y)
            if (new_x, new_y) != ref_loc and valid_location(new_loc):
                locations.append(new_loc)
    return locations


def add_links(a_map):
    """ Add additional links between scenes in the map.""" 
    # for each created scene, make 0-1 exit to other scenes if possible
    # create a dictionary of (x, y): Scene object items for easy search
    scene_dict = create_scene_dict(a_map)

    # for each scene s1 in a_map.scenes
    for s1 in a_map.scenes.values():
        # make a list S of all scenes in a_map.scenes adjacent to s1
        adj_scenes = adjacent_scenes(scene_dict, s1.location)
        # determine number of desired links to make from s1 (0 or 1)
        n = randint(0, 1)
        linked = 0
        # while we still need to make more links and there are adjacent scenes
        while linked < n and adj_scenes:
            # pick a scene s2 from S
            s2 = choice(adj_scenes)
            # check if there's already a link between s1 and s2
            if has_link(s1, s2):
                # if yes, remove s2 from S, continue
                adj_scenes.remove(s2)
            else:
                # else if no, make a link b/w s1 and s2 
                create_link(s1, s2)
                linked += 1
    

def create_scene_dict(a_map):
    """ Create dict with key=location, value=scene object."""
    scene_dict = {}
    for sc in a_map.scenes.values():
        scene_dict[sc.location] = sc
    return scene_dict


def adjacent_scenes(scene_dict, location):
    """
    Return a list of Scene objects that are adjacent to location.
    
    Contains scenes that are adjacent, not necessarily linked.
    """
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


def valid_location(location):
    """ Determine if a location is valid based on grid size."""
    x, y = location
    if x < 1 or x > GRID_SIZE or y < 1 or y > GRID_SIZE:
        return False
    else:
        return True


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


def link_direction(loc1, loc2):
    """ Return the direction of the exit from loc1 to loc2."""
    # not adjacent
    if not is_adjacent(loc1, loc2):
        return None
    x1, y1 = loc1
    x2, y2 = loc2
    diff = (x2 - x1, y2 - y1)
    return DIFF_TO_DIR[diff]


def is_adjacent(loc1, loc2):
    """ Determine if loc1 and loc2 are adjacent."""
    x1, y1 = loc1
    x2, y2 = loc2
    return abs(x1 - x2) <= 1 and abs(y1 - y2) <= 1


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


def update_exits(a_map):
    """ Update description of exits in all scenes in the map."""
    for scene in a_map.scenes.values():
        scene.description += "The path leads towards {}".format(
                                                            scene.exits.keys())

