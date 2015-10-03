"""
Test function in draw_map.py
"""

from nose.tools import *
import draw_map
import map_
import map_gen


def draw_map_test():
    ## Case 1
    a_map = map_.Map('story')

    # scene1
    s1 = map_gen.new_scene(a_map, None, (2, 1))
    s1.name = 'scene1'
    s1.exits.update({'s': 'scene2', 
                     'e': 'scene3',
                     'se': 'scene4'})
    a_map.add_scene(s1.name, s1)
    # scene2
    s2 = map_gen.new_scene(a_map, None, (2, 2))
    s2.name = 'scene2'
    s2.exits.update({'n': 'scene1',
                     'ne': 'scene3'})
    a_map.add_scene(s2.name, s2)
    # scene3
    s3 = map_gen.new_scene(a_map, None, (3, 1))
    s3.name = 'scene3'
    s3.exits.update({'w': 'scene1',
                     'sw': 'scene2'})
    a_map.add_scene(s3.name, s3)
    # scene4
    s4 = map_gen.new_scene(a_map, None, (3, 2))
    s4.name = 'scene4'
    s4.exits.update({'nw': 'scene1'})
    a_map.add_scene(s4.name, s4)

    canvas = draw_map.prepare_canvas(a_map)

    ok_(canvas[2][0] == '#') 
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
