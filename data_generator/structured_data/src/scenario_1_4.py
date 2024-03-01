# scenario 1_4: color is decisive criterion (green object in scene => 0; blue object in scene = 1)
# Restrictions:
# a) only 1 object visible in each scene
# b) all features instead of the color and the position are the same
# c) non-equivalent distribution 1/0:
#   Number of data sets labelled with 1: counter/3
#   Number of data sets labelled with 0: 2*counter/3 (for green)
# ----------------
# = scenario 1_2 but with non-equivalent distribution
from util import compute_random_position, save_values_as_xlsx, save_tmp
import random


def compute_scenario1_4(counter, scene_width, scene_height, obj1, obj2, path):
    cntr = 1
    image_names = []
    position_x = []
    position_y = []
    size_x = []
    size_y = []
    shapes = []
    colors = []
    label = []
    label_counter_good = 0
    label_counter_bad = 0

    while label_counter_good < counter/3:
        random_x, random_y = compute_random_position(scene_width, scene_height, obj1)
        obj1.position = (random_x, random_y)
        random_nr = random.randint(0, counter)
        if label_counter_good < counter / 3:
            save_tmp(random_nr, obj1, 1, image_names, position_x, position_y, size_x, size_y, shapes, colors, label)
            label_counter_good = label_counter_good + 1
    cntr = label_counter_good
    while(cntr < counter):
        random_x, random_y = compute_random_position(scene_width, scene_height, obj2)
        obj2.position = (random_x, random_y)
        random_nr = random.randint(0, counter)
        save_tmp(random_nr, obj2, 0, image_names, position_x, position_y, size_x, size_y, shapes, colors, label)
        cntr = cntr + 1
    save_values_as_xlsx(path, "scenario_1_4.xlsx", image_names, position_x, position_y, size_x, size_y, shapes, colors, label)
