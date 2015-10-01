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
                'nw': '\\',
              }


def draw_map(a_map):
    """ Draw the map with ASCII characters."""
    # create empty canvas (max grid of scenes and links)
    c_size = 2*map_gen.GRID_SIZE - 1
    canvas = [ [ ' ' for i in xrange(c_size) ] for j in xrange(c_size) ]
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
            # choose link symbol
            # if the canvas location isn't a space, draw an 'x' for crossroad
            if canvas[x][y] != ' ':
                link_symbol = SYMBOL_LINK['cross']
            else:
                link_symbol = SYMBOL_LINK[dir1]
            # add the link symbol to determined canvas location
            canvas[x][y] = link_symbol
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
    #print "Canvas location: {}".format((x2, y2))
    return (x2, y2)


def get_canvas_link_location(location, direction):
    """ Return link location on canvas given scene's location."""
    # assumption: min location = (1, 1)
    # location + direction does not go off the map

    # get canvas location for the scene
    x, y = get_canvas_scene_location(location)
    # calculate canvas location for the link based on link direction
    dx, dy = map_gen.DIR_TO_DIFF[direction]
    link_loc = (x + dx, y + dy)
    print "Canvas link location: {}".format(link_loc)
    return link_loc


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

