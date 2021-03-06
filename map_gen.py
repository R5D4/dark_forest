"""
Procedurally generate map scenes.

Map location arranged as follows:
                x
        1   2   3   4   ...
    1
    2
y   3
    4
    .
    .
    .
Location tuple is (x, y)
"""

from random import randint
from random import choice
from random import shuffle
import random
import map_
import items

########## GLOBAL THINGIES ##########

## Settings
MIN_SCENES = 30 # recommend > 10
MAX_SCENES = 50 # hard limit is GRID_SIZE^2, recommend less
GRID_SIZE = 9 # scenes created in virtual grid of size GRID_SIZE x GRID_SIZE

## Counts and sequence numbers
ID_SEQ = 1 # part of name for generated scenes

## Data constants
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
# features
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
    add_lair(a_map)
    add_item_stashes(a_map)
    add_links(a_map) # add additional links
    add_all_desc(a_map)
    spawn_boss(a_map) # spawn the boss on the map

    # add special scenes
    a_map.add_special_scene('story', map_.Story(a_map.characters))
    a_map.add_special_scene('death', map_.Death(a_map.characters))
    a_map.add_special_scene('win', map_.Win(a_map.characters))
    a_map.add_special_scene('timeup', map_.TimeUp(a_map.characters))
    return a_map


########## HELPER FUNCTIONS ##########

def generate_scenes(a_map):
    """ 
    Generate scenes for the new map.
    
    Add between MIN_SCENES and MAX_SCENES number of scenes to the map.
    Link the created scene such that there is a path between each pair of
        scenes.
    Each scene has a name, location, and exits created in the linking stage.
    """
    candidate_scenes = [] # list of scenes with empty adjacent locations
    occupied_locs = [] # list of occupied locations
    n = randint(MIN_SCENES, MAX_SCENES)

    # pick a starting location for entrance scene
    loc = (randint(1, GRID_SIZE), randint(1, GRID_SIZE))

    # create a new scene at the starting location
    new_sc = new_scene(a_map, 'entrance', loc)
    add_flora(new_sc)
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
            add_flora(new_sc)
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
    """ 
    Create a new scene in a_map at location.
    
    Set scene name depending on scene type.
    """
    scene = map_.Scene(a_map.characters)
    scene.name = make_name(scene_type)
    scene.location = location
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
        

def add_flora(scene):
    """ Add flora for each vertical stratum in a scene."""
    new_stratum = map_.Stratum('canopy', random.choice(CANOPY))
    scene.features.append(new_stratum)
    new_stratum = map_.Stratum('understory', random.choice(UNDERSTORY))
    scene.features.append(new_stratum)
    new_stratum = map_.Stratum('shrubs', random.choice(SHRUBS))
    scene.features.append(new_stratum)
    new_stratum = map_.Stratum('floor', random.choice(FLOOR))
    scene.features.append(new_stratum)


def add_lair(a_map):
    """ Add one boss lair to the map."""
    # pick a random scene from the map
    scene = choice(a_map.scenes.values())
    lair = map_.Lair()
    scene.features.append(lair)
    # add lair's scene name to the map
    a_map.lair_scene_name = scene.name


def add_item_stashes(a_map):
    """ Add item stashes to the map. One per scene."""
    goal = get_item_stash_goal(len(a_map.scenes))
    candidates = a_map.scenes.values()
    count = 0
    # loop until we've reached our goal or no more scenes
    while count < goal and candidates:
        # pick random scene from map
        sc = choice(candidates)
        # add the item stash to the scene
        add_item_stash(sc)
        # remove scene from list (one item stash/scene)
        candidates.remove(sc)
        # increment count
        count += 1


def get_item_stash_goal(n):
    """ 
    Return number of desired items stashes in map
    
    n: number of scenes
    """
    base = 3 # minimum 3 item stash on map
    rand_goal = randint(0, int(0.15 * n)) # up to 15% of total number of scenes
    # rand_goal = n # for testing, one item stash in every scene
    limit = max(base, rand_goal)
    return limit


def add_item_stash(scene):
    """ Add an item stash to a scene."""
    # Create pool of items to choose from
    # 1. Take 2 weapons, put in pool
    pool = []
    for i in range(2):
        pool.append(items.new_weapon())
    # 2. Take 1 armor, put in pool
    for i in range(1):
        pool.append(items.new_armor())
    # 3. Randomly pick 1-2 items from pool
    shuffle(pool)
    final = []
    for i in range(randint(1, 2)):
        final.append(pool.pop())
    # Create item stash and add to scene
    stash = map_.ItemStash(final)
    scene.features.append(stash)


def add_all_desc(a_map):
    """ Construct a description for each scene in a_map."""
    for scene in a_map.scenes.values():
        add_description(scene)


def add_description(scene):
    """ Add description to a scene."""
    # Update description of features
    descriptions = []
    for f in scene.features:
        descriptions.append(f.get_desc()) 
    # Update description of exits
    descriptions.append("\nThe path leads towards {}".format(
                                                       scene.exits.keys()))
    scene.description = ' '.join(descriptions)


def spawn_boss(a_map):
    """ Spawn the boss in its lair."""
    sc_name = a_map.lair_scene_name
    a_map.boss_scene_name = sc_name
    sc = a_map.scenes[sc_name]
    # NOTE: uncomment to show boss spawn location on map, should be False
    sc.flags['encounter'] = True
    # put the boss in the lair
    lair = sc.get_lair()
    lair.has_boss = True


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


