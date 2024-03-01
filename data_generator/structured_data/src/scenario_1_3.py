# scenario 1_3: color is decisive criterion (green object in scene => 0; blue object in scene = 1)
# Restrictions:
# a) only 1 object visible in each scene
# b) all features instead of the color and the position are the same
# c) equivalent distribution 1/0
import random

from util import compute_random_position, save_tmp, save_values_as_xlsx


def compute_scenario1_3(counter, scene_width, scene_height, obj1, obj2, path):
    cntr = 1
    image_names = []
    position_x = []
    position_y = []
    size_x = []
    size_y = []
    shapes = []
    colors = []
    label = []

    while cntr < counter/2:
        random_x, random_y = compute_random_position(scene_width, scene_height, obj1)
        obj1.position = (random_x, random_y)
        random_nr = random.randint(0, counter)
        save_tmp(random_nr, obj1, 1, image_names, position_x, position_y, size_x, size_y, shapes, colors, label)
        cntr = cntr+1
    while cntr < counter:
        random_x, random_y = compute_random_position(scene_width, scene_height, obj2)
        obj2.position = (random_x, random_y)
        random_nr = random.randint(0, counter)
        save_tmp(random_nr, obj2, 0,image_names, position_x, position_y, size_x, size_y, shapes, colors, label)
        cntr = cntr+1
    save_values_as_xlsx(path, "scenario_1_3.xlsx", image_names, position_x, position_y, size_x, size_y, shapes, colors, label)