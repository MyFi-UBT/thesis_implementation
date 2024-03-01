# scenario 2_1: shape and position is decisive criterion (at least one circular object is in the upper seventh of the scene (y > 576) = 1)
# Restrictions:
# a) 4 objects are visible in each scene
# b) features color and size stay the same across all data sets. Shape and Position varies.
# c) equivalent distribution 1/0
import random

from util import compute_random_position, save_tmp, save_values_as_xlsx, compute_random_positions_without_intersections, \
    save_values_as_xlsx_4objects, save_tmp_4objects, paint_image


def compute_scenario2_1(counter, scene_width, scene_height, obj3, obj3_1, obj4, obj4_1, path):
    image_names = []
    positions_x_obj1 = []
    positions_y_obj1 = []
    sizes_x_obj1 = []
    sizes_y_obj1 = []
    shapes_obj1 = []
    colors_obj1 = []
    positions_x_obj2 = []
    positions_y_obj2 = []
    sizes_x_obj2 = []
    sizes_y_obj2 = []
    shapes_obj2 = []
    colors_obj2 = []
    positions_x_obj3 = []
    positions_y_obj3 = []
    sizes_x_obj3 = []
    sizes_y_obj3 = []
    shapes_obj3 = []
    colors_obj3 = []
    positions_x_obj4 = []
    positions_y_obj4 = []
    sizes_x_obj4 = []
    sizes_y_obj4 = []
    shapes_obj4 = []
    colors_obj4 = []
    label = []
    positions = positions_x_obj1, positions_y_obj1, positions_x_obj2, positions_y_obj2, positions_x_obj3, positions_y_obj3, positions_x_obj4, positions_y_obj4
    sizes = sizes_x_obj1, sizes_y_obj1, sizes_x_obj2, sizes_y_obj2, sizes_x_obj3, sizes_y_obj3, sizes_x_obj4, sizes_y_obj4
    shapes = shapes_obj1, shapes_obj2, shapes_obj3, shapes_obj4
    colors = colors_obj1, colors_obj2, colors_obj3, colors_obj4

    obj_array = obj3, obj3_1, obj4, obj4_1
    label_counter_good = 0
    label_counter_bad = 0

    while label_counter_good < counter / 2 or label_counter_bad < counter / 2:
        compute_random_positions_without_intersections(scene_width, scene_height, obj_array)
        random_nr = random.randint(0, counter)
        random_nr_2 = random.randint(0, counter)
        reason = ""
        if label_counter_good < counter / 2:
            if obj3.position[1] > scene_height - (scene_height / 7) or obj3_1.position[1] > scene_height - (
                    scene_height / 7):
                #                print(scene_height / 7)
                if obj3.position[1] > scene_height - (scene_height / 7):
                    reason = "obj3"
                if obj3_1.position[1] > scene_height - (scene_height / 7):
                    reason = "obj3_2"
                if obj3.position[1] > scene_height - (scene_height / 7) and obj3_1.position[1] > scene_height - (
                        scene_height / 7):
                    reason = "obj3_and_3_2"
                save_tmp_4objects(random_nr, obj_array, 1, image_names, positions, sizes, shapes, colors, label)
                label_counter_good = label_counter_good + 1
                # use the next method to paint an image in order to validate the generated data
                # paint_image(1, reason, random_nr, random_nr_2, scene_height, scene_width, obj_array, "../validation_images/scenario2_1/")
        else:
            if label_counter_bad < counter / 2:
                save_tmp_4objects(random_nr, obj_array, 0, image_names, positions, sizes, shapes, colors, label)
                label_counter_bad = label_counter_bad + 1
                # use the next method to paint an image in order to validate the generated data
                # paint_image(0, "undefined", random_nr, random_nr_2, scene_height, scene_width, obj_array, "../validation_images/scenario2_1/")

    save_values_as_xlsx_4objects(path, "scenario_2_1.xlsx", image_names, positions, sizes, shapes, colors, label)
