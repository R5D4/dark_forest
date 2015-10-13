"""
Tests functions in map_gen.py
"""

from nose.tools import *
from random import randint
from random import choice
import map_gen
import map_


def add_landmark_test():
    # Test if a landmark is properly added to a scene
    for l_type in map_gen.LANDMARKS.keys():
        sc = map_.Scene(None)
        map_gen.add_landmark(sc, l_type)
        ok_(l_type in sc.features)
        ok_(sc.features[l_type] in map_gen.LANDMARKS[l_type])


def add_landmarks_test():
    a_map = map_.Map('story')
    map_gen.generate_scenes(a_map)
    map_gen.add_landmarks(a_map)
    
    # Test if correct number of landmarks added?
    # Test that no scene has more than one landmark
    for sc in a_map.scenes.values():
        count = 0
        for key in sc.features.keys():
            if key in map_gen.LANDMARKS:
                count +=1
        print "count: {}. features: {}".format(count, sc.features.items())
        ok_(count <= 1)
    

def add_features_test():
    # test if all types of environmental features are added
    a_map = map_.Map('story')
    for i in xrange(0, 100): # 100 trials
        scene = map_gen.new_scene(a_map, 'random', (1, 1))
        map_gen.add_features(scene)
        print scene.features
        ok_(scene.features['canopy'] in map_gen.CANOPY)
        ok_(scene.features['understory'] in map_gen.UNDERSTORY)
        ok_(scene.features['shrubs'] in map_gen.SHRUBS)
        ok_(scene.features['floor'] in map_gen.FLOOR)


def init_landmark_limits_test():
    # test if generated values are within limits
    n = 100
    for i in xrange(0, 100): # 100 trials
        limits = map_gen.init_landmark_limits(n)
        print limits
        ok_(limits['wallow'] >= 1 and limits['wallow'] <= 10)
        ok_(limits['rooting'] >= 2 and limits['rooting'] <= 20)
        ok_(limits['damaged_tree'] >= 0 and limits['damaged_tree'] <= 5)
        ok_(limits['dead_wood'] >= 1 and limits['dead_wood'] <= 5)
        ok_(limits['bed'] >= 1 and limits['bed'] <= 2)
        ok_(limits['track'] >= 5 and limits['track'] <= 20)


def add_links_test():
    # Test if map_gen.add_links function actually adds between 0 and 1 link
    # per scene.

    # two scenes, max two new links
    a_map = map_.Map('story')

    s1 = map_gen.new_scene(a_map, None, (5, 5))
    s1.name = 'scene1'
    a_map.add_scene(s1)
    s2 = map_gen.new_scene(a_map, None, (6, 5))
    s2.name = 'scene2'
    a_map.add_scene(s2)

    map_gen.add_links(a_map)
    ok_(count_links(a_map) <= 2)


    # three scenes, max three new links
    a_map = map_.Map('story')

    s1 = map_gen.new_scene(a_map, None, (5, 5))
    s1.name = 'scene1'
    a_map.add_scene(s1)
    s2 = map_gen.new_scene(a_map, None, (6, 5))
    s2.name = 'scene2'
    a_map.add_scene(s2)
    s3 = map_gen.new_scene(a_map, None, (4, 5))
    s3.name = 'scene3'
    a_map.add_scene(s3)

    map_gen.add_links(a_map)
    ok_(count_links(a_map) <= 3)

    # four scenes, max four new links
    a_map = map_.Map('story')

    s1 = map_gen.new_scene(a_map, None, (5, 5))
    s1.name = 'scene1'
    a_map.add_scene(s1)
    s2 = map_gen.new_scene(a_map, None, (6, 5))
    s2.name = 'scene2'
    a_map.add_scene(s2)
    s3 = map_gen.new_scene(a_map, None, (7, 5))
    s3.name = 'scene3'
    a_map.add_scene(s3)
    s4 = map_gen.new_scene(a_map, None, (8, 5))
    s4.name = 'scene4'
    a_map.add_scene(s4)

    map_gen.add_links(a_map)
    ok_(count_links(a_map) <= 4)


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


def DFS_test():
    # test for the helper function DFS
    a_map = map_.Map('story')

    s1 = map_gen.new_scene(a_map, None, (5, 5))
    s1.name = 'scene1'
    a_map.add_scene(s1)
    s2 = map_gen.new_scene(a_map, None, (6, 5))
    s2.name = 'scene2'
    a_map.add_scene(s2)
    map_gen.create_link(s1, s2)
    ok_(set(DFS(s1, a_map)) == set([s1, s2]))
    ok_(set(DFS(s2, a_map)) == set([s1, s2]))


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
    ok_(map_gen.link_direction(loc1, loc2) == 's')
    # north-east
    loc2 = (6, 6)
    ok_(map_gen.link_direction(loc1, loc2) == 'se')
    # east
    loc2 = (6, 5)
    ok_(map_gen.link_direction(loc1, loc2) == 'e')
    # south-east
    loc2 = (6, 4)
    ok_(map_gen.link_direction(loc1, loc2) == 'ne')
    # south
    loc2 = (5, 4)
    ok_(map_gen.link_direction(loc1, loc2) == 'n')
    # south-west
    loc2 = (4, 4)
    ok_(map_gen.link_direction(loc1, loc2) == 'nw')
    # west
    loc2 = (4, 5)
    ok_(map_gen.link_direction(loc1, loc2) == 'w')
    # north-west
    loc2 = (4, 6)
    ok_(map_gen.link_direction(loc1, loc2) == 'sw')
    

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
    s1.exits['s'] = 'scene3'
    s3.exits['n'] = 'scene1'
    ok_(map_gen.has_link(s1, s3) is True)
    ok_(map_gen.has_link(s3, s1) is True)

    # case 3: nw-se link
    s4 = map_gen.new_scene(a_map, 'scene4', (4, 6))
    s4.name = 'scene4'
    s1.exits['sw'] = 'scene4'
    s4.exits['ne'] = 'scene1'
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
    ok_(s1.exits['s'] == 'scene3')
    ok_(s3.exits['n'] == 'scene1')
    # nw-se
    s4 = map_gen.new_scene(a_map, None, (4, 6))
    s4.name = 'scene4'
    map_gen.create_link(s1, s4)
    ok_(s1.exits['sw'] == 'scene4')
    ok_(s4.exits['ne'] == 'scene1')
    # ne-sw
    s5 = map_gen.new_scene(a_map, None, (6, 6))
    s5.name = 'scene5'
    map_gen.create_link(s1, s5)
    ok_(s1.exits['se'] == 'scene5')
    ok_(s5.exits['nw'] == 'scene1')


def generate_scenes_test():
    # 100 trials
    for x in range(1, 101):
        a_map = map_.Map('story')
        map_gen.ID_SEQ = 1
        map_gen.generate_scenes(a_map)
        scene_dict = map_gen.create_scene_dict(a_map)

        # Test if any scenes overlap in location
        so_far = []
        for sc in a_map.scenes.values():
            ok_(sc.location not in so_far)
            so_far.append(sc.location)

        # Test if enough links are added for a connected map
        ok_(count_links(a_map) == len(a_map.scenes.values())-1)

        # Test if every generated scene is adjacent to at least one other scene
        for s in a_map.scenes.values():
            # create list of all adjacent locations to s
            adj_list = map_gen.all_adjacent(s.location)
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

        # Test for map connectedness
        ok_(check_map_connectedness(a_map))

        # Test if each scene is well-formed (features, landmarks)
        # NOTE: Implement this


########## HELPER FUNCTIONS ##########

def check_map_connectedness(a_map):
    """ 
    Check if the map represents a connected graph.

    Only use for maps created by map_gen.generate_scenes, as it will be a tree.
    Maps generated using map_gen.new_map has loops due to extra links added.
    """
    # Check if every scene is accessible using DFS search 
    # Successful DFS traversal from any scene proves connectedness since
    # links are bidirectional
    sc = choice(a_map.scenes.values())
    # Get list of visited scenes using DFS traversal
    visited = DFS(sc, a_map)
    # test if list of visited scenes contains all the scenes in the map 
    return set(visited) == set(a_map.scenes.values())


def DFS(start_scene, a_map):
    """
    Return list of visited scenes using iterative Depth-First traversal.
    """
    visited = []
    stack = [(None, start_scene)] # (parent, node)
    while stack: # not empty
        #print_stack(stack)
        #print_visited(visited)
        parent, scene = stack.pop()
        visited.append(scene)
        # get list of children 
        children = [ a_map.scenes[name] for name in scene.exits.values() ]
        if parent in children: # not None
            children.remove(parent)
        for child in children:
            stack.append((scene, child))
    return visited


def print_stack(stack):
    """ Prints the stack nicely to debug DFS."""
    raw_input('------------------------------')
    for parent, scene in stack:
        if parent is not None:
            p_name = parent.name
        else:
            p_name = None
        print "P: {}, Scene: {}, Location: {}".format(p_name,
                                                      scene.name,
                                                      scene.location)

def print_visited(visited):
    """ Prints list of visited scenes during DFS traversal."""
    for sc in visited:
        print "Name: {}, Location: {}".format(sc.name, sc.location)


def count_links(a_map):
    """ Return the total number of links in the map."""
    # number of links =  sum of the number of exits in each scene / 2
    return sum([ len(sc.exits) for sc in a_map.scenes.values() ]) / 2 

