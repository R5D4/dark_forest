""" Tests for the map_ module."""

import map_
import map_gen
from nose.tools import *


def update_encounter_test():
    # Scene class.
    # Test if encounter chance is calculated as desired.

    a_map = map_.Map('story')
    sc = map_.Scene(None)
    sc.features['wallow'] = 'large' # +10
    a_map.add_scene(sc)
    map_gen.add_description(a_map)

    a_map.clock.time = 22 # night1 (+3)
    # chance = 10 + 3 + 1 = 14
    ok_(sc.update_encounter() == 14)
