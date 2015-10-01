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
    pass
