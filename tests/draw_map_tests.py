"""
Test function in draw_map.py
"""

from nose.tools import *
import draw_map


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
