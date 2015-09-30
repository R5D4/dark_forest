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


def link_direction_test():
    loc1 = (5, 5)
    # north
    loc2 = (5, 6)
    ok_(map_gen.link_direction(loc1, loc2) == 'n')
    # north-east
    loc2 = (6, 6)
    ok_(map_gen.link_direction(loc1, loc2) == 'ne')
    # east
    loc2 = (6, 5)
    ok_(map_gen.link_direction(loc1, loc2) == 'e')
    # south-east
    loc2 = (6, 4)
    ok_(map_gen.link_direction(loc1, loc2) == 'se')
    # south
    loc2 = (5, 4)
    ok_(map_gen.link_direction(loc1, loc2) == 's')
    # south-west
    loc2 = (4, 4)
    ok_(map_gen.link_direction(loc1, loc2) == 'sw')
    # west
    loc2 = (4, 5)
    ok_(map_gen.link_direction(loc1, loc2) == 'w')
    # north-west
    loc2 = (4, 6)
    ok_(map_gen.link_direction(loc1, loc2) == 'nw')
    

def has_link_test():
    a_map = map_.Map('story')

    # case 1: east-west link
    s1 = map_gen.new_scene(a_map, 'scene1', (5, 5))
    s1.name = 'scene1'
    s2 = map_gen.new_scene(a_map, 'scene2', (6, 5))
    s2.name = 'scene2'
    s1.exits['e'] = 'scene2'
    s2.exits['w'] = 'scene1'
    ok_(map_gen.has_link(s1, s2) is True)
    ok_(map_gen.has_link(s2, s1) is True)

    # case 2: north-south link
    s3 = map_gen.new_scene(a_map, 'scene3', (5, 6))
    s3.name = 'scene3'
    s1.exits['n'] = 'scene3'
    s3.exits['s'] = 'scene1'
    ok_(map_gen.has_link(s1, s3) is True)
    ok_(map_gen.has_link(s3, s1) is True)

    # case 3: nw-se link
    s4 = map_gen.new_scene(a_map, 'scene4', (4, 6))
    s4.name = 'scene4'
    s1.exits['nw'] = 'scene4'
    s4.exits['se'] = 'scene1'
    ok_(map_gen.has_link(s1, s4) is True)
    ok_(map_gen.has_link(s4, s1) is True)

    # case 4: not adjacent (and therefore cannot be linked)
    s5 = map_gen.new_scene(a_map, 'scene5', (9, 9))
    s5.name = 'scene5'
    ok_(map_gen.has_link(s1, s5) is False)
    ok_(map_gen.has_link(s5, s1) is False)
    
    # case 5: adjacent (ne-sw) but no links
    s6 = map_gen.new_scene(a_map, 'scene6', (6, 6))
    s6.name = 'scene6'
    ok_(map_gen.has_link(s1, s6) is False)
    ok_(map_gen.has_link(s6, s1) is False)
    

def create_link_test():
    a_map = map_.Map('story')
    # east-west
    s1 = map_gen.new_scene(a_map, None, (5, 5))
    s1.name = 'scene1'
    s2 = map_gen.new_scene(a_map, None, (6, 5))
    s2.name = 'scene2'
    map_gen.create_link(s1, s2)
    ok_(s1.exits['e'] == 'scene2')
    ok_(s2.exits['w'] == 'scene1')
    # north-south
    s3 = map_gen.new_scene(a_map, None, (5, 6))
    s3.name = 'scene3'
    map_gen.create_link(s1, s3)
    ok_(s1.exits['n'] == 'scene3')
    ok_(s3.exits['s'] == 'scene1')
    # nw-se
    s4 = map_gen.new_scene(a_map, None, (4, 6))
    s4.name = 'scene4'
    map_gen.create_link(s1, s4)
    ok_(s1.exits['nw'] == 'scene4')
    ok_(s4.exits['se'] == 'scene1')
    # ne-sw
    s5 = map_gen.new_scene(a_map, None, (6, 6))
    s5.name = 'scene5'
    map_gen.create_link(s1, s5)
    ok_(s1.exits['ne'] == 'scene5')
    ok_(s5.exits['sw'] == 'scene1')



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

