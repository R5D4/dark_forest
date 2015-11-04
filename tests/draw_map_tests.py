"""
Test function in draw_map.py
"""

from nose.tools import *
import draw_map
import map_
import map_gen


def prepare_canvas_test():
    # Test if links are drawn properly

    ### Simple test ###
    a_map = map_.Map('story')
    # create scenes with location data
    s1 = map_gen.new_scene(a_map, None, (1, 1))
    s2 = map_gen.new_scene(a_map, None, (2, 1))
    s3 = map_gen.new_scene(a_map, None, (1, 2))
    s4 = map_gen.new_scene(a_map, None, (2, 2))
    # set scene names
    s1.name = 'scene1'
    s2.name = 'scene2'
    s3.name = 'scene3'
    s4.name = 'scene4'
    # update exits
    s1.exits.update({'se': 'scene4'})
    s4.exits.update({'nw': 'scene1'})
    s2.exits.update({'sw': 'scene3'})
    s3.exits.update({'ne': 'scene2'})
    # add scenes to map
    a_map.add_scene(s1)
    a_map.add_scene(s2)
    a_map.add_scene(s3)
    a_map.add_scene(s4)
    # prepare canvas
    canvas = draw_map.prepare_canvas(a_map, (1, 1))
    #draw_map.print_canvas(canvas)
    # tests
    ok_(canvas[1][1] == 'X')

    ### Complete automated tests on procedurally generated maps ###
    for x in range(1, 101):
        a_map = map_gen.new_map()
        # prepare canvas
        canvas = draw_map.prepare_canvas(a_map, None)
        draw_map.print_canvas(canvas)
        # for each scene
        for sc in a_map.scenes.values():
            # for each exit
            for ex in sc.exits.keys():
                # calculate canvas position of the link
                canvas_x, canvas_y = draw_map.get_canvas_link_location(
                                                                sc.location,
                                                                ex)
                # check if link is the correct symbol
                print "{}: {}".format(sc.location, sc.exits)
                ok_(canvas[canvas_x][canvas_y] == draw_map.SYMBOL_LINK[ex] or \
                    canvas[canvas_x][canvas_y] == 'X')


def draw_map_test():
    ## Case 1
    a_map = map_.Map('story')

    # scene1
    s1 = map_gen.new_scene(a_map, None, (2, 1))
    s1.name = 'scene1'
    s1.exits.update({'s': 'scene2', 
                     'e': 'scene3',
                     'se': 'scene4'})
    a_map.add_scene(s1)
    # scene2
    s2 = map_gen.new_scene(a_map, None, (2, 2))
    s2.name = 'scene2'
    s2.exits.update({'n': 'scene1',
                     'ne': 'scene3'})
    a_map.add_scene(s2)
    # scene3
    s3 = map_gen.new_scene(a_map, None, (3, 1))
    s3.name = 'scene3'
    s3.exits.update({'w': 'scene1',
                     'sw': 'scene2'})
    a_map.add_scene(s3)
    # scene4
    s4 = map_gen.new_scene(a_map, None, (3, 2))
    s4.name = 'scene4'
    s4.exits.update({'nw': 'scene1'})
    a_map.add_scene(s4)

    canvas = draw_map.prepare_canvas(a_map, (2, 1))
    draw_map.print_canvas(canvas)

    ok_(canvas[2][0] == 'P') 
    ok_(canvas[2][2] == '#') 
    ok_(canvas[4][0] == '#') 
    ok_(canvas[4][2] == '#') 
    ok_(canvas[2][1] == '|') 
    ok_(canvas[3][0] == '-') 
    ok_(canvas[3][1] == 'X') 


def get_canvas_scene_location_test():
    # first row, any column
    ok_(draw_map.get_canvas_scene_location((1, 1)) == (0, 0))
    ok_(draw_map.get_canvas_scene_location((1, 2)) == (0, 2))
    ok_(draw_map.get_canvas_scene_location((1, 3)) == (0, 4))
    # any rows, first column
    ok_(draw_map.get_canvas_scene_location((1, 1)) == (0, 0))
    ok_(draw_map.get_canvas_scene_location((2, 1)) == (2, 0))
    ok_(draw_map.get_canvas_scene_location((3, 1)) == (4, 0))
    # any row, any column
    ok_(draw_map.get_canvas_scene_location((2, 2)) == (2, 2))
    ok_(draw_map.get_canvas_scene_location((2, 3)) == (2, 4))
    ok_(draw_map.get_canvas_scene_location((3, 3)) == (4, 4))
    

def get_canvas_link_location_test():
    # n
    ok_(draw_map.get_canvas_link_location((1, 2), 'n') == (0, 1))
    ok_(draw_map.get_canvas_link_location((2, 3), 'n') == (2, 3))
    # ne
    ok_(draw_map.get_canvas_link_location((2, 2), 'ne') == (3, 1))
    ok_(draw_map.get_canvas_link_location((1, 3), 'ne') == (1, 3))
    # e
    ok_(draw_map.get_canvas_link_location((2, 1), 'e') == (3, 0))
    ok_(draw_map.get_canvas_link_location((2, 3), 'e') == (3, 4))
    # se
    ok_(draw_map.get_canvas_link_location((2, 1), 'se') == (3, 1))
    ok_(draw_map.get_canvas_link_location((1, 2), 'se') == (1, 3))
    # s
    ok_(draw_map.get_canvas_link_location((2, 1), 's') == (2, 1))
    ok_(draw_map.get_canvas_link_location((1, 2), 's') == (0, 3))
    # sw
    ok_(draw_map.get_canvas_link_location((2, 1), 'sw') == (1, 1))
    ok_(draw_map.get_canvas_link_location((2, 2), 'sw') == (1, 3))
    # w
    ok_(draw_map.get_canvas_link_location((2, 1), 'w') == (1, 0))
    ok_(draw_map.get_canvas_link_location((3, 2), 'w') == (3, 2))
    # nw
    ok_(draw_map.get_canvas_link_location((2, 2), 'nw') == (1, 1))
    ok_(draw_map.get_canvas_link_location((3, 3), 'nw') == (3, 3))
