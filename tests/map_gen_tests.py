"""
Tests functions is map_gen.py
"""

from nose.tools import *
from random import randint
from random import choice
import map_gen
import map_


def empty_adjacent_test():
    for x in range(1, 101):
        loc = (randint(1, 9), randint(1, 9))
        scenes = {}
        scenes[loc] = "This is a test scene."
        adj_loc = map_gen.empty_adjacent(loc, scenes)
        print "loc = {}, adj_loc = {}".format(loc, adj_loc)
        
        ok_(loc != adj_loc)
        x, y = loc
        new_x, new_y = adj_loc
        ok_(abs(x - new_x) <= 1 and abs(y - new_y) <= 1)


def valid_location_test():
    gs = map_gen.GRID_SIZE
    print "Grid size is {} x {}".format(gs, gs)
    # success test cases
    for x in range(1, 101):
        loc = (randint(1, gs), randint(1, gs))
        print "Location is {}".format(loc)
        ok_(map_gen.valid_location(loc) is True)
    # failure test cases
    loc = (0, randint(1, gs))
    ok_(map_gen.valid_location(loc) is False)
    loc = (randint(1, gs), 0)
    ok_(map_gen.valid_location(loc) is False)
    loc = (gs+1, randint(1, gs))
    ok_(map_gen.valid_location(loc) is False)
    loc = (randint(1, gs), gs+1)
    ok_(map_gen.valid_location(loc) is False)


def generate_scenes_test():
    for x in range(1, 101):
        a_map = map_.Map('story')
        map_gen.ID_SEQ = 1
        map_gen.generate_scenes(a_map)
        scene_dict = map_gen.create_scene_dict(a_map)
        # for each scene s in a_map.scenes
        for s in a_map.scenes.values():
            # create list of all adjacent locations to s
            adj_list = all_adjacent(s.location)
            linked = False
            # test if there is at least one adjacent scene to s
            for adj_loc in adj_list:
                if adj_loc in scene_dict:
                    linked = True
                else:
                    pass
            ok_(linked is True, "Unconnected scene at {}: {}".format(
                s.location, 
                scene_dict))
    

def adjacent_scenes_test():
    a_map = map_.Map('story')
    location = (5, 5)

    # one adjacent scene
    scene_dict = {
                 (5, 5): map_gen.new_scene(a_map, 'entrance', (5, 5)),
                 (4, 6): map_gen.new_scene(a_map, 'scene1', (4, 6)),
                 }
    adj_scenes = map_gen.adjacent_scenes(scene_dict, location)
    print adj_scenes
    ok_(scene_dict[(4, 6)] in adj_scenes)

    # two adjacent scenes
    scene_dict[(6, 5)] = map_gen.new_scene(a_map, 'scene2', (6, 5)), 
    adj_scenes = map_gen.adjacent_scenes(scene_dict, location)
    print adj_scenes
    ok_(scene_dict[(4, 6)] in adj_scenes)
    ok_(scene_dict[(6, 5)] in adj_scenes)

    # three adjacent scenes
    scene_dict[(6, 6)] = map_gen.new_scene(a_map, 'scene3', (6, 6)), 
    adj_scenes = map_gen.adjacent_scenes(scene_dict, location)
    print adj_scenes
    ok_(scene_dict[(4, 6)] in adj_scenes)
    ok_(scene_dict[(6, 5)] in adj_scenes)
    ok_(scene_dict[(6, 6)] in adj_scenes)


########## HELPER FUNCTIONS ##########

def all_adjacent(ref_loc):
    """ Returns a list of all adjacent locations to ref_loc."""
    # generate list of all possible adjacent locations
    locations = [] # array of (x, y) tuples
    ref_x, ref_y = ref_loc
    for new_x in range(ref_x - 1, ref_x + 2):
        for new_y in range(ref_y - 1, ref_y + 2):
            new_loc = (new_x, new_y)
            if (new_x, new_y) != ref_loc and map_gen.valid_location(new_loc):
                locations.append(new_loc)
    return locations

