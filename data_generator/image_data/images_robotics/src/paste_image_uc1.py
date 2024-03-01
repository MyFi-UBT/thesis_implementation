import os

from PIL import Image, ImageDraw, ImageFilter
import random
from random import randrange
from pathlib import Path

def intersection_with_area(end_left_area_x, end_left_area_y, randomxx, randomyy, form):
    if ((randomxx + form.width) > end_left_area_x) or ((randomyy + form.height) > end_left_area_y):
        return True
    else:
        return False

def intersection_with_background(background, randomxx, randomyy, form):
    if ((randomxx + form.width) > background.width) or ((randomyy + form.height) > background.height):
        return True
    else:
        return False


def intersection_with_other_objects(randomxx_1, randomyy_1, img, positions_and_sizes):
    for p in positions_and_sizes:
        pos = p[0]
        size = p[1]

        min_obj1_x = pos[0]
        max_obj1_x = pos[0] + size[0]
        min_obj2_x = randomxx_1
        max_obj2_x = randomxx_1 + img.width

        min_obj1_y = pos[1]
        max_obj1_y = pos[1] + size[1]
        min_obj2_y = randomyy_1
        max_obj2_y = randomyy_1 + img.height

        # check if the objects intersect in x direction, continue means no intersection
        if min_obj2_x > max_obj1_x or min_obj1_x > max_obj2_x:
            continue
        else:
            # check if the objects intersect in y direction
            if min_obj2_y > max_obj1_y or min_obj1_y > max_obj2_y:
                continue
            else:
                # there is an intersection (in x AND in y direction)
                return True
    return False

def create_fixed_position(x, background_image, object_image):

    background = Image.open(background_image)
    background = background.resize((int(background.size[0]/2), int(background.size[1]/2)))
    img = Image.open(object_image)

    posx = 295
    posy = 885 - img.size[1]
    background.paste(img, (posx, posy), img)

    print("printed fixed pos")
    return background

def create_random_positions(x, background_image, object_images, path, label, data_type):
    images = []
    background = Image.open(background_image)
    start_right_area_x = 249
    end_right_area_x = 875
    start_right_area_y = 1296
    end_right_area_y = 1481

    start_left_area_x = 248/2
    end_left_area_x = 1084/2
    start_left_area_y = 648/2
    end_left_area_y = 1072/2
    for oi in object_images:
        img = Image.open(oi)
        images.append(img)

    positions_and_sizes = []
    counter = 0

    for img in images:
        rotate_degree = random.randint(0, 180)
        img = img.rotate(rotate_degree, expand = True)
        randomxx_1 = random.randint(start_left_area_x, end_left_area_x)
        randomyy_1 = random.randint(start_left_area_y, end_left_area_y)
        # for the first object that is pasted, it is only necessary to check if there is an section with the
        # background/image border
        if counter == 0:
            while (intersection_with_area(end_left_area_x, end_left_area_y, randomxx_1, randomyy_1, img)):
                randomxx_1 = random.randint(start_left_area_x, end_left_area_x)
                randomyy_1 = random.randint(start_left_area_y, end_left_area_y)

        # in case other objects already exist in the image, intersections between objects AND with the background
        # have to be avoided
        else:
            while (intersection_with_area(end_left_area_x, end_left_area_y, randomxx_1, randomyy_1, img) or intersection_with_other_objects(randomxx_1, randomyy_1, img,
                                                                                        positions_and_sizes)):
                randomxx_1 = random.randint(start_left_area_x, end_left_area_x)
                randomyy_1 = random.randint(start_left_area_y, end_left_area_y)
        # last parameter in pasting process important for transparent images

        background.paste(img, (randomxx_1, randomyy_1), img.convert('RGBA'))
        position = (randomxx_1, randomyy_1)
        size = (img.width, img.height)
        positions_and_sizes.append((position, size))
        counter = counter + 1

    # define condition for being positive labelled
    # TODO: this condition has to be adjusted manually for each generation case.
    #  We need an (semi-)automated solution here
#    if (positions_and_sizes[2][0][1] < 100 and positions_and_sizes[3][0][1] < 100):
    if label == 1:
        Path(path+'/good').mkdir(parents=True, exist_ok=True)
        nr_of_entries = os.listdir(path+'/good')
        background = background.convert("RGB")
        # the next line is only for reduced images!
        background = background.resize((int(background.size[0] / 2), int(background.size[1] / 2)))
        if data_type == "png":
            background.save(path + '/good/data_' + str(len(nr_of_entries)) + '.png')
        else:
            background.save(path + '/good/data_' + str(len(nr_of_entries)) + '.jpg')
    else:
        Path(path+'/bad').mkdir(parents=True, exist_ok=True)
        nr_of_entries = os.listdir(path + '/bad')
        background = background.convert("RGB")
        # the next line is only for reduced images!
        background = background.resize((int(background.size[0] / 2), int(background.size[1] / 2)))
        if data_type == "png":
            background.save(path + '/bad/data_' + str(len(nr_of_entries)) + '.png')
        else:
            background.save(path + '/bad/data_' + str(len(nr_of_entries)) + '.jpg')
    if data_type == "png":
        print("Successfully created a new image: data_" + str(len(nr_of_entries)) + ".png")
    else:
        print("Successfully created a new image: data_" + str(len(nr_of_entries)) + ".jpg")
