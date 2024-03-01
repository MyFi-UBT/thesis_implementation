# scenario 1_4: color is decisive criterion (green object in scene => 0; blue object in scene = 1)
# Restrictions:
# a) only 1 object visible in each scene
# b) features that stay the same across all datasets: shape
#    varying features: color (g/b), position (random), size (noisy)
# c) equivalent distribution 1/0
# ----------------
# = scenario 1_1 but with noise in size (5)
import random

from util import compute_random_position, save_tmp, save_values_as_xlsx, create_noise


def compute_scenario1_2(counter, scene_width, scene_height, obj1, obj2, path):
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
        obj1_size_old = obj1.size
        obj1.size = create_noise(obj1.size, 5)
        save_tmp(random_nr, obj1, 1, image_names, position_x, position_y, size_x, size_y, shapes, colors, label)
        # reset old object size
        obj1.size = obj1_size_old
        cntr = cntr+1
    while cntr < counter:
        random_x, random_y = compute_random_position(scene_width, scene_height, obj2)
        obj2.position = (random_x, random_y)
        random_nr = random.randint(0, counter)
        obj2_size_old = obj2.size
        obj2.size = create_noise(obj2.size, 5)
        save_tmp(random_nr, obj2, 0, image_names, position_x, position_y, size_x, size_y, shapes, colors, label)
        obj2.size = obj2_size_old
        cntr = cntr+1
    save_values_as_xlsx(path, "scenario_1_2.xlsx", image_names, position_x, position_y, size_x, size_y, shapes, colors, label)