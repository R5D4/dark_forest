"""
Draw the map with ASCII characters.
"""

import map_gen

SYMBOL_SCENE = '#'
SYMBOL_LINK = {
                'n': '|',
                'ne': '/',
                'e': '-',
                'se': '\\',
                's': '|',
                'sw': '/',
                'w': '-',
                'nw': '\\'
              }


def draw_map(a_map):
    """ Draw the map with ASCII characters."""
    # create empty canvas (max grid of scenes and links)
    canvas = [ [] for i in xrange(2*map_gen.GRID_SIZE - 1) ]
    # for each scene in the map
    for s1 in a_map.scenes.values():
        # determine canvas location of x and y
        x, y = get_canvas_scene_location(s1.location)
        # add '#' to canvas at new location
        canvas[x][y] = SYMBOL_SCENE
        # for each exit from the scene
        for dir1 in s1.exits.keys():
            # determine canvas location to put the link symbol
            x, y = get_canvas_link_location(s1.location, dir1)
            # choose one of '/', '\', or '|' based on exit direction and
            # add the link symbol to determined canvas location
            canvas[x][y] = SYMBOL_LINK[dir1]
    # draw the canvas
    print_canvas(canvas)


def get_canvas_scene_location(location):
    """ Return corresponding location on the canvas."""
    x, y = location
    # step 1: subtract 1 from x, y since canvas array starts from [0][0]
    x1 = x - 1
    y1 = y - 1
    # step 2: if x or y is greater than 1, add that difference
    x2 = x1 + (x - 1)
    y2 = y1 + (y - 1)
    print "Canvas location: {}".format((x, y))
    return (x2, y2)


def get_canvas_link_location(location, direction):
    """ Return link location on canvas given scene's location."""
    # get canvas location for the scene
    x, y = get_canvas_scene_location(location)
    # calculate canvas location for the link based on link direction

    


def print_canvas(canvas):
    """ Print out the constructed canvas nicely."""
    map_string = ""
    for row in canvas:
        for col in row:
            map_string = "{}{}".format(map_string, col)
        map_string = "{}\n".format(map_string)
    print map_string


def draw_test():
    """ Quick test to see how the map would look."""
    canvas = [
                [' ', ' ', '#'],
                [' ', ' ', '|'],
                [' ', ' ', '#'],
                [' ', '/', ' '],
                ['#', ' ', ' ']
             ]

    map_string = ""
    for row in canvas:
        for col in row:
            map_string = "{}{}".format(map_string, col)
        map_string = "{}\n".format(map_string)
    print map_string

